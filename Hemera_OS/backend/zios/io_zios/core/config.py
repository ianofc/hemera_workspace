import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "IO CONSCIOS (Guerrilla Edition)"
    VERSION: str = "2.0.0"
    APP_ENV: str = os.getenv("APP_ENV", "local")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    SERVICE_TOKEN: str = os.getenv("SERVICE_TOKEN_SECRET", "changeme")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./zios_brain.db")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

settings = Settings()