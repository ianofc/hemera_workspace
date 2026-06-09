from fastapi import APIRouter, Query
from typing import List, Optional
import os
from app.engines.thalamus.queue import talamus_queue
from app.engines.thalamus.ingress import thalamus_ingress

router = APIRouter()

# Configuração do Redis (Cache de Dopamina)
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

@router.get("/ingest")
async def ingest_event(
    user_id: str,
    action: str,
    tags: Optional[List[str]] = Query(default=None)
):
    # 1. Sanitiza os inputs
    sanitized_user_id = thalamus_ingress.sanitize_string(user_id)
    sanitized_action = thalamus_ingress.sanitize_string(action)
    sanitized_tags = thalamus_ingress.sanitize_tags(tags or [])

    # 2. Prepara o payload
    event_payload = {
        "user_id": sanitized_user_id,
        "action": sanitized_action,
        "event_type": sanitized_action,
        "tags": sanitized_tags,
    }

    # 3. Publica na fila de eventos de forma assíncrona e desacoplada
    await talamus_queue.publish(event_payload)

    return {
        "status": "received",
        "user_id": sanitized_user_id,
        "action": sanitized_action,
        "tags": sanitized_tags
    }