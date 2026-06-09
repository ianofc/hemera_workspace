import logging

logger = logging.getLogger("ZIOS_RESONANCE")

class ResonanceEngine:
    """
    Motor de Ressonância do ZIOS.
    Prioriza o foco e decide intervenções autônomas com base em pesos de relevância do contexto.
    Pondera fatores como urgência, recência temporal, relevância semântica para o usuário e impacto/segurança.
    """
    def __init__(self, weights: dict = None):
        # Pesos padrão para cálculo de ressonância (a soma deve ser 1.0)
        self.weights = weights or {
            "urgency": 0.35,          # Urgência operacional imediata
            "user_relevance": 0.25,   # Alinhamento com a identidade/priors do Ian
            "impact": 0.20,           # Impacto potencial na estabilidade do OS
            "security_risk": 0.20     # Severidade de anomalias/ameaças
        }
        
    def calculate_resonance(self, context: dict) -> float:
        """Calcula um score de ressonância entre 0.0 e 1.0 para o contexto."""
        if not context:
            return 0.0
            
        score = 0.0
        
        # 1. Urgência
        urgency = float(context.get("urgency", 0.0))
        score += urgency * self.weights.get("urgency", 0.35)
        
        # 2. Relevância para o Usuário (ex: priors do Ian Santos)
        user_relevance = float(context.get("user_relevance", 0.0))
        # Se for um trigger do próprio Ian ou tiver tags importantes, sobe relevância
        if context.get("user_id") == "ian_master" or context.get("is_master_trigger"):
            user_relevance = max(user_relevance, 1.0)
        score += user_relevance * self.weights.get("user_relevance", 0.25)
        
        # 3. Impacto Operacional
        impact = float(context.get("impact", 0.0))
        score += impact * self.weights.get("impact", 0.20)
        
        # 4. Risco de Segurança
        security_risk = float(context.get("security_risk", 0.0))
        if context.get("threat_detected") or context.get("shield_level") == "ELEVATED":
            security_risk = max(security_risk, 0.9)
        score += security_risk * self.weights.get("security_risk", 0.20)
        
        # Garante que o score final fique no intervalo [0.0, 1.0]
        return min(max(score, 0.0), 1.0)

    def should_intervene(self, context: dict, threshold: float = 0.7) -> bool:
        """Decide se o ZIOS deve agir proativamente com base no threshold de ressonância."""
        score = self.calculate_resonance(context)
        context["computed_resonance"] = score
        logger.info(f"📊 Ressonância calculada: {score:.4f} (Threshold: {threshold})")
        return score >= threshold

    def prioritize_contexts(self, contexts: list, threshold: float = 0.5) -> list:
        """
        Recebe uma lista de contextos, calcula seus scores de ressonância,
        filtra os que estão acima do threshold e os ordena do mais ressonante para o menos.
        """
        prioritized = []
        for ctx in contexts:
            score = self.calculate_resonance(ctx)
            # Cria uma cópia para não alterar o dicionário original destrutivamente
            ctx_copy = ctx.copy()
            ctx_copy["resonance_score"] = score
            if score >= threshold:
                prioritized.append(ctx_copy)
                
        # Ordena por score decrescente
        prioritized.sort(key=lambda x: x["resonance_score"], reverse=True)
        return prioritized