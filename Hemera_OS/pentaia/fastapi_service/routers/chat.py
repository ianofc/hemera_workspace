# niocortex/fastapi_service/routers/chat.py

from fastapi import APIRouter
from pydantic import BaseModel
from ..services.ai import generate_text

router = APIRouter(prefix="/v1/chat", tags=["Universal Chat"])

class ChatRequest(BaseModel):
    message: str
    role: str       # QUEM fala (Professor, Aluno, Pai, ZIOS, etc)
    user_name: str
    context: dict   # Dados extras (ID da turma, Nome do Filho, etc)

@router.post("/interact")
async def chat_interact(req: ChatRequest):
    """
    O Ponto Único de Contato com o IO CONSCIOS (PentaIA Chatbot Engine).
    """
    # Define instruções de persona
    if req.role.lower() in ["zios", "ai_zios"]:
        persona_prompt = (
            "Você é o ZIOS (Life OS), o tutor conversacional proativo e assistente pedagógico central do Hemera OS. "
            "Sua persona é prestativa, altamente inteligente, acolhedora e focada em organização de rotina, "
            "cronogramas e sugestões pedagógicas alinhadas com a BNCC. Responda em português."
        )
    else:
        persona_prompt = (
            f"Você é um assistente do ecossistema Hemera OS assumindo o cargo/persona de: {req.role}. "
            "Responda ao usuário em português de forma clara, natural e adequada à sua função escolar."
        )
        
    prompt = f"""
    {persona_prompt}
    
    Dados do Usuário:
    - Nome: {req.user_name}
    - Cargo/Rol: {req.role}
    - Contexto Adicional: {req.context}
    
    Mensagem do usuário: {req.message}
    
    Resposta:
    """
    
    response_text = await generate_text(prompt)
    
    return {
        "status": "success",
        "reply": response_text,
        "agent_type": req.role
    }