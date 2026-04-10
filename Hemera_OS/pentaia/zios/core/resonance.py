class ResonanceEngine:
    """Motor de Proatividade (The Sims Logic)."""
    def should_intervene(self, context):
        return context.get("urgency", 0) > 0.8