# fastapi_service/routers/post.py
import base64
import os
from datetime import datetime, timezone
from typing import Dict, List, Literal
from uuid import UUID, uuid4

from fastapi import APIRouter, Header, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel, Field

# Prefixo alinhado com os testes unitários (/v1/message/send)
router = APIRouter(prefix="/v1/message", tags=["Post Supra-Messenger"])

# --- SCHEMAS ---
class SendMessagePayload(BaseModel):
    recipient_id: str
    content_type: str = Field(default="text/plain")
    payload: str = Field(min_length=1)
    ephemeral_timer: int = Field(default=0, ge=0, le=604800)

class SendMessageResponse(BaseModel):
    message_id: UUID
    mode: Literal["Secret", "Cloud"]
    zios_intelligent: bool
    accepted_at: datetime
    expires_at: datetime | None
    delivery_channel: Literal["redis_pubsub", "in_memory"]


# --- CONNECTION MANAGER ---
class PostConnectionManager:
    """Gerencia conexões WebSocket (suporta múltiplos dispositivos simultâneos por usuário)."""
    
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, user_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.setdefault(user_id, []).append(websocket)

    def disconnect(self, user_id: str, websocket: WebSocket):
        if user_id in self.active_connections:
            self.active_connections[user_id] = [
                ws for ws in self.active_connections[user_id] if ws is not websocket
            ]
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]

    async def send_personal_message(self, message: dict, user_id: str):
        if user_id in self.active_connections:
            for connection in self.active_connections[user_id]:
                await connection.send_json(message)


manager = PostConnectionManager()


# --- UTILITÁRIOS DE SEGURANÇA ---
def _validate_bearer(auth_header: str | None) -> str:
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authorization Bearer token ausente ou inválido.")
    token = auth_header.split(" ", 1)[1].strip()
    if len(token) < 16: # TODO: Substituir por validação real do JWT do Lyv
        raise HTTPException(status_code=401, detail="JWT inválido.")
    return token

def _is_base64_payload(value: str) -> bool:
    try:
        base64.b64decode(value, validate=True)
        return True
    except Exception:
        return False


# --- REST ENDPOINT (Integração de Bots e Mídia - Q3) ---
@router.post("/send", response_model=SendMessageResponse)
async def send_message_rest(
    body: SendMessagePayload,
    authorization: str | None = Header(default=None, alias="Authorization"),
    x_post_mode: Literal["Secret", "Cloud"] = Header(default="Cloud", alias="X-Post-Mode"),
    x_zios_intelligent: Literal["True", "False"] = Header(default="False", alias="X-ZIOS-Intelligent"),
):
    """
    Endpoint via HTTP POST para mensagens sistêmicas.
    No modo Secret, exige conteúdo em Base64 e content_type encriptado.
    """
    _validate_bearer(authorization)

    # Validação do Chat Secreto (Criptografia E2E Mockada)
    if x_post_mode == "Secret":
        if not _is_base64_payload(body.payload):
            raise HTTPException(
                status_code=422,
                detail="No modo Secret, o payload deve ser Base64 válido."
            )
        if "encrypted" not in body.content_type:
            raise HTTPException(
                status_code=422,
                detail="No modo Secret, o content_type deve indicar criptografia."
            )

    accepted_at = datetime.now(timezone.utc)
    expires_at = None
    if body.ephemeral_timer > 0:
        expires_at = datetime.fromtimestamp(
            accepted_at.timestamp() + body.ephemeral_timer,
            tz=timezone.utc,
        )

    message_id = uuid4()

    # Roteia em tempo real se o usuário alvo estiver com o Post aberto
    await manager.send_personal_message(
        {
            "event": "message.new",
            "message_id": str(message_id),
            "mode": x_post_mode,
            "zios_intelligent": x_zios_intelligent == "True",
            "content_type": body.content_type,
            "content": body.payload,
            "accepted_at": accepted_at.isoformat(),
            "expires_at": expires_at.isoformat() if expires_at else None,
        },
        str(body.recipient_id)
    )

    return SendMessageResponse(
        message_id=message_id,
        mode=x_post_mode,
        zios_intelligent=(x_zios_intelligent == "True"),
        accepted_at=accepted_at,
        expires_at=expires_at,
        delivery_channel="redis_pubsub" if os.getenv("REDIS_URL") else "in_memory",
    )


# --- WEBSOCKET ENDPOINT (Core Ultrarrápido) ---
@router.websocket("/ws/{user_id}")
async def post_websocket(websocket: WebSocket, user_id: str):
    """
    Conexão persistente para troca de mensagens e eventos.
    """
    await manager.connect(user_id, websocket)
    
    try:
        while True:
            data = await websocket.receive_json()
            event = data.get("event", "message.send")
            
            if event == "ping":
                await websocket.send_json({"event": "pong", "ts": datetime.now(timezone.utc).isoformat()})
            
            elif event == "typing":
                target_user_id = data.get("to_user_id")
                if target_user_id:
                    await manager.send_personal_message(
                        {
                            "event": "typing.started",
                            "from_user_id": user_id,
                            "at": datetime.now(timezone.utc).isoformat(),
                        },
                        str(target_user_id)
                    )
            
            elif event == "message.send":
                target_user_id = data.get("to_user_id")
                if target_user_id:
                    payload = {
                        "event": "message.new",
                        "message_id": str(uuid4()),
                        "sender_id": user_id,
                        "content": data.get("content"),
                        "timestamp": datetime.now(timezone.utc).isoformat()
                    }
                    
                    await manager.send_personal_message(payload, str(target_user_id))
                    
                    payload["event"] = "message.sent_ack"
                    await manager.send_personal_message(payload, user_id)

    except WebSocketDisconnect:
        manager.disconnect(user_id, websocket)
