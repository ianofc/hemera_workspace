class AccumbensRanker:
    """
    Juiz Final: Decide a ordem baseada em probabilidade de engajamento.
    Pesos: Share > Comment > Like > Click
    """
    def __init__(self):
        self.weights = {
            "share": 10.0,
            "comment": 5.0,
            "like": 2.0,
            "click": 1.0
        }

    async def rank(self, candidates):
        for c in candidates:
            # Cálculo de score baseado em comportamento (simulado por enquanto)
            engagement_score = (
                c.get("predicted_shares", 0) * self.weights["share"] +
                c.get("predicted_likes", 0) * self.weights["like"]
            )
            # Soma a afinidade da SARA (0 a 1) multiplicada por um fator de peso
            c["final_score"] = (c.get("sara_score", 0.5) * 50) + engagement_score
            
        return [str(c["id"]) for c in sorted(candidates, key=lambda x: x["final_score"], reverse=True)]

accumbens_ranker = AccumbensRanker()