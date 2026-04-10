# io_zios/routers/chat.py
from fastapi import APIRouter, HTTPException, Depends, Header
from pydantic import BaseModel
from core.agents import AgentFactory
import os

router = APIRouter(prefix="/v1/chat", tags=["Universal Chat"])

class ChatRequest(BaseModel):
    message: str
    role: str       # QUEM fala (Professor, Aluno, Pai)
    user_name: str
    context: dict   # Dados extras (ID da turma, Nome do Filho, etc)

# Segurança
async def verify_token(x_service_token: str = Header(..., alias="X-Service-Token")):
    expected = os.getenv("SERVICE_TOKEN_SECRET", "segredo_mestre_do_ian_123")
    if x_service_token != expected:
        raise HTTPException(status_code=403, detail="Acesso negado ao Chat Universal.")

@router.post("/interact")
async def chat_interact(req: ChatRequest, token: str = Depends(verify_token)):
    """
    O Ponto Único de Contato com o IO CONSCIOS.
    O sistema identifica o papel (Role) e aciona o Agente correto.
    """
    
    # 1. Fábrica de Agentes
    # O Zios instância a "persona" correta para atender a requisição
    agent = AgentFactory.get_agent(req.role, {
        "user_name": req.user_name, 
        **req.context
    })
    
    # 2. Processamento Cognitivo
    # O Agente processa a mensagem com o contexto específico
    response_text = agent.process(req.message)
    
    return {
        "status": "success",
        "reply": response_text,
        "agent_type": req.role,
        "mode": "Oráculo"
    }