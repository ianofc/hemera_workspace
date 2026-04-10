from sqlalchemy.future import select
from app.db.base import ContentModel
import traceback

class ContentRepository:
    def __init__(self, db_session):
        self.db = db_session

    async def add_content(self, content_data: dict):
        try:
            content = ContentModel(**content_data)
            self.db.add(content)
            await self.db.commit()
            return content
        except Exception as e:
            print(f"❌ [DB ERROR] Falha ao inserir: {e}")
            traceback.print_exc()
            raise e

    async def get_candidates(self, limit=500):
        result = await self.db.execute(select(ContentModel).limit(limit))
        return result.scalars().all()