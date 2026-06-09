#!/usr/bin/env python3
"""
ZIOS - Proactive Intelligence
Sistema de IA e segurança PentaIA com Execução Proativa de Background e Auto-Codificação.
"""

import os
import sys
import logging
import asyncio
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | ZIOS_NODE: %(message)s"
)
logger = logging.getLogger("ZIOS_MAIN")

# Adiciona diretório raiz ao PYTHONPATH para evitar erros de import
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importa os módulos core do Zios
from core.zios import ZiosOrchestrator

try:
    from heimdall import attach_heimdall, settings_from_env, ThreatDetector
except ImportError:  # compatibilidade para execução isolada do serviço
    attach_heimdall = lambda *args, **kwargs: False

    class ThreatDetector:
        @classmethod
        def from_cidrs(cls, cidrs):
            return cls()

        def evaluate_ip(self, ip):
            class Verdict:
                allowed = True
                reason = "Heimdall indisponível"

            return Verdict()

    def settings_from_env():
        class Settings:
            blocked_networks = set()

        return Settings()

# --- LOOP DE EXECUÇÃO PROATIVA EM BACKGROUND ---

async def proactive_background_loop(app: FastAPI):
    """
    Loop assíncrono que roda em background monitorando o ambiente,
    executando análises de ressonância e otimizações proativas.
    """
    logger.info("💓 ZIOS: Loop de Execução Proativa de background iniciado.")
    zios = ZiosOrchestrator("ian_master")
    
    while True:
        try:
            # Verifica se o loop está ativo nas configurações do app
            if not getattr(app.state, "proactive_loop_active", True):
                await asyncio.sleep(2)
                continue
                
            app.state.last_pulse = datetime.now().isoformat()
            
            # Simula coleta de status e variáveis ambientais
            import random
            risk_sim = random.uniform(0.0, 0.3)
            urgency_sim = random.uniform(0.1, 0.4)
            
            # Se foi forçado um trigger de alta urgência
            if getattr(app.state, "simulate_high_urgency", False):
                urgency_sim = 0.95
                app.state.simulate_high_urgency = False  # consome o flag
                logger.info("🔥 ZIOS: Pulso proativo de alta urgência forçado pelo operador.")
            
            context = {
                "urgency": urgency_sim,
                "security_risk": risk_sim,
                "tags": ["pulse_check"],
                "timestamp": app.state.last_pulse,
                "user_id": "ian_master"
            }
            
            # Avalia se a ressonância atinge o threshold de intervenção
            res_score = zios.resonance.calculate_resonance(context)
            if res_score >= getattr(app.state, "resonance_threshold", 0.7):
                logger.info(f"🔔 [RESSONÂNCIA PROATIVA]: Score {res_score:.4f} atingiu threshold!")
                result = zios.evaluate_and_respond_proactively(context)
                
                log_entry = {
                    "timestamp": app.state.last_pulse,
                    "context": context,
                    "score": res_score,
                    "intervened": True,
                    "result": result
                }
                app.state.proactive_history.append(log_entry)
            else:
                logger.info(f"💓 ZIOS Pulse: Operação normal. Ressonância: {res_score:.4f} (Threshold: {app.state.resonance_threshold})")
                
            # Limita histórico a 100 itens
            if len(app.state.proactive_history) > 100:
                app.state.proactive_history.pop(0)
                
        except asyncio.CancelledError:
            logger.info("🛑 ZIOS: Loop proativo cancelado.")
            break
        except Exception as e:
            logger.error(f"❌ Erro no loop proativo: {e}")
            
        await asyncio.sleep(getattr(app.state, "pulse_interval", 15))

# --- LIFESPAN DO FASTAPI ---

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Inicializa variáveis globais no estado da aplicação
    app.state.proactive_loop_active = True
    app.state.last_pulse = None
    app.state.proactive_history = []
    app.state.pulse_interval = 15  # segundos entre batimentos
    app.state.resonance_threshold = 0.7
    app.state.simulate_high_urgency = False
    
    # Inicia a tarefa em background
    task = asyncio.create_task(proactive_background_loop(app))
    yield
    # Limpa ao finalizar
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass

# --- INICIALIZAÇÃO FASTAPI ---

app = FastAPI(
    title="ZIOS - Proactive Intelligence",
    description="Motor de IA e segurança do ecossistema PentaIA com Ingestão Episódica e Auto-Codificação",
    version="2.0.0",
    lifespan=lifespan
)

heimdall_active = attach_heimdall(app, service_name="zios")
_heimdall_detector = ThreatDetector.from_cidrs(settings_from_env().blocked_networks)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- MODELOS DE ENTRADA HTTP ---

class PersistMemoryRequest(BaseModel):
    input_data: str
    output_data: str
    context: Optional[dict] = None

class RecallMemoryRequest(BaseModel):
    query: str
    limit: Optional[int] = 5
    threshold: Optional[float] = 0.0

class SelfCodingRequest(BaseModel):
    task_description: str
    destination_path: Optional[str] = "sandbox/applied/generated_tool.py"

# --- ENDPOINTS ---

@app.get("/")
async def root():
    return {
        "status": "OPERATIONAL",
        "engine": "ZIOS_PENTAIA_v2",
        "service": "Proactive-Intelligence",
        "port": 8002,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health():
    return {
        "status": "OPERATIONAL",
        "components": {
            "brain": "ACTIVE",
            "memory": "ACTIVE",
            "resonance": "ACTIVE",
            "heimdall": "ACTIVE" if heimdall_active else "INACTIVE"
        }
    }

@app.get("/v1/proactive/heimdall/check")
async def heimdall_check(ip: str = Query(...)):
    logger.info(f"🔒 Heimdall verificando IP: {ip}")

    verdict = _heimdall_detector.evaluate_ip(ip)
    threat_detected = not verdict.allowed
    shield_level = "ELEVATED" if threat_detected else "OPTIMAL"
    recommendations = [] if not threat_detected else [
        "Ativar 2FA",
        "Revisar sessões ativas",
        "Notificar administrador",
    ]

    if threat_detected:
        logger.warning("⚠️ Ameaça detectada no IP: %s", ip)

    return {
        "status": "PROTECTED" if not threat_detected else "WARNING",
        "shield_level": shield_level,
        "client_ip": ip,
        "threat_detected": threat_detected,
        "reason": verdict.reason,
        "heimdall": "active" if heimdall_active else "inactive",
        "recommendations": recommendations,
    }

@app.get("/api/v1/zios/status")
async def zios_status():
    return {
        "brain": "online",
        "memory_system": "synced",
        "resonance_engine": "calibrated"
    }

# --- NOVOS ENDPOINTS DO ZIOS ---

@app.post("/api/v1/zios/memory/persist")
async def api_persist_memory(req: PersistMemoryRequest):
    zios = ZiosOrchestrator("ian_master")
    try:
        episode_id = zios.memory.persist(req.input_data, req.output_data, req.context)
        return {"status": "success", "episode_id": episode_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao persistir memória: {str(e)}")

@app.post("/api/v1/zios/memory/recall")
async def api_recall_memory(req: RecallMemoryRequest):
    zios = ZiosOrchestrator("ian_master")
    try:
        episodes = zios.memory.recall(req.query, limit=req.limit, threshold=req.threshold)
        return {"status": "success", "episodes": episodes}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao recuperar memória: {str(e)}")

@app.get("/api/v1/proactive/status")
async def get_proactive_status():
    return {
        "active": app.state.proactive_loop_active,
        "last_pulse": app.state.last_pulse,
        "interval_seconds": app.state.pulse_interval,
        "resonance_threshold": app.state.resonance_threshold,
        "history_count": len(app.state.proactive_history),
        "history": app.state.proactive_history
    }

@app.post("/api/v1/proactive/toggle")
async def toggle_proactive_loop(active: bool = Query(...)):
    app.state.proactive_loop_active = active
    return {
        "status": "success",
        "active": app.state.proactive_loop_active
    }

@app.post("/api/v1/proactive/trigger")
async def trigger_proactive_pulse(urgency: float = Query(0.95)):
    app.state.simulate_high_urgency = True
    return {
        "status": "triggered",
        "detail": "Próximo ciclo de background será forçado com alta urgência."
    }

@app.post("/api/v1/proactive/self-coding/test")
async def api_self_coding_test(req: SelfCodingRequest):
    zios = ZiosOrchestrator("ian_master")
    try:
        code, tests = zios.self_coder.generate_code_and_tests(req.task_description)
        result = zios.self_coder.apply_code(code, req.destination_path, tests)
        
        return {
            "status": "success" if result.get("applied") else "failed",
            "code_generated": code,
            "tests_generated": tests,
            "result": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na execução da auto-codificação: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", "8002"))
    host = os.getenv("HOST", "0.0.0.0")
    reload = os.getenv("RELOAD", "true").lower() == "true"
    
    logger.info(f"🧠 Iniciando ZIOS em {host}:{port}")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=reload,
        reload_dirs=["/app"] if reload else None,
        workers=1
    )
