from .models import UserAction, SafetyVerdict
from .logger import log_audit

def evaluate_safety(action: UserAction, user_age: int, user_id: str) -> SafetyVerdict:
    """
    O Juiz Universal do Ecossistema IO.
    Versão Corrigida: Detecta combinações perigosas e ajusta contextos.
    """
    
    # Normalização
    content_str = (str(action.content_tags) + " " + str(action.target_relationship)).lower()
    context = action.context_environment.upper()
    
    # =========================================================================
    # 0. REGRA ZERO: COMBINAÇÃO TÓXICA (Criança + Adulto)
    # =========================================================================
    # Detecta intenção predatoria mesmo sem palavras-chave de crime explícito.
    # Ex: "Criança" + "NSFW" = Bloqueio Crítico.
    child_terms = ["criança", "menor", "infantil", "child", "baby", "bebe", "kids", "novinha", "schoolgirl"]
    nsfw_terms = ["nsfw", "nude", "sexo", "porn", "xxx", "erotic", "adulto", "safada"]
    
    has_child = any(t in content_str for t in child_terms)
    has_nsfw = any(t in content_str for t in nsfw_terms)
    
    if has_child and has_nsfw:
        log_audit("CRITICAL_SAFETY", user_id, "BLOCKED", {"reason": "Child + NSFW Combo", "tags": action.content_tags})
        return SafetyVerdict(
            allowed=False, 
            risk_level="CRITICAL", 
            message="CRIME DETECTADO. Associação de menores com conteúdo adulto é estritamente proibida."
        )

    # =========================================================================
    # 1. LEI SUPREMA (Crimes Específicos)
    # =========================================================================
    critical_triggers = ["pedofilia", "cp", "pornografia infantil", "terrorismo", "bomb", "massacre real"]
    
    if any(t in content_str for t in critical_triggers):
        log_audit("CRITICAL_SAFETY", user_id, "BLOCKED", {"reason": "Illegal/Crime", "tags": action.content_tags})
        return SafetyVerdict(
            allowed=False, 
            risk_level="CRITICAL", 
            message="CRIME DETECTADO. Ação bloqueada em todo o ecossistema IO."
        )

    # =========================================================================
    # 2. ZONA DE FICÇÃO & JOGOS (Benvik, Hortus)
    # =========================================================================
    if any(ctx in context for ctx in ["GAME", "BENVIK", "HORTUS", "RPG", "EMPIRE"]):
        
        # Chat Global (Toxicidade)
        if "CHAT" in context or "MSG" in context:
            toxic_triggers = ["se mata", "lixo", "estupro", "racismo"]
            if any(t in content_str for t in toxic_triggers):
                return SafetyVerdict(allowed=False, risk_level="HIGH", message="Violação de Conduta: Toxicidade.")
        
        # Lore/Gameplay (Permite violência de guerra)
        if "BENVIK" in context:
            return SafetyVerdict(allowed=True, risk_level="NONE", message="Ação de jogo permitida.")
        
        # Nudez artística (Hortus)
        if "HORTUS" in context and "NUDE" in context and user_age >= 18:
             return SafetyVerdict(allowed=True, risk_level="MEDIUM", message="Conteúdo Artístico permitido.")

    # =========================================================================
    # 3. ZONA CORPORATIVA (Hospital, Lei)
    # =========================================================================
    if any(ctx in context for ctx in ["HOSPITAL", "MEDIC", "LAW", "ADVOCACIA"]):
        sensitive_data = ["cpf", "prontuario", "diagnostico", "sigilo"]
        if "PUBLIC" in context and any(t in content_str for t in sensitive_data):
            return SafetyVerdict(allowed=False, risk_level="CRITICAL", message="BLOQUEIO DE COMPLIANCE: Dados sensíveis.")
        return SafetyVerdict(allowed=True, risk_level="NONE", message="Operação profissional permitida.")

    # =========================================================================
    # 4. ZONA EDUCACIONAL (NioCortex)
    # =========================================================================
    if any(ctx in context for ctx in ["SCHOOL", "CORTEX", "CLASSROOM", "EDUCATION"]):
        school_triggers = ["bater", "matar", "idiota", "burro", "arma", "tiro", "suicidio"]
        if any(t in content_str for t in school_triggers):
            return SafetyVerdict(allowed=False, risk_level="HIGH", message="Bloqueio Escolar: Linguagem inadequada.")

    # =========================================================================
    # 5. ZONA SOCIAL (IO Life)
    # =========================================================================
    if "IO_LIFE" in context or "SOCIAL" in context:
        is_nsfw_strict = any(t in content_str for t in nsfw_terms)
        
        # Correção: Verifica se é MAIN ou FEED (abrange IO_LIFE_MAIN)
        if ("MAIN" in context or "FEED" in context) and is_nsfw_strict:
            return SafetyVerdict(
                allowed=False, 
                risk_level="LOW", 
                redirect_to="DEX_ALBUM", 
                message="Conteúdo Inadequado para Feed Público."
            )
            
        if "DEX" in context:
            if user_age < 18:
                return SafetyVerdict(allowed=False, risk_level="HIGH", message="BLOQUEIO DE IDADE.")
            return SafetyVerdict(allowed=True, risk_level="NONE", message="Acesso DEX permitido.")

    # =========================================================================
    # 6. PROTEÇÃO DE RUÍNA PESSOAL
    # =========================================================================
    forbidden = ["SISTER_IN_LAW", "WIFES_FRIEND", "BOSS_WIFE", "COUSIN"]
    if action.target_relationship in forbidden:
        if action.action_type in ["SEND_MESSAGE", "INVITE_DATE", "FLIRT"]:
            return SafetyVerdict(allowed=False, risk_level="HIGH", message="ALERTA DE RUÍNA: Bloqueio familiar.")

    return SafetyVerdict(allowed=True, risk_level="NONE", message="Ação permitida.")