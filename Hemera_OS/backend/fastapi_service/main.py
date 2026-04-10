from fastapi import FastAPI, Depends, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import logging

# Configuração de Logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ioconscius")

# --- IMPORTAÇÃO DOS LÓBULOS CEREBRAIS (ROUTERS) ---
# Certifique-se de que estes arquivos existem na pasta 'routers/'
from .routers import education, chat, proactive

app = FastAPI(
    title="IO CONSCIOS API",
    description="The Soul OS & Pedagogical Brain for NioCortex",
    version="2.1.0 (Full Brain Enabled)"
)

# --- CONFIGURAÇÃO DE SEGURANÇA (CORS) ---
# Permite que o Django (NioCortex) converse com o FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Em produção, restrinja para o domínio do Django
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- AUTENTICAÇÃO ENTRE SISTEMAS (SERVICE TOKEN) ---
async def verify_token(x_service_token: str = Header(...)):
    """
    Garante que apenas o NioCortex (que tem o segredo) possa acessar o Cérebro.
    """
    expected_token = os.getenv("SERVICE_TOKEN_SECRET", "dev-secret")
    if x_service_token != expected_token:
        logger.warning("Tentativa de acesso não autorizado ao IO CONSCIOS.")
        raise HTTPException(status_code=403, detail="Acesso negado ao Cérebro.")

# --- HEALTH CHECK (MONITORAMENTO) ---
@app.get("/")
def health_check():
    return {
        "status": "active", 
        "system": "IO CONSCIOS", 
        "modules": ["Education", "Chat", "Proactive"],
        "mode": os.getenv("APP_ENV", "guerrilla")
    }

# --- REGISTRO DOS LÓBULOS (COM PROTEÇÃO) ---

# 1. Módulo Educacional (Copiloto Pedagógico)
app.include_router(
    education.router, 
    dependencies=[Depends(verify_token)]
)

# 2. Módulo de Chat Universal (Agentes: Professor, Pai, Admin)
app.include_router(
    chat.router, 
    dependencies=[Depends(verify_token)]
)

# 3. Módulo Proativo (O Observador/Guardião)
app.include_router(
    proactive.router, 
    dependencies=[Depends(verify_token)]
)

if __name__ == "__main__":
    import uvicorn
    # Roda na porta 8001 para não conflitar com o Django (8000)
    # ou 8000 se estiver em container isolado via Docker
    port = int(os.getenv("PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port)