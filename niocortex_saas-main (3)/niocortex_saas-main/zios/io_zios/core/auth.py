from fastapi import Header, HTTPException
from core.config import settings
from core.logger import logger

async def verify_service_token(x_service_token: str = Header(..., alias="X-Service-Token")):
    """Verifica se a chamada vem de um app autorizado."""
    if x_service_token != settings.SERVICE_TOKEN:
        logger.warning(f"Acesso negado. Token inválido: {x_service_token[:5]}***")
        raise HTTPException(status_code=403, detail="Acesso negado: Token de serviço inválido")
    return True