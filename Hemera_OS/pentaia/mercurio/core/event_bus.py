import asyncio
import json
import logging
import uuid
from abc import ABC, abstractmethod
from typing import Dict, Callable, Awaitable, Any, Optional, Set
import redis.asyncio as aioredis
from .topic_manager import TopicManager

logger = logging.getLogger("MERCURIO_EVENT_BUS")

class EventBus(ABC):
    @abstractmethod
    async def start(self) -> None:
        pass

    @abstractmethod
    async def stop(self) -> None:
        pass

    @abstractmethod
    async def publish(self, topic: str, message: Dict[str, Any]) -> int:
        """Publishes a message to a topic. Returns the number of subscribers notified."""
        pass

    @abstractmethod
    async def subscribe(self, pattern: str, callback: Callable[[Dict[str, Any]], Awaitable[None]]) -> str:
        """Subscribes to a topic pattern (supports exact and wildcards like 'metrics:*').
        Returns a unique subscription ID.
        """
        pass

    @abstractmethod
    async def unsubscribe(self, pattern: str, subscription_id: str) -> bool:
        """Unsubscribes using the pattern and subscription ID. Returns True if found and removed."""
        pass


class InMemoryEventBus(EventBus):
    def __init__(self, topic_manager: TopicManager):
        self._topic_manager = topic_manager
        # Mapping: pattern -> {subscription_id: callback}
        self._subscriptions: Dict[str, Dict[str, Callable[[Dict[str, Any]], Awaitable[None]]]] = {}
        self._lock = asyncio.Lock()
        self._running = False

    async def start(self) -> None:
        self._running = True
        logger.info("InMemoryEventBus started successfully.")

    async def stop(self) -> None:
        self._running = False
        async with self._lock:
            self._subscriptions.clear()
        logger.info("InMemoryEventBus stopped.")

    async def publish(self, topic: str, message: Dict[str, Any]) -> int:
        if not self._running:
            logger.warning("Event bus not running. Cannot publish.")
            return 0

        # Validate topic format
        if not self._topic_manager.is_valid_format(topic):
            logger.warning(f"Refusing to publish to invalid topic format: {topic}")
            return 0

        notified_count = 0
        async with self._lock:
            # We check which registered patterns match the incoming topic
            for pattern, subs in self._subscriptions.items():
                if self._topic_manager.match_topic(pattern, topic):
                    for sub_id, callback in list(subs.items()):
                        # Trigger callback asynchronously to not block the publisher
                        asyncio.create_task(self._safe_execute(callback, topic, message))
                        notified_count += 1
        return notified_count

    async def subscribe(self, pattern: str, callback: Callable[[Dict[str, Any]], Awaitable[None]]) -> str:
        # Check if the subscription pattern contains wildcard or is exact, validate prefix
        prefix = pattern.split(":")[0] if ":" in pattern else pattern
        if prefix not in self._topic_manager._allowed_prefixes and pattern != "*" and pattern != "*:*":
            logger.warning(f"Subscribing to non-standard pattern: {pattern}")

        subscription_id = str(uuid.uuid4())
        async with self._lock:
            if pattern not in self._subscriptions:
                self._subscriptions[pattern] = {}
            self._subscriptions[pattern][subscription_id] = callback
            
        logger.debug(f"Subscribed callback to pattern '{pattern}' (ID: {subscription_id})")
        return subscription_id

    async def unsubscribe(self, pattern: str, subscription_id: str) -> bool:
        async with self._lock:
            if pattern in self._subscriptions and subscription_id in self._subscriptions[pattern]:
                del self._subscriptions[pattern][subscription_id]
                if not self._subscriptions[pattern]:
                    del self._subscriptions[pattern]
                logger.debug(f"Unsubscribed subscription ID '{subscription_id}' from pattern '{pattern}'")
                return True
        return False

    async def _safe_execute(self, callback: Callable[[Dict[str, Any]], Awaitable[None]], topic: str, message: Dict[str, Any]):
        try:
            # Injecting topic into message metadata if not present
            enriched_msg = {**message, "_topic": topic}
            await callback(enriched_msg)
        except Exception as e:
            logger.error(f"Error in EventBus subscriber callback for topic {topic}: {e}", exc_info=True)


class RedisEventBus(EventBus):
    def __init__(self, topic_manager: TopicManager, redis_url: str = "redis://localhost:6379/0"):
        self._topic_manager = topic_manager
        self._redis_url = redis_url
        self._client: Optional[aioredis.Redis] = None
        self._pubsub: Optional[aioredis.client.PubSub] = None
        # Local routing table: pattern -> {subscription_id: callback}
        self._subscriptions: Dict[str, Dict[str, Callable[[Dict[str, Any]], Awaitable[None]]]] = {}
        self._lock = asyncio.Lock()
        self._listener_task: Optional[asyncio.Task] = None
        self._running = False

    async def start(self) -> None:
        async with self._lock:
            if self._running:
                return
            
            logger.info(f"Connecting to Redis Event Bus at {self._redis_url}...")
            self._client = aioredis.from_url(self._redis_url, decode_responses=True)
            # Perform a quick ping to ensure connection works
            await self._client.ping()
            
            self._pubsub = self._client.pubsub()
            self._running = True
            self._listener_task = asyncio.create_task(self._listen_loop())
            logger.info("RedisEventBus started and connected.")

    async def stop(self) -> None:
        async with self._lock:
            self._running = False
            
        if self._listener_task:
            self._listener_task.cancel()
            try:
                await self._listener_task
            except asyncio.CancelledError:
                pass
            self._listener_task = None

        async with self._lock:
            if self._pubsub:
                await self._pubsub.close()
                self._pubsub = None
            if self._client:
                await self._client.close()
                self._client = None
            self._subscriptions.clear()
        logger.info("RedisEventBus stopped and connections closed.")

    async def publish(self, topic: str, message: Dict[str, Any]) -> int:
        if not self._running or not self._client:
            logger.warning("Redis Event Bus is not running.")
            return 0

        if not self._topic_manager.is_valid_format(topic):
            logger.warning(f"Refusing to publish to invalid topic format: {topic}")
            return 0

        # Redis publish returns the number of clients that received the message
        # within Redis, but since we publish on a topic, we use JSON string.
        payload = json.dumps(message)
        receivers = await self._client.publish(topic, payload)
        return receivers

    async def subscribe(self, pattern: str, callback: Callable[[Dict[str, Any]], Awaitable[None]]) -> str:
        subscription_id = str(uuid.uuid4())
        
        async with self._lock:
            is_new_pattern = pattern not in self._subscriptions
            if is_new_pattern:
                self._subscriptions[pattern] = {}
            self._subscriptions[pattern][subscription_id] = callback

        # If it's a new pattern, register it with the Redis PubSub connection
        if is_new_pattern and self._running and self._pubsub:
            if "*" in pattern:
                await self._pubsub.psubscribe(pattern)
                logger.info(f"Registered Redis Pattern Subscribe (psubscribe) for '{pattern}'")
            else:
                await self._pubsub.subscribe(pattern)
                logger.info(f"Registered Redis Channel Subscribe (subscribe) for '{pattern}'")
                
        return subscription_id

    async def unsubscribe(self, pattern: str, subscription_id: str) -> bool:
        async with self._lock:
            if pattern not in self._subscriptions or subscription_id not in self._subscriptions[pattern]:
                return False
                
            del self._subscriptions[pattern][subscription_id]
            is_empty = len(self._subscriptions[pattern]) == 0
            if is_empty:
                del self._subscriptions[pattern]

        # If no local subscribers are left for this pattern, unsubscribe from Redis
        if is_empty and self._running and self._pubsub:
            try:
                if "*" in pattern:
                    await self._pubsub.punsubscribe(pattern)
                    logger.info(f"Unregistered Redis Pattern Subscribe for '{pattern}'")
                else:
                    await self._pubsub.unsubscribe(pattern)
                    logger.info(f"Unregistered Redis Channel Subscribe for '{pattern}'")
            except Exception as e:
                logger.error(f"Error unsubscribing from Redis: {e}")
                
        return True

    async def _listen_loop(self) -> None:
        """Listens for messages arriving from Redis and forwards them to registered callbacks."""
        while self._running:
            try:
                if not self._pubsub:
                    await asyncio.sleep(0.5)
                    continue
                    
                # get_message checks for messages or blocks
                msg = await self._pubsub.get_message(ignore_subscribe_messages=True, timeout=1.0)
                if msg is None:
                    continue
                
                channel = msg.get("channel")
                pattern = msg.get("pattern")
                data_raw = msg.get("data")
                
                if not channel or not data_raw:
                    continue
                
                try:
                    data = json.loads(data_raw)
                except json.JSONDecodeError:
                    data = {"raw": data_raw}
                
                # Check who should receive this message based on the matched pattern or channel
                async with self._lock:
                    matched_patterns = []
                    # In Redis, pattern messages have the 'pattern' field filled
                    # But we also validate locally using TopicManager for correctness
                    for registered_pattern in self._subscriptions.keys():
                        if (pattern and registered_pattern == pattern) or \
                           (self._topic_manager.match_topic(registered_pattern, channel)):
                            matched_patterns.append(registered_pattern)
                            
                    for pat in matched_patterns:
                        for callback in list(self._subscriptions[pat].values()):
                            asyncio.create_task(self._safe_execute(callback, channel, data))
                            
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in Redis PubSub listen loop: {e}", exc_info=True)
                await asyncio.sleep(1.0) # avoid tight loop on persistent failures

    async def _safe_execute(self, callback: Callable[[Dict[str, Any]], Awaitable[None]], topic: str, message: Dict[str, Any]):
        try:
            enriched_msg = {**message, "_topic": topic}
            await callback(enriched_msg)
        except Exception as e:
            logger.error(f"Error executing callback in RedisEventBus for topic {topic}: {e}")


async def create_event_bus(topic_manager: TopicManager, redis_url: Optional[str] = None) -> EventBus:
    """Factory to instantiate and start the appropriate Event Bus.
    Falls back to InMemoryEventBus if Redis is unavailable.
    """
    if redis_url:
        try:
            bus = RedisEventBus(topic_manager, redis_url)
            await bus.start()
            logger.info("Using high-performance Redis Event Bus.")
            return bus
        except Exception as e:
            logger.warning(f"Could not connect to Redis: {e}. Falling back to InMemoryEventBus.")
    
    bus = InMemoryEventBus(topic_manager)
    await bus.start()
    logger.info("Using local InMemory Event Bus fallback.")
    return bus
