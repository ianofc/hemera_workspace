#!/usr/bin/env python3
"""
TAS - Thalamus Accumbens SARA System
Entry point oficial unificado da PentaIA.
"""

import os
import sys
import logging
from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import text

# Garante que o diretório raiz esteja no PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

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
    logger.info("🚀 [TAS ORCHESTRATOR] Iniciando motor PentaIA...")
    
    # 1. Conecta os handlers de eventos do Talamus ao Accumbens RL
    from app.engines.accumbens.rl import process_feedback_event
    from app.engines.thalamus.queue import talamus_queue
    talamus_queue.register_handler(process_feedback_event)
    
    # 2. Inicializa a fila assíncrona do Talamus (RabbitMQ/Kafka/MemoryFallback)
    await talamus_queue.start()
    
    # 3. Inicializa o daemon de Vigília e Monitoramento da SARA
    from app.engines.sara.vigilance import sara_vigilance
    await sara_vigilance.start()
    
    # 4. Inicialização do Banco (opcional/resiliente)
    try:
        from app.db.session import engine
        # Verifica conexão rápida
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        logger.info("🗄️ Conexão resiliente com o Postgres/Supabase ativa.")
    except Exception as e:
        logger.warning(f"⚠️ Banco em modo fallback: {e}")
    
    logger.info("🔥 TAS Engine pronto e operacional.")
    yield  # App rodando
    
    # Shutdown elegante
    logger.info("🛑 Desligando componentes do TAS...")
    await talamus_queue.stop()
    await sara_vigilance.stop()
    logger.info("🛑 TAS Engine desligado com sucesso.")

# --- FASTAPI APP ---
app = FastAPI(
    title="TAS - Thalamus Accumbens SARA",
    description="Motor de decisão do feed PentaIA. Filtra (Thalamus), Alinha (SARA) e Ranqueia (Accumbens).",
    version="2.2.0",
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

# Inclui os roteadores da API real
from app.api.v1.api import api_router
app.include_router(api_router, prefix="/api/v1")

# --- HEALTH & SARA STATUS ---

@app.get("/")
async def health_check():
    """Health check consolidado com dados de monitoramento da SARA"""
    from app.engines.sara.vigilance import sara_vigilance
    status_sara = sara_vigilance.get_status()
    
    return {
        "status": "OPERATIONAL",
        "engine": "TAS_PENTAIA_v2.2.0",
        "timestamp": datetime.utcnow().isoformat(),
        "sara_vigilance": status_sara,
        "components": {
            "thalamus": "ACTIVE",
            "sara": "ACTIVE", 
            "accumbens": "ACTIVE"
        }
    }

@app.get("/api/v1/sara/status")
async def get_sara_status():
    """Retorna estatísticas detalhadas de orquestração de recursos da SARA"""
    from app.engines.sara.vigilance import sara_vigilance
    return sara_vigilance.get_status()

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