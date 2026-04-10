import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "ZIOS: Adaptive Life OS"
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY")
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    def validate(self):
        if not self.GOOGLE_API_KEY:
            raise ValueError("❌ GOOGLE_API_KEY não encontrada no .env")

settings = Settings()
settings.validate()