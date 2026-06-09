from typing import List, Dict, Any
from app.engines.accumbens.rl import accumbens_rl

class AccumbensRanker:
    """
    Juiz Final: Decide a ordem baseada em probabilidade de engajamento e preferências do RL.
    Pesos: Share > Comment > Like > Click
    """
    def __init__(self):
        self.weights = {
            "share": 12.0,
            "comment": 6.0,
            "like": 3.0,
            "click": 1.0,
            "boredom_penalty": -5.0
        }

    async def rank(self, candidates: List[Dict[str, Any]], user_id: str = None, user_profile: Dict[str, Any] = None) -> List[str]:
        # Carrega interesses do usuário do perfil (banco) ou do cache em memória do RL
        user_interests = {}
        if user_profile and isinstance(user_profile, dict):
            user_interests = user_profile.get("priority_interests") or {}
        
        # Se os interesses não vieram no perfil ou o perfil é vazio, tenta ler do fallback do Accumbens RL
        if not user_interests and user_id:
            user_interests = accumbens_rl.get_fallback_interests(user_id)

        # Garante que seja um dicionário
        if not isinstance(user_interests, dict):
            user_interests = {}

        for c in candidates:
            # 1. Cálculo de score baseado em comportamento histórico/predito
            engagement_score = (
                c.get("predicted_shares", 0) * self.weights["share"] +
                c.get("predicted_comments", 0) * self.weights["comment"] +
                c.get("predicted_likes", 0) * self.weights["like"] +
                c.get("predicted_clicks", 0) * self.weights["click"]
            )
            
            # 2. Impulsionamento de preferência pessoal baseada em RL
            profile_boost = 0.0
            candidate_tags = c.get("tags") or []
            for tag in candidate_tags:
                tag_clean = str(tag).strip().lower()
                profile_boost += user_interests.get(tag_clean, 0.0)

            # 3. Penalidade por visualizações excessivas sem clique (tédio)
            boredom = float(c.get("boredom_count", 0) * self.weights["boredom_penalty"])

            # 4. Score SARA (Afinidade Semântica) - escala de 0 a 1 -> peso 50
            sara_score = float(c.get("sara_score", 0.5))

            # Fórmula Accumbens: SARA + Engagement + Personal RL Boost + Boredom
            c["final_score"] = (sara_score * 50) + engagement_score + (profile_boost * 5.0) + boredom

        # Ordena candidatos por final_score de forma decrescente
        sorted_candidates = sorted(candidates, key=lambda x: x.get("final_score", 0.0), reverse=True)
        return [str(c["id"]) for c in sorted_candidates]

accumbens_ranker = AccumbensRanker()