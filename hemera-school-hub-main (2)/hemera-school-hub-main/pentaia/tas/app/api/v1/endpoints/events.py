from fastapi import APIRouter
import os

router = APIRouter()

# Configuração do Redis (Cache de Dopamina)
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

@router.get("/ingest")
async def ingest_event(user_id: str, action: str):
    # Simulação de ingestão para não quebrar se o redis falhar
    return {"status": "received", "dopamine_score": 10}