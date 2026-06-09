import logging
from typing import Dict, Set
from fastapi import WebSocket

logger = logging.getLogger("hermes.pool")

class HermesConnectionPool:
    """
    WebSocket Connection Pool otimizado para alta concorrência.
    Permite múltiplos dispositivos por usuário (mapeando user_id para um set de conexões abertas).
    Lida com conexões quebradas automaticamente durante o envio de mensagens.
    """
    def __init__(self):
        # Dicionário de user_id -> Set de conexões de WebSocket
        self.active_connections: Dict[str, Set[WebSocket]] = {}

    async def connect(self, user_id: str, websocket: WebSocket):
        """
        Aceita o handshake do WebSocket e registra o socket no pool do usuário.
        """
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = set()
        self.active_connections[user_id].add(websocket)
        logger.info(f"Usuário {user_id} conectado. Conexões ativas do usuário: {len(self.active_connections[user_id])}")

    async def disconnect(self, user_id: str, websocket: WebSocket):
        """
        Remove com segurança a conexão do pool do usuário.
        """
        if user_id in self.active_connections:
            self.active_connections[user_id].discard(websocket)
            # Remove a chave se não houver mais conexões ativas
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]
            logger.info(f"Conexão do usuário {user_id} removida. Restantes: {len(self.active_connections.get(user_id, []))}")

    async def send_personal_message(self, message: str, user_id: str) -> bool:
        """
        Envia uma mensagem (como texto) a todas as conexões ativas associadas a um user_id.
        Retorna True se pelo menos um envio foi bem-sucedido.
        """
        if user_id not in self.active_connections or not self.active_connections[user_id]:
            logger.debug(f"Tentativa de envio de mensagem para {user_id}, mas o usuário está offline.")
            return False

        disconnected_sockets = set()
        success = False

        # Itera sobre uma cópia das conexões para evitar erros de modificação simultânea (RuntimeError)
        for connection in list(self.active_connections[user_id]):
            try:
                await connection.send_text(message)
                success = True
            except Exception as e:
                logger.warning(f"Erro ao enviar mensagem para {user_id} no socket {connection}: {e}")
                disconnected_sockets.add(connection)

        # Remove conexões com falha de forma assíncrona
        for socket in disconnected_sockets:
            await self.disconnect(user_id, socket)

        return success

    async def broadcast(self, message: str):
        """
        Envia uma mensagem para todas as conexões abertas no pool.
        """
        disconnected_connections = []

        # Itera sobre todas as conexões ativas e envia de forma assíncrona
        for user_id, sockets in list(self.active_connections.items()):
            for socket in list(sockets):
                try:
                    await socket.send_text(message)
                except Exception as e:
                    logger.warning(f"Erro no broadcast para o usuário {user_id}: {e}")
                    disconnected_connections.append((user_id, socket))

        # Limpa as conexões que falharam
        for user_id, socket in disconnected_connections:
            await self.disconnect(user_id, socket)

    def get_connection_count(self) -> int:
        """
        Retorna a contagem total de conexões abertas no momento.
        """
        return sum(len(sockets) for sockets in self.active_connections.values())

    def is_user_online(self, user_id: str) -> bool:
        """
        Retorna se o usuário tem conexões ativas.
        """
        return user_id in self.active_connections and len(self.active_connections[user_id]) > 0
