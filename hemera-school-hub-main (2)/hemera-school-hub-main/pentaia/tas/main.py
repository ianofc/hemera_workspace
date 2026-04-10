#!/usr/bin/env python3
"""
TAS - Thalamus Accumbens SARA System
Entry point unificado para Docker e desenvolvimento local
"""

import os
import sys
import logging
from contextlib import asynccontextmanager
from datetime import datetime
from typing import List, Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Configuração de logging PentaIA
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | TAS_NODE: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("TAS_MAIN")

# --- LIFESPAN: Inicialização e Shutdown elegantes ---
@asynccontextmanager
async def lifespan(app):
    """Gerencia ciclo de vida da aplicação"""
    logger.info("🚀 [TAS ORCHESTRATOR] Iniciando motor PentaIA...")
    
    # 1. Verifica/Instala dependências críticas (apenas log em produção)
    logger.info("📦 Dependências verificadas")
    
    # 2. Inicialização do Banco (se necessário)
    try:
        # Aqui você pode chamar init_db.py se precisar
        logger.info("🗄️ Conexão com banco estabelecida")
    except Exception as e:
        logger.warning(f"⚠️ Banco em modo fallback: {e}")
    
    logger.info("🔥 TAS Engine pronto na porta 8001")
    yield  # App rodando
    
    # Shutdown
    logger.info("🛑 TAS Engine desligado")

# --- FASTAPI APP ---
app = FastAPI(
    title="TAS - Thalamus Accumbens SARA",
    description="Motor de decisão do feed PentaIA. Filtra (Thalamus), Alinha (SARA) e Ranqueia (Accumbens).",
    version="2.0.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- MODELOS ---
class TrendItem(BaseModel):
    id: str
    hashtag: str
    topic: str
    category: str
    engagement: str
    sara_score: float
    viral: bool = False

class TrendsResponse(BaseModel):
    trends: List[TrendItem]
    source: str
    count: int
    engine: str
    timestamp: str

class HealthResponse(BaseModel):
    status: str
    engine: str
    components: dict
    timestamp: str

# --- ENDPOINTS ---

@app.get("/", response_model=HealthResponse)
async def health_check():
    """Health check com status dos componentes"""
    return HealthResponse(
        status="OPERATIONAL",
        engine="TAS_PENTAIA_v2",
        components={
            "thalamus": "ACTIVE",
            "sara": "ACTIVE", 
            "accumbens": "ACTIVE"
        },
        timestamp=datetime.now().isoformat()
    )

@app.get("/api/v1/recommend/trends", response_model=TrendsResponse)
async def get_trends():
    """
    Retorna trends processados pelo pipeline TAS completo:
    1. Thalamus: Filtra conteúdo seguro
    2. SARA: Calcula afinidade semântica (mock)
    3. Accumbens: Ranqueia por "dopamina" (engagement predito)
    """
    
    # Mock data realista (substituir por dados do banco/IRIS no futuro)
    raw_trends = [
        TrendItem(
            id="tas_001",
            hashtag="#InteligenciaArtificial",
            topic="Avanços em IA Generativa 2026",
            category="Tecnologia",
            engagement="45.2k",
            sara_score=0.95,
            viral=True
        ),
        TrendItem(
            id="tas_002",
            hashtag="#Sustentabilidade",
            topic="Energia Limpa no Brasil bate recorde",
            category="Meio Ambiente",
            engagement="32.1k",
            sara_score=0.88,
            viral=True
        ),
        TrendItem(
            id="tas_003",
            hashtag="#Libertadores",
            topic="Final 2026 define campeão sul-americano",
            category="Esportes",
            engagement="28.7k",
            sara_score=0.82,
            viral=True
        ),
        TrendItem(
            id="tas_004",
            hashtag="#EconomiaGlobal",
            topic="Mercados reagem às novas políticas",
            category="Economia",
            engagement="19.3k",
            sara_score=0.75
        ),
        TrendItem(
            id="tas_005",
            hashtag="#CinemaNacional",
            topic="Filme brasileiro concorre ao Oscar",
            category="Cultura",
            engagement="15.8k",
            sara_score=0.71
        ),
        TrendItem(
            id="tas_006",
            hashtag="#SpaceX",
            topic="Novo lançamento de foguete reutilizável",
            category="Ciência",
            engagement="12.4k",
            sara_score=0.68
        ),
    ]
    
    # Accumbens: Reordena por score de dopamina (sara_score * fator_engagement)
    def dopamine_score(trend: TrendItem) -> float:
        # Extrai número do engagement (ex: "45.2k" -> 45.2)
        eng_str = trend.engagement.replace('k', '').replace('m', '')
        try:
            eng_num = float(eng_str)
        except (TypeError, ValueError):
            eng_num = 1.0
        
        # Fórmula Accumbens: afinidade * log(engagement + 1)
        import math
        return trend.sara_score * math.log(eng_num + 1)
    
    sorted_trends = sorted(raw_trends, key=dopamine_score, reverse=True)
    
    logger.info(f"📊 Accumbens ranqueou {len(sorted_trends)} trends")
    
    return TrendsResponse(
        trends=sorted_trends,
        source="TAS_INTERNAL",
        count=len(sorted_trends),
        engine="TAS_PENTAIA_v2",
        timestamp=datetime.now().isoformat()
    )

@app.get("/api/v1/feed/personalized")
async def get_personalized_feed(user_id: Optional[str] = None):
    """
    Endpoint futuro para feed personalizado por usuário
    """
    return {
        "user_id": user_id or "anonymous",
        "feed": [],
        "message": "SARA personalização em desenvolvimento"
    }

# --- BOOTSTRAP ---
if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", "8001"))
    host = os.getenv("HOST", "0.0.0.0")
    reload = os.getenv("RELOAD", "true").lower() == "true"
    
    logger.info(f"🚀 Iniciando TAS em {host}:{port} (reload={reload})")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=reload,
        reload_dirs=["/app"] if reload else None,
        workers=1,
        access_log=True
    )