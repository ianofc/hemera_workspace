from fastapi import APIRouter
from app.api.v1.endpoints import recommend, events, user, search

api_router = APIRouter()
api_router.include_router(recommend.router, prefix="/recommend", tags=["Recommendation"])
api_router.include_router(events.router, prefix="/events", tags=["Ingestion"])
api_router.include_router(user.router, prefix="/user", tags=["Sovereignty"])
api_router.include_router(search.router, prefix="/search", tags=["Semantic Search"])