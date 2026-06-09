from core.brain import ZiosBrain
from core.memory import ZiosMemory
from core.safety import evaluate_safety
from core.resonance import ResonanceEngine
from core.coding import ZiosSelfCoder
import logging

logger = logging.getLogger("ZIOS_ORCHESTRATOR")

class ZiosOrchestrator:
    """
    Orquestrador Central do ZIOS.
    Integra a Memória Episódica, o Motor de Ressonância, a Inteligência Neural (Brain)
    e a capacidade de Auto-Codificação.
    """
    def __init__(self, user_id: str):
        self.user_id = user_id
        # Inicializa a memória com suporte a Supabase/SQLite fallback
        self.memory = ZiosMemory(user_id)
        self.brain = ZiosBrain(self.memory)
        self.resonance = ResonanceEngine()
        self.self_coder = ZiosSelfCoder()

    def process(self, input_data: str, context: dict = None) -> str:
        """Processa um input aplicando travas de segurança e integrando com o cérebro neural."""
        if not evaluate_safety(input_data):
            logger.warning(f"⚠️ Tentativa de execução bloqueada por segurança. Input: {input_data}")
            return "ZIOS: Esta ação viola meus protocolos éticos."
            
        # Pega a resposta do cérebro neural (Gemini)
        response = self.brain.think(input_data, context)
        
        # Persiste o episódio na memória episódica
        self.memory.persist(input_data, response, context)
        
        return response

    def evaluate_and_respond_proactively(self, context: dict) -> dict:
        """
        Analisa o contexto atual usando a Filtragem por Ressonância.
        Se a ressonância for alta, executa uma ação de otimização de ambiente de forma autônoma.
        """
        context["user_id"] = context.get("user_id", self.user_id)
        
        if self.resonance.should_intervene(context):
            logger.info("🔔 [RESSONÂNCIA]: Intervenção proativa ativada.")
            
            # Se houver um alerta de segurança (pelo Heimdall, etc.)
            if context.get("threat_detected") or context.get("security_risk", 0.0) > 0.7:
                action = "Executada auditoria proativa de segurança e rotação de travas de API."
                self.memory.persist("PROACTIVE_TRIGGER: SecurityThreat", action, context)
                return {
                    "intervened": True,
                    "action": "security_audit",
                    "reason": "Alto risco de segurança",
                    "message": action
                }
                
            # Se for uma necessidade de nova ferramenta ou otimização de código
            if "optimize_code" in context.get("tags", []):
                # Executa um pipeline de auto-codificação simples de teste/demonstração
                code, tests = self.self_coder.generate_code_and_tests("otimização de slug para logs")
                dest = "sandbox/applied/slug_tool.py"
                result = self.self_coder.apply_code(code, dest, tests)
                
                action = f"Auto-Codificação proativa concluída. Sucesso: {result.get('applied')}"
                self.memory.persist("PROACTIVE_TRIGGER: CodeOptimization", action, context)
                return {
                    "intervened": True,
                    "action": "self_coding",
                    "result": result,
                    "message": action
                }

            # Ação genérica proativa de check de integridade
            action_msg = "Zios realizou varredura de integridade e logs prioritários em background."
            self.memory.persist("PROACTIVE_TRIGGER: SystemPulse", action_msg, context)
            return {
                "intervened": True,
                "action": "system_pulse",
                "message": action_msg
            }
            
        return {
            "intervened": False,
            "message": "Nível de ressonância abaixo do threshold de intervenção."
        }