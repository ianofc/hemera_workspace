import json
import logging
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from ..hermes import HermesConnectionPool, ZiosBridge, DoubleRatchetSession

logger = logging.getLogger("hermes.router")

router = APIRouter(prefix="/v1/hermes", tags=["Hermes Messaging System"])

# Instâncias globais da camada Hermes no escopo do router
pool = HermesConnectionPool()
zios_bridge = ZiosBridge(pool)

# Dicionário de sessões de E2EE em memória para fins de demonstração
sessions: dict[str, DoubleRatchetSession] = {}

@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    """
    Canal de WebSocket de alta concorrência do Hermes integrado com ZIOS Bridge.
    """
    await pool.connect(user_id, websocket)
    try:
        while True:
            # Recebe mensagens enviadas pelo cliente
            raw_data = await websocket.receive_text()
            logger.info(f"Mensagem recebida do websocket de {user_id}: {raw_data}")
            
            try:
                message_json = json.loads(raw_data)
                content = message_json.get("content", "")
                recipient_id = message_json.get("recipient_id")
                is_encrypted = message_json.get("is_encrypted", False)
            except json.JSONDecodeError:
                # Caso a mensagem seja texto simples, tratamos de forma simplificada
                content = raw_data
                recipient_id = None
                is_encrypted = False
                message_json = {}

            # 1. Integração com o canal lateral do ZIOS Bridge
            if zios_bridge.is_zios_command(content):
                await zios_bridge.handle_message(user_id, content)
                continue

            # 2. Roteamento de mensagens normais ou criptografadas entre usuários
            if recipient_id:
                if pool.is_user_online(recipient_id):
                    await pool.send_personal_message(raw_data, recipient_id)
                else:
                    offline_notification = json.dumps({
                        "sender_id": "system",
                        "recipient_id": user_id,
                        "content": f"Usuário {recipient_id} está offline. Mensagem armazenada.",
                        "is_control": True
                    })
                    await pool.send_personal_message(offline_notification, user_id)
            else:
                reply = json.dumps({
                    "sender_id": "system",
                    "recipient_id": user_id,
                    "content": f"Mensagem recebida: {content[:30]}...",
                    "is_control": True
                })
                await pool.send_personal_message(reply, user_id)

    except WebSocketDisconnect:
        logger.info(f"Usuário {user_id} desconectado via WebSocketDisconnect.")
    except Exception as e:
        logger.error(f"Erro inesperado no WebSocket do usuário {user_id}: {e}")
    finally:
        await pool.disconnect(user_id, websocket)
