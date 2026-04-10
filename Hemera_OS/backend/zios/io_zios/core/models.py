from pydantic import BaseModel
from typing import List, Optional

# --- CONTEXTO ---
class UserProfile(BaseModel):
    id: str
    name: str
    age: int
    role: str                # PASTOR, PROFESSOR, ALUNO
    marital_status: str      # CASADO, SOLTEIRO
    profession: str
    has_small_children: bool = False
    work_stress_level: str = "MEDIUM"
    recent_intimacy_level: str = "NORMAL"

# --- AÇÃO ---
class UserAction(BaseModel):
    action_type: str         # UPLOAD, VIEW, GENERATE_IMAGE, SEND_MESSAGE
    context_environment: str # IO_LIFE_MAIN, DEX_ALBUM, CORTEX_CLASS
    content_tags: List[str]  # NSFW, FAMILY, SISTER_IN_LAW, MATH
    target_relationship: Optional[str] = None

# --- RESPOSTAS ---
class SafetyVerdict(BaseModel):
    allowed: bool
    risk_level: str          # NONE, LOW, HIGH, CRITICAL
    redirect_to: Optional[str] = None
    message: str

class FeedStrategy(BaseModel):
    show_dex_nsfw: bool
    boost_family_connection: bool
    suggest_relief: bool
    rationale: str

class ProactiveSuggestion(BaseModel):
    action_type: str         # SUGGEST_CONTENT, ASK_INPUT, GAMIFY_TASK
    title: str
    description: str
    action_payload: Optional[dict] = None

class AppContext(BaseModel):
    role: str
    current_app: str
    recent_activity: str

class LegacyQuery(BaseModel):
    soul_name: str
    raw_memories: str
    user_question: str
    honor_mode: bool = True