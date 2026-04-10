# iris/main.py

from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from core.sattr_logic import SATTR
import uvicorn
import logging
from datetime import datetime

# --- CONFIGURAÇÃO DE LOGGING DE ALTA DISPONIBILIDADE ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | IRIS_NODE: %(message)s"
)
logger = logging.getLogger("IRIS_MAIN")

# --- INSTANCIAÇÃO DO CORE SATTR ---
# Inicializamos aqui para persistência de memória do motor pytrends
sattr_engine = SATTR()

# --- DEFINIÇÃO DA APP COM METADADOS DE SÉCULO XXII ---
app = FastAPI(
    title="IRIS OMEGA - Neural Vision Interface",
    description="Portal de entrada do sistema SATTR (Systemic Algorithm for Real-time Trends & Resonance). Responsável pela varredura espectral de dados globais e intenção de busca.",
    version="2.0.1",
    contact={
        "name": "PentaIA Engineering Hub",
        "url": "http://pentaia.internal",
    }
)

# --- MIDDLEWARE: SEGURANÇA E FLUXO ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # No ecossistema interno, permitimos crosstalk total
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Diagnostic"])
async def health_check():
    """
    Retorna o status vital do Nó de Visão IRIS.
    Verifica se o motor SATTR está carregado e pronto para varredura.
    """
    return {
        "node_id": "IRIS-OMEGA-UNIT-01",
        "service": "IRIS",
        "status": "OPERATIONAL",
        "mode": "REALTIME_SPECTRAL_SCAN",
        "timestamp": datetime.now().isoformat(),
        "engine_ready": sattr_engine is not None
    }

@app.get("/scan/full", tags=["Intelligence"])
async def perform_full_spectrum_scan(response: Response):
    """
    Executa a varredura completa multicamada (Pytrends + RSS).
    Retorna o bundle de tendências ordenado por momentum gravitacional.
    """
    try:
        logger.info("Solicitação de varredura profunda recebida.")
        
        # Executa o algoritmo Iris-Omega
        scan_data = sattr_engine.perform_scan()
        
        # Adicionamos um Header customizado para o Mercúrio identificar a versão do motor
        response.headers["X-PentaIA-Engine"] = scan_data.get("engine_version", "unknown")
        
        if scan_data.get("status") == "waiting_pulse":
            logger.warning("Varredura concluída com dados de fallback (Modo de Espera).")
        else:
            logger.info(f"Varredura concluída. {len(scan_data.get('google_trends', []))} tendências filtradas.")

        return scan_data

    except Exception as e:
        logger.critical(f"Falha Crítica na Interface de Visão: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Neural Vision Disruption",
                "message": "Ocorreu uma falha na ressonância dos dados durante a varredura profunda.",
                "remedy": "Verifique a conectividade do nó IRIS com os serviços externos."
            }
        )

# --- BOOTSTRAP DO SISTEMA ---
if __name__ == "__main__":
    # Rodando na porta 8003 conforme arquitetura PentaIA
    logger.info("Iniciando Nó IRIS OMEGA na porta 8003...")
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8003, 
        reload=True, 
        reload_dirs=["/app"],  # Limita watch
        reload_includes=["*.py"],
        workers=1,
        access_log=True
    )