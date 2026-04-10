import requests
import logging
from .config import IRIS_URL

logger = logging.getLogger("mercurio")

class IrisBridge:
    def get_trends(self):
        try:
            logger.info(f"Contactando Iris em: {IRIS_URL}")
            response = requests.get(f"{IRIS_URL}/scan/full", timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Iris retornou erro: {response.status_code}")
                return None
        except Exception as e:
            logger.error(f"Falha ao conectar com Iris: {e}")
            return None