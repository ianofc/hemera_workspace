import os

SERVICE_NAME = "mercurio"
SERVICE_PORT = int(os.getenv("MERCURIO_PORT", "8004"))
REQUEST_TIMEOUT_DEFAULT = float(os.getenv("MERCURIO_TIMEOUT", "2.5"))

# Endpoints internos (docker-first com fallback local)
TAS_TRENDS_URL = os.getenv("TAS_TRENDS_URL", "http://tas:8001/api/v1/recommend/trends")
IRIS_SCAN_URL = os.getenv("IRIS_SCAN_URL", "http://iris:8003/scan/full")
HEIMDALL_CHECK_URL = os.getenv("HEIMDALL_CHECK_URL", "http://zios:8002/v1/proactive/heimdall/check")

# Política de priorização por origem
MERCURIO_WEIGHT_BIRD = int(os.getenv("MERCURIO_WEIGHT_BIRD", "3"))
MERCURIO_WEIGHT_RSS = int(os.getenv("MERCURIO_WEIGHT_RSS", "2"))
MERCURIO_WEIGHT_API = int(os.getenv("MERCURIO_WEIGHT_API", "1"))

# Resiliência
MERCURIO_BUNDLE_CACHE_TTL_S = int(os.getenv("MERCURIO_BUNDLE_CACHE_TTL_S", "90"))
MERCURIO_CIRCUIT_COOLDOWN_S = int(os.getenv("MERCURIO_CIRCUIT_COOLDOWN_S", "30"))
MERCURIO_CIRCUIT_FAILURE_LIMIT = int(os.getenv("MERCURIO_CIRCUIT_FAILURE_LIMIT", "2"))

# aliases de tópicos (formato: "ia:inteligencia-artificial,ai")
MERCURIO_TOPIC_ALIASES = os.getenv("MERCURIO_TOPIC_ALIASES", "")

# CORS
CORS_ALLOW_ORIGINS = [
    origin.strip()
    for origin in os.getenv(
        "MERCURIO_CORS_ALLOW_ORIGINS",
        "http://localhost:8080,http://127.0.0.1:8080",
    ).split(",")
    if origin.strip()
]
