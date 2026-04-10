#!/usr/bin/env python3
"""
ZIOS - Proactive Intelligence
Sistema de IA e segurança PentaIA
"""

import os
import sys
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | ZIOS_NODE: %(message)s"
)
logger = logging.getLogger("ZIOS_MAIN")

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
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

app = FastAPI(
    title="ZIOS - Proactive Intelligence",
    description="Motor de IA e segurança do ecossistema PentaIA",
    version="2.0.0"
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
