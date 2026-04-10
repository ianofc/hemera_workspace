# niocortex/fastapi_service/routers/proactive.py

from fastapi import APIRouter, Header, Depends
from pydantic import BaseModel
from typing import Optional
import random

router = APIRouter(prefix="/v1/proactive", tags=["Proactive Guardian"])

class ContextInput(BaseModel):
    user_role: str
    current_page: str
    user_name: str
    meta_data: Optional[dict] = {}

@router.post("/observe")
async def observe_user(ctx: ContextInput):
    """
    O Zios AI "olha" para o que o usuário está fazendo e decide se fala algo.
    Retorna: { "should_speak": bool, "message": str, "emotion": str }
    """
    
    # Lógica de "Tutorial de Game" / "Amigo"
    
    # 1. Cenário: Professor abrindo o Diário de Classe pela primeira vez (ou vazio)
    if "diario" in ctx.current_page and ctx.user_role == "PROFESSOR":
        # Simulação de verificação de dados
        if ctx.meta_data.get("turma_nova", False):
            return {
                "should_speak": True,
                "emotion": "excited",
                "message": f"Ei {ctx.user_name}! Vi que essa é uma turma nova. Quer que eu gere um Plano de Aula inaugural para quebrar o gelo?"
            }

    # 2. Cenário: Aluno com nota baixa (Acolhimento)
    if "boletim" in ctx.current_page and ctx.user_role == "ALUNO":
        media = ctx.meta_data.get("media_geral", 7.0)
        if media < 6.0:
            return {
                "should_speak": True,
                "emotion": "concerned",
                "message": "Notei que as notas de Matemática caíram. Não desanime! Eu tenho uma lista de exercícios gamificada que pode ajudar. Quer tentar?"
            }

    # 3. Cenário: Diretor no Financeiro (Alerta Estratégico)
    if "financeiro" in ctx.current_page and ctx.user_role == "ADMIN":
        # Random trigger para simular "insight"
        if random.random() > 0.7: 
            return {
                "should_speak": True,
                "emotion": "neutral",
                "message": "Analisando o fluxo... A inadimplência do 3º ano subiu 5% este mês. Sugiro enviar um lembrete amigável aos pais via WhatsApp."
            }

    # 4. Cenário: Ociosidade / Aleatório (Conversa de amigo)
    if random.random() > 0.95: # 5% de chance de falar algo espontâneo
        frases = [
            "Não esqueça de beber água, viu?",
            "Você está mandando muito bem hoje!",
            "Se precisar de ajuda para organizar essa papelada, é só chamar."
        ]
        return {
            "should_speak": True,
            "emotion": "happy",
            "message": random.choice(frases)
        }

    # Se nada acontecer, ele fica em silêncio (observando)
    return {"should_speak": False, "message": "", "emotion": "idle"}