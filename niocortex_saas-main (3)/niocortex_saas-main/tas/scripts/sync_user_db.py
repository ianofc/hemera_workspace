import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.base import Base
import app.db.base_user # Força o carregamento do modelo de perfil
from app.db.session import engine

async def sync():
    print("⏳ [SUPABASE] Criando tabelas de Soberania do Utilizador...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ [SUPABASE] Tabelas de Utilizador integradas!")

if __name__ == "__main__":
    asyncio.run(sync())