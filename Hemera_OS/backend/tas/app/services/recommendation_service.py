from app.engines.thalamus.filters import ThalamusFilter
from app.engines.sara.vector_search import SaraEngine
from app.engines.accumbens.ranker import AccumbensRanker
from app.db.repositories.content_repository import ContentRepository
from app.db.session import async_session

class RecommendationService:
    def __init__(self):
        self.thalamus = ThalamusFilter()
        self.sara = SaraEngine()
        self.accumbens = AccumbensRanker()

    async def get_feed(self, request):
        async with async_session() as session:
            repo = ContentRepository(session)
            # Busca candidatos reais do banco
            raw_objects = await repo.get_candidates()
            raw_data = [{"id": o.id, "tags": o.tags, "safety": o.safety_label} for o in raw_objects]
            
            # Se o banco estiver vazio, usa um fallback para teste
            if not raw_data:
                raw_data = [{"id": "test_1", "tags": ["politics"], "safety": "safe"}]

            clean = await self.thalamus.apply(request, raw_data)
            aligned = await self.sara.align(request.user_id, clean)
            return await self.accumbens.rank(aligned)

recommendation_service = RecommendationService()