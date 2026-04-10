import asyncio
import sys
import os

# Adiciona a raiz do projeto ao sys.path para evitar ModuleNotFoundError
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.base import Base
from app.db.session import engine

async def init_models():
    print("⏳ [SUPABASE] Criando tabelas...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ [SUPABASE] Tabelas sincronizadas com sucesso!")

if __name__ == "__main__":
    asyncio.run(init_models())