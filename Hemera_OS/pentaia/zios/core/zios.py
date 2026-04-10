from core.brain import ZiosBrain
from core.memory import ZiosMemory
from core.safety import evaluate_safety
from core.resonance import ResonanceEngine

class ZiosOrchestrator:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.memory = ZiosMemory(user_id)
        self.brain = ZiosBrain(self.memory)
        self.resonance = ResonanceEngine()

    def process(self, input_data: str, context: dict = None):
        if not evaluate_safety(input_data):
            return "ZIOS: Esta ação viola meus protocolos éticos."
        return self.brain.think(input_data, context)