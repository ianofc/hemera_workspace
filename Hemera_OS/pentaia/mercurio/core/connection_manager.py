import asyncio
import logging
import time
from typing import Dict, Set, List, Any, Optional
from fastapi import WebSocket, WebSocketDisconnect
from .event_bus import EventBus
from .topic_manager import TopicManager

logger = logging.getLogger("MERCURIO_CONNECTION_MANAGER")

class ActiveConnection:
    def __init__(self, websocket: WebSocket, client_id: str, subscribed_patterns: List[str]):
        self.websocket = websocket
        self.client_id = client_id
        self.subscribed_patterns = subscribed_patterns
        self.last_seen = time.time()

class ConnectionManager:
    def __init__(self, event_bus: EventBus, topic_manager: TopicManager, heartbeat_interval: float = 15.0, connection_timeout: float = 30.0):
        self.event_bus = event_bus
        self.topic_manager = topic_manager
        self.heartbeat_interval = heartbeat_interval
        self.connection_timeout = connection_timeout
        
        # Maps client_id -> ActiveConnection
        self._connections: Dict[str, ActiveConnection] = {}
        # Maps websocket object -> client_id for quick reverse lookup
        self._socket_to_id: Dict[WebSocket, str] = {}
        
        self._lock = asyncio.Lock()
        self._heartbeat_task: Optional[asyncio.Task] = None
        self._event_bus_sub_id: Optional[str] = None
        self._running = False

    async def start(self) -> None:
        """Starts the connection manager, registering with the Event Bus and starting heartbeat."""
        async with self._lock:
            if self._running:
                return
            self._running = True
            
            # Subscribe globally to all Event Bus messages to route them to WebSockets
            self._event_bus_sub_id = await self.event_bus.subscribe("*", self._route_event_bus_message)
            self._heartbeat_task = asyncio.create_task(self._heartbeat_loop())
            logger.info("ConnectionManager started successfully. Global listener registered.")

    async def stop(self) -> None:
        """Stops the connection manager, cancelling background tasks and cleaning up connections."""
        async with self._lock:
            self._running = False
            
        if self._heartbeat_task:
            self._heartbeat_task.cancel()
            try:
                await self._heartbeat_task
            except asyncio.CancelledError:
                pass
            self._heartbeat_task = None

        if self._event_bus_sub_id:
            await self.event_bus.unsubscribe("*", self._event_bus_sub_id)
            self._event_bus_sub_id = None

        # Close all active connections
        async with self._lock:
            connections_to_close = list(self._connections.values())
            for conn in connections_to_close:
                try:
                    await conn.websocket.close(code=1001, reason="Server shutting down")
                except Exception:
                    pass
            self._connections.clear()
            self._socket_to_id.clear()
            
        logger.info("ConnectionManager stopped and all connections closed.")

    async def connect(self, websocket: WebSocket, client_id: str, topics: List[str]) -> bool:
        """Accepts a WebSocket connection, validates its topic subscriptions, and stores it in the pool."""
        try:
            await websocket.accept()
        except Exception as e:
            logger.error(f"Failed to accept WebSocket connection for client {client_id}: {e}")
            return False

        # Validate topics and fall back to '*' if empty
        valid_topics = []
        for t in topics:
            if t == "*" or t == "*:*" or self.topic_manager.is_valid_format(t) or "*" in t:
                valid_topics.append(t)
            else:
                logger.warning(f"Client {client_id} requested invalid topic subscription: {t}")

        if not valid_topics:
            valid_topics = ["*"]  # listen to everything as default

        conn = ActiveConnection(websocket, client_id, valid_topics)
        
        async with self._lock:
            # If the client_id is already connected, close the old one to prevent duplicates
            if client_id in self._connections:
                old_conn = self._connections[client_id]
                logger.info(f"Client {client_id} reconnected. Closing previous connection.")
                try:
                    await old_conn.websocket.close(code=1008, reason="Reconnected from another tab/device")
                except Exception:
                    pass
                del self._socket_to_id[old_conn.websocket]

            self._connections[client_id] = conn
            self._socket_to_id[websocket] = client_id

        logger.info(f"Client {client_id} connected. Subscribed topics: {valid_topics}")
        return True

    async def disconnect(self, websocket: WebSocket) -> None:
        """Removes and cleans up a connection from the pool."""
        async with self._lock:
            client_id = self._socket_to_id.pop(websocket, None)
            if client_id and client_id in self._connections:
                del self._connections[client_id]
                logger.info(f"Client {client_id} disconnected and removed from pool.")

    async def handle_ping(self, websocket: WebSocket) -> None:
        """Updates the last_seen timestamp for a client connection when a pong or message is received."""
        async with self._lock:
            client_id = self._socket_to_id.get(websocket)
            if client_id and client_id in self._connections:
                self._connections[client_id].last_seen = time.time()

    async def update_subscriptions(self, client_id: str, new_topics: List[str]) -> bool:
        """Updates the subscribed topics list for a client connection."""
        async with self._lock:
            if client_id not in self._connections:
                return False
            
            valid_topics = []
            for t in new_topics:
                if t == "*" or t == "*:*" or self.topic_manager.is_valid_format(t) or "*" in t:
                    valid_topics.append(t)
            
            if valid_topics:
                self._connections[client_id].subscribed_patterns = valid_topics
                logger.info(f"Updated subscriptions for {client_id} to: {valid_topics}")
                return True
        return False

    async def _route_event_bus_message(self, message: Dict[str, Any]) -> None:
        """Callback that receives messages from the Event Bus and routes them to eligible WebSockets."""
        topic = message.get("_topic", "unknown")
        
        # Prepare targets
        targets: List[ActiveConnection] = []
        async with self._lock:
            for conn in self._connections.values():
                for pattern in conn.subscribed_patterns:
                    if self.topic_manager.match_topic(pattern, topic):
                        targets.append(conn)
                        break  # Match found, move to next client

        if not targets:
            return

        # Broadcast concurrently
        send_tasks = [self._send_safe(conn, message) for conn in targets]
        await asyncio.gather(*send_tasks)

    async def _send_safe(self, conn: ActiveConnection, message: Dict[str, Any]) -> None:
        """Sends a message to a single connection, handling errors and disconnecting if unreachable."""
        try:
            # We strip the internal routing key '_topic' from the sent payload if we want a clean client output
            # but keeping it is useful for the client to know where it came from.
            # We'll keep it so client knows the specific topic!
            await conn.websocket.send_json(message)
        except (WebSocketDisconnect, Exception) as e:
            logger.debug(f"Failed to send message to client {conn.client_id}, disconnecting: {e}")
            await self.disconnect(conn.websocket)

    async def _heartbeat_loop(self) -> None:
        """Periodically checks and cleans up dead connections, sending pings to active ones."""
        while self._running:
            try:
                await asyncio.sleep(self.heartbeat_interval)
                
                now = time.time()
                zombies: List[ActiveConnection] = []
                active_conns: List[ActiveConnection] = []
                
                async with self._lock:
                    for conn in list(self._connections.values()):
                        if now - conn.last_seen > self.connection_timeout:
                            zombies.append(conn)
                        else:
                            active_conns.append(conn)

                # Process zombies
                for zombie in zombies:
                    logger.warning(f"Connection timeout for client {zombie.client_id}. Cleaning up.")
                    try:
                        await zombie.websocket.close(code=1011, reason="Heartbeat timeout")
                    except Exception:
                        pass
                    await self.disconnect(zombie.websocket)

                # Send application-level ping to active connections
                ping_payload = {"type": "ping", "timestamp": now}
                send_ping_tasks = []
                for conn in active_conns:
                    send_ping_tasks.append(self._send_safe(conn, ping_payload))
                
                if send_ping_tasks:
                    await asyncio.gather(*send_ping_tasks)
                    
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in connection manager heartbeat loop: {e}", exc_info=True)
