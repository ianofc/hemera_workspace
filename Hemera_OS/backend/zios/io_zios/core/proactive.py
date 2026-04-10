from .models import AppContext, ProactiveSuggestion

def generate_proactive_action(context: AppContext) -> ProactiveSuggestion:
    if context.role == "PASTOR" and context.current_app == "IO_LIFE":
        return ProactiveSuggestion(
            action_type="SUGGEST_CONTENT",
            title="Inspiração para Sermão",
            description="Domingo chegando. Análise teológica disponível.",
            action_payload={"tool": "Sermon_Builder"}
        )
            
    if context.role == "PROFESSOR" and "PLANNING" in context.current_app:
        return ProactiveSuggestion(
            action_type="ASK_INPUT",
            title="Assistente de Aula",
            description="Para qual turma vamos planejar hoje?",
            action_payload={"fields": ["turma", "tema"]}
        )

    if context.role == "ALUNO" and "Python" in context.recent_activity:
        return ProactiveSuggestion(
            action_type="GAMIFY_TASK",
            title="Desafio de Código",
            description="Resolver desafio valendo 50 XP?",
            action_payload={"challenge_id": "PYTHON_01"}
        )

    return ProactiveSuggestion(action_type="NONE", title="", description="")