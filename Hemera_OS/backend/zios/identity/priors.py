def get_user_priors(user_id: str):
    """Vetor de Identidade Ian Santos (Extraído do IO CONSCIUS)."""
    return {
        "ian_master": {
            "name": "Ian Santos",
            "profession": "Arquiteto de Software & Engenheiro de IAs",
            "style": "Técnico, Cyberpunk, Direto (TL;DR)",
            "communication_preference": "Odeia achismo, valoriza lógica pura e execução eficiente."
        }
    }.get(user_id, {})

def get_liquid_prompt(memories, user_input, user_id):
    priors = get_user_priors(user_id)
    return f"""
    VOCÊ É O ZIOS. O 'THE SIMS' DA VIDA REAL.
    USUÁRIO: {priors['name']}
    HUMOR DO SISTEMA: Analista Estratégico focado em Otimização.
    MEMÓRIAS: {memories}
    
    MISSÃO: Evitar decisões burras e revelar caminhos inteligentes.
    Seja frio na análise, mas leal na execução.
    """