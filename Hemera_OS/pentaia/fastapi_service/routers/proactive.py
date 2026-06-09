# fastapi_service/routers/proactive.py

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import random
import logging
from ..services.ai import generate_text, gerar_recomendacao_cursos_tas, buscar_noticias_externas_iris

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

class PerformanceEvent(BaseModel):
    aluno_id: int
    turma_id: int
    evento: Dict[str, Any]

class RecommendationItem(BaseModel):
    titulo: str
    categoria: str
    match_score: int
    descricao: str

class NewsItem(BaseModel):
    titulo: str
    fonte: str
    snippet: str
    url: str


# --- HEIMDALL SECURITY CORE (Integrado) ---

@router.get("/heimdall/check")
async def check_request_safety(ip: str):
    """
    HEIMDALL: Responsável pela integridade e segurança.
    Analisa reputação de IP e comportamento suspeito.
    """
    # Filtros de rede local e nós de confiança PentaIA
    if ip.startswith(("127.0.0.1", "192.168", "172.18")):
        return {
            "status": "INTERNAL",
            "shield_level": "MAXIMUM",
            "client_ip": ip,
            "threat_detected": False,
            "reason": "Rede local confiável."
        }

    # Bloqueio simulado para IPs conhecidos da lista negra ou padrão de ameaça alto
    is_suspicious = ip in ["185.220.101.5", "45.132.22.189"] or random.random() > 0.95
    return {
        "status": "PROTECTED" if not is_suspicious else "WARNING",
        "shield_level": "OPTIMAL",
        "client_ip": ip,
        "threat_detected": is_suspicious,
        "reason": "Tentativa de injeção de prompt no PENTAIA" if is_suspicious else "IP Residencial Confiável"
    }


# --- ZIOS OBSERVATION ENGINE ---

@router.post("/observe", response_model=ObservationResponse)
async def observe_user(ctx: ContextInput):
    """
    ZIOS AI: O cérebro que decide quando intervir proativamente.
    """
    # 1. CONTEXTO DE SEGURANÇA IMEDIATO
    if ctx.meta_data.get("risk_detected", False):
        return ObservationResponse(
            should_speak=True,
            emotion="protective",
            source="HEIMDALL",
            message=f"Segurança em primeiro lugar, {ctx.user_name}. Detectamos um comportamento anômalo. O Heimdall elevou o nível do escudo preventivamente."
        )

    # 2. DECISÃO DA IA DE ACORDO COM O CONTEXTO
    prompt = f"""
    Você é o ZIOS AI, o cérebro proativo e tutor pedagógico do Hemera OS.
    Analise o contexto de navegação atual do usuário para decidir se deve enviar uma mensagem de suporte proativo útil ou permanecer em silêncio (de acordo com as necessidades e regras de negócio do Hemera).
    
    Contexto do Usuário:
    - Nome: {ctx.user_name}
    - Cargo: {ctx.user_role}
    - Página Atual: {ctx.current_page}
    - Metadados: {ctx.meta_data}
    
    Diretrizes:
    - Se a página atual for "diario" e o cargo for "PROFESSOR", sugira de forma empolgante gerar planos de aula ou atividades práticas alinhadas à BNCC.
    - Se a página atual for "boletim" e o cargo for "ALUNO" e as notas/médias nos metadados estiverem baixas (< 6.0), envie uma mensagem de apoio amigável e ofereça ajuda com trilhas de reforço no Moodle (Accubens/dopamina).
    - Se for "financeiro" e o cargo for "ADMIN", analise metadados de inadimplência e recomende ações de cobrança automatizadas.
    - Se for um contexto geral sem necessidade de interrupção, permaneça em silêncio.
    
    Responda em formato JSON estrito com os campos: should_speak (bool), message (str), emotion (str), source (str).
    Formatos possíveis de emotion: 'happy', 'concerned', 'excited', 'neutral', 'protective', 'idle'.
    Formatos possíveis de source: 'ZIOS', 'IRIS', 'HEIMDALL', 'TAS', 'SYSTEM'.
    """
    import json
    try:
        from google import genai
        from google.genai import types
        api_key = random.choice([x for x in [generate_text.__globals__.get("api_key")] if x])
        
        if not api_key:
            raise ValueError("Chave de API não configurada.")
            
        client = genai.Client(api_key=api_key)
        response = await client.aio.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=ObservationResponse
            )
        )
        data = json.loads(response.text)
        return ObservationResponse(**data)
    except Exception as e:
        logger.error(f"Erro na observação por IA, usando fallback: {e}")
        
        # Fallback estático
        if "diario" in ctx.current_page and ctx.user_role == "PROFESSOR":
            return ObservationResponse(
                should_speak=True,
                emotion="excited",
                source="ZIOS",
                message=f"Ei {ctx.user_name}! O TAS sugere um Plano de Aula focado em integração pedagógica para hoje. Quer ver?"
            )
        return ObservationResponse(
            should_speak=False,
            message="",
            emotion="idle",
            source="SYSTEM"
        )


# --- TAS PREDITIVO (RECOMENDAÇÃO DE CURSOS / MOODLE) ---

@router.post("/tas/recommendations", response_model=List[RecommendationItem])
async def get_tas_recommendations(perfil: dict):
    """
    TAS: Retorna sugestões do Moodle e cursos de acordo com o que o usuário mais gosta e precisa.
    """
    try:
        recs = await gerar_recomendacao_cursos_tas(perfil)
        return recs
    except Exception as e:
        logger.error(f"Erro ao buscar recomendações do TAS: {e}")
        return []


# --- IRIS NEWS CRAWLER (NOTÍCIAS EXTERNAS) ---

@router.get("/iris/news", response_model=List[NewsItem])
async def get_iris_news():
    """
    IRIS: Busca notícias externas sobre EdTech e educação geral na web.
    """
    try:
        news = await buscar_noticias_externas_iris()
        return news
    except Exception as e:
        logger.error(f"Erro ao buscar notícias da IRIS: {e}")
        return []


# --- ANALISE PERFORMANCE WEBHOOK (INTEGRAÇÃO DJANGO) ---

@router.post("/analyze-performance")
async def analyze_performance_trigger(payload: PerformanceEvent):
    """
    Acionado via webhook do Django quando notas/frequências são inseridas.
    O TAS avalia e reporta o risco pedagógico.
    """
    logger.info(f"TAS Analysis Triggered for Aluno {payload.aluno_id} in Turma {payload.turma_id}")
    evento = payload.evento
    tipo = evento.get("tipo")
    
    prompt = f"""
    Você é o TAS (Total Analysis System), o motor de recomendação do Hemera OS.
    Analise o seguinte evento acadêmico do aluno {payload.aluno_id} na turma {payload.turma_id}:
    - Tipo: {tipo}
    - Dados: {evento}
    
    Avalie o risco acadêmico (evasão/reprovação) e recomende a melhor ação.
    Retorne um JSON estrito contendo:
    {{
        "status": "analyzed",
        "risk": "HIGH" | "MEDIUM" | "LOW",
        "action": "Ação recomendada pelo sistema"
    }}
    """
    import json
    try:
        from google import genai
        api_key = generate_text.__globals__.get("api_key")
        if not api_key:
            raise ValueError("Chave de API não configurada.")
            
        client = genai.Client(api_key=api_key)
        response = await client.aio.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config={"response_mime_type": "application/json"}
        )
        return json.loads(response.text)
    except Exception as e:
        logger.error(f"Erro no TAS webhook performance: {e}")
        # Fallback
        if tipo == "nota":
            valor = evento.get("valor", 10.0)
            if valor < 5.0:
                return {"status": "analyzed", "risk": "HIGH", "action": "Acionar ZIOS para recuperação paralela."}
        return {"status": "analyzed", "risk": "LOW", "action": "Nenhuma ação necessária."}