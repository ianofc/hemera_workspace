import threading
import requests
import os
import logging
import json

logger = logging.getLogger(__name__)

class PentaIAClient:
    """
    Cliente interno para se comunicar com o motor de inteligência PentaIA (FastAPI).
    Comunicação feita em background thread para não bloquear a UI do Django.
    """
    def __init__(self):
        # A API roda na porta 8001 da rede local (ou host do docker)
        self.base_url = os.environ.get("PENTAIA_SERVICE_URL", "http://pentaia:8001")
        self.service_token = os.environ.get("SERVICE_TOKEN_SECRET", "dev-secret")

    def _post_async(self, endpoint: str, payload: dict):
        url = f"{self.base_url}{endpoint}"
        headers = {
            "Content-Type": "application/json",
            "x-service-token": self.service_token
        }
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=5)
            response.raise_for_status()
            logger.info(f"[PentaIAClient] Success: {endpoint} | Status: {response.status_code}")
        except Exception as e:
            logger.error(f"[PentaIAClient] Failed to reach PentaIA locally at {url}. Error: {str(e)}")

    def send_event_background(self, endpoint: str, payload: dict):
        """
        Gera uma thread background (fire and forget) para enviar o payload.
        """
        thread = threading.Thread(target=self._post_async, args=(endpoint, payload,))
        thread.start()

    def analyze_performance(self, aluno_id: int, turma_id: int, evento_detalhes: dict):
        """
        Ativa o agente TAS via Webhook para analisar flutuações nas Notas ou Frequências.
        """
        payload = {
            "aluno_id": aluno_id,
            "turma_id": turma_id,
            "evento": evento_detalhes  # ex: {"tipo": "nota", "valor": 4.5, "atividade_id": 12}
        }
        self.send_event_background("/proactive/analyze-performance", payload)

# Instância Singleton exportada
pentaia = PentaIAClient()
