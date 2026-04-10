# fastapi_service/routers/proactive.py

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
import random
import logging

# Configuração de logs para o monitoramento PentaIA
logger = logging.getLogger("ZIOS_PROACTIVE")
router = APIRouter(prefix="/v1/proactive", tags=["Proactive Guardian"])

# --- SCHEMAS ---

class ContextInput(BaseModel):
    user_role: str        # PROFESSOR, ALUNO, ADMIN, STANDARD, PREMIUM
    current_page: str     # diario, boletim, financeiro, feed, explore, mercurio
    user_name: str
    meta_data: Optional[dict] = {}

class ObservationResponse(BaseModel):
    should_speak: bool
    message: str
    emotion: str
    source: str           # ZIOS, IRIS, HEIMDALL, TAS

# --- HEIMDALL SECURITY CORE (Integrado) ---

@router.get("/heimdall/check")
async def check_request_safety(ip: str):
    """
    HEIMDALL: Responsável pela integridade e segurança.
    Analisa reputação de IP e comportamento suspeito.
    """
    is_suspicious = False
    
    # Filtros de rede local e nós de confiança PentaIA
    if ip.startswith(("127.0.0.1", "192.168", "172.18")):
        return {
            "status": "INTERNAL",
            "shield_level": "MAXIMUM",
            "client_ip": ip,
            "threat_detected": False
        }

    # Simulação de detecção de Bot/Threat (GreyNoise logic)
    if random.random() > 0.99: # Simulação de IP malicioso
        is_suspicious = True

    return {
        "status": "PROTECTED" if not is_suspicious else "WARNING",
        "shield_level": "OPTIMAL",
        "client_ip": ip,
        "threat_detected": is_suspicious
    }

# --- ZIOS OBSERVATION ENGINE ---

@router.post("/observe", response_model=ObservationResponse)
async def observe_user(ctx: ContextInput):
    """
    ZIOS AI: O cérebro que decide quando intervir proativamente.
    Utiliza o TAS para cálculos de métricas e IRIS para pulso de rede.
    """
    
    # 1. CONTEXTO DE SEGURANÇA (Intervenção do HEIMDALL via ZIOS)
    if ctx.meta_data.get("risk_detected", False):
        return {
            "should_speak": True,
            "emotion": "protective",
            "source": "HEIMDALL",
            "message": f"Segurança em primeiro lugar, {ctx.user_name}. Detectamos um comportamento anômalo. O Heimdall elevou o nível do escudo preventivamente."
        }

    # 2. CONTEXTO EDUCACIONAL: Professor no Diário
    if "diario" in ctx.current_page and ctx.user_role == "PROFESSOR":
        if ctx.meta_data.get("turma_nova", False):
            return {
                "should_speak": True,
                "emotion": "excited",
                "source": "ZIOS",
                "message": f"Ei {ctx.user_name}! Essa turma é nova por aqui. O TAS sugere um Plano de Aula focado em integração para hoje. Quer ver?"
            }

    # 3. CONTEXTO EDUCACIONAL: Aluno no Boletim (Acolhimento)
    if "boletim" in ctx.current_page and ctx.user_role == "ALUNO":
        media = ctx.meta_data.get("media_geral", 7.0)
        if media < 6.0:
            return {
                "should_speak": True,
                "emotion": "concerned",
                "source": "ZIOS",
                "message": "Notei que o desempenho em exatas oscilou. Não se cobre tanto! O TAS preparou uma trilha de reforço gamificada para você."
            }

    # 4. CONTEXTO FINANCEIRO/ADMIN: Alerta Estratégico (Poder do TAS)
    if "financeiro" in ctx.current_page and ctx.user_role == "ADMIN":
        inadimplencia = ctx.meta_data.get("taxa_inadimplencia", 0)
        if inadimplencia > 10:
            return {
                "should_speak": True,
                "emotion": "neutral",
                "source": "TAS",
                "message": f"Análise concluída: A inadimplência subiu {inadimplencia}%. O TAS recomenda automatizar as cobranças via Thalamus agora."
            }

    # 5. CONTEXTO DE REDE/NOTÍCIAS (Poder da IRIS)
    if ctx.current_page in ["explore", "feed", "mercurio"]:
        top_hashtag = ctx.meta_data.get("trending_hashtag", None)
        if top_hashtag and random.random() > 0.8:
            return {
                "should_speak": True,
                "emotion": "happy",
                "source": "IRIS",
                "message": f"O mundo está falando de {top_hashtag}! A IRIS detectou um pico de engajamento. Vale a pena conferir o contexto."
            }

    # 6. CONTEXTO HUMANO: Bem-estar (ZIOS Amigo)
    if random.random() > 0.96:
        frases = [
            f"Tudo em ordem por aqui, {ctx.user_name}. Lembre-se de descansar um pouco.",
            "O ecossistema PentaIA está operando em harmonia.",
            "Sempre de olho para que você possa focar no que importa."
        ]
        return {
            "should_speak": True,
                "emotion": "happy",
                "source": "ZIOS",
                "message": random.choice(frases)
        }

    # Silêncio operacional (ZIOS apenas observa)
    return {
        "should_speak": False, 
        "message": "", 
        "emotion": "idle",
        "source": "SYSTEM"
    }