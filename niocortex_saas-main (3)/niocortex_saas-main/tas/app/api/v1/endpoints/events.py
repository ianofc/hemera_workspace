from fastapi import APIRouter, Depends
from app.schemas.user import UserEvent
from app.db.session import get_db
import aioredis # Para cache rápido de comportamento (Dopamina temporária)

router = APIRouter()

@router.post("/track")
async def track_user_behavior(event: UserEvent):
    # Aqui, em sistemas de alta escala, salvaríamos no Redis e depois no DB
    # Por enquanto, vamos logar que o motor recebeu o estímulo
    print(f"🔥 [ACCUMBENS] Estímulo recebido: {event.event_type} no conteúdo {event.content_id}")
    return {"status": "tracked", "reward_processed": True}