import logging
import sys
# Tenta importar da nova localização, se falhar, usa a antiga
try:
    from pythonjsonlogger.json import JsonFormatter
except ImportError:
    from pythonjsonlogger.jsonlogger import JsonFormatter

from core.config import settings

logger = logging.getLogger("io_zios")
handler = logging.StreamHandler(sys.stdout)

# Formato JSON limpo
formatter = JsonFormatter('%(asctime)s %(levelname)s %(message)s %(module)s')
handler.setFormatter(formatter)

logger.addHandler(handler)
logger.setLevel(settings.LOG_LEVEL)

def log_audit(event_type, user_id, verdict, metadata=None):
    logger.info("AUDIT", extra={
        "event_type": event_type,
        "user_id": user_id,
        "verdict": verdict,
        "meta": metadata or {}
    })