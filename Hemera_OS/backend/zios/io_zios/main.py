import os
import logging
import uvicorn
from fastapi import FastAPI, Depends, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

# --- Imports do Core Original (Lógica de Negócio) ---
from core.models import (
    UserAction, UserProfile, SafetyVerdict, FeedStrategy, 
    LegacyQuery, AppContext, ProactiveSuggestion
)
from core.safety import evaluate_safety
from core.behavior import analyze_hydraulic_pressure
from core.proactive import generate_proactive_action
from core.legacy import prepare_legacy_prompt
from core.brain import consult_gemini
from core.auth import verify_service_token
from core.validators import sanitize_input
from core.logger import logger

# --- Imports de Banco de Dados ---
from db.database import engine, Base, get_db
from db.tables import AuditLog

# --- Importação dos Novos Routers (Módulos NioCortex) ---
# O try/except garante que o servidor suba mesmo se você ainda não criou os arquivos na pasta 'routers'
education = None
chat = None
proactive_router = None

try:
    from routers import education, chat
    # Tenta importar um router 'proactive' específico de rotas, se existir, 
    # para não confundir com o core.proactive (lógica)
    try:
        from routers import proactive as proactive_router
    except ImportError:
        pass
except ImportError as e:
    logger.warning(f"Novos routers não encontrados completamente: {e}. Rodando com funcionalidades limitadas.")

# Inicializa Banco de Dados
Base.metadata.create_all(bind=engine)

# Configuração da Aplicação
app = FastAPI(
    title="IO CONSCIOS API",
    description="The Soul OS & Pedagogical Brain for NioCortex",
    version="2.2.0 (Unified Brain)"
)

# CORS (Permitir acesso do NioCortex/Django)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Em produção, troque "*" pelo domínio do seu NioCortex
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- ENDPOINTS GERAIS ---

@app.get("/")
def health_check():
    active_modules = ["Safety", "Behavior", "Legacy"]
    if education: active_modules.append("Education")
    if chat: active_modules.append("Universal Chat")
    
    return {
        "status": "ONLINE", 
        "mode": "Guerrilla Tech", 
        "interface": "Headless API",
        "version": "2.2.0",
        "modules_active": active_modules
    }

# --- ENDPOINTS ORIGINAIS (Core Cognitivo) ---

# 1. O JUIZ (Safety)
@app.post("/v1/judge/action", response_model=SafetyVerdict)
async def judge_action(
    action: UserAction, 
    user_age: int, 
    user_id: str, 
    db: Session = Depends(get_db),
    auth=Depends(verify_service_token)
):
    """ Avalia segurança de uma ação específica. """
    action.target_relationship = sanitize_input(action.target_relationship)
    verdict = evaluate_safety(action, user_age, user_id)
    
    # Log de Auditoria
    log_entry = AuditLog(
        user_id=user_id,
        action_type=action.action_type,
        verdict="ALLOWED" if verdict.allowed else "BLOCKED",
        details=verdict.dict()
    )
    db.add(log_entry)
    db.commit()
    
    return verdict

# 2. O PSICÓLOGO (Behavior)
@app.post("/v1/feed/strategy", response_model=FeedStrategy)
async def get_feed_strategy(user: UserProfile, auth=Depends(verify_service_token)):
    """ Define estratégia de feed baseada na pressão psicológica. """
    return analyze_hydraulic_pressure(user)

# 3. O GUARDIÃO LEGADO (Proactive Original)
# Mantido para compatibilidade com sistemas antigos que chamam este endpoint direto
@app.post("/v1/proactive/suggest", response_model=ProactiveSuggestion)
async def get_suggestion(context: AppContext, auth=Depends(verify_service_token)):
    """ Gera sugestão de ação baseada no contexto do app. """
    return generate_proactive_action(context)

# 4. O SÁBIO (Legacy)
@app.post("/v1/legacy/consult")
async def consult_legacy(query: LegacyQuery, auth=Depends(verify_service_token)):
    """ Consulta memórias antigas com filtro de honra. """
    query.user_question = sanitize_input(query.user_question)
    prompt = prepare_legacy_prompt(query.soul_name, query.raw_memories, query.honor_mode)
    response = consult_gemini(prompt, query.user_question)
    return {"response": response}

# 5. CHAT SIMPLES (Legado)
# Renomeado para não conflitar com o Chat Universal Inteligente
@app.post("/v1/chat/simple_interact")
async def chat_interaction_legacy(user_input: str, persona: str = "MENTOR", auth=Depends(verify_service_token)):
    user_input = sanitize_input(user_input)
    prompt = f"Atue como um {persona}. Responda de forma sábia e direta."
    response = consult_gemini(prompt, user_input)
    return {"response": response}

# --- REGISTRO DOS NOVOS MÓDULOS (Routers NioCortex) ---

if education:
    app.include_router(education.router, dependencies=[Depends(verify_service_token)])

if chat:
    # O Chat Universal (v1/chat/interact) assume o protagonismo aqui
    app.include_router(chat.router, dependencies=[Depends(verify_service_token)])

if proactive_router:
    # Se houver um router proativo mais avançado (observador), ele é registrado
    app.include_router(proactive_router.router, dependencies=[Depends(verify_service_token)])


if __name__ == "__main__":
    # Porta definida por variável de ambiente ou padrão 8001
    port = int(os.getenv("PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port)