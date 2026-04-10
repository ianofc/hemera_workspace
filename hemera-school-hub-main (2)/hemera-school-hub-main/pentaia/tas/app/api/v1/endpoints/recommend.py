from fastapi import APIRouter, Query
from pydantic import BaseModel

from app.services.recommendation_service import recommendation_service


class RecRequest(BaseModel):
    user_id: str
    context: str


router = APIRouter()


@router.post("/")
async def get_recommendations(req: RecRequest, include_meta: bool = Query(default=False)):
    if include_meta:
        ids, meta = await recommendation_service.get_feed_with_meta(req)
        return {"user_id": req.user_id, "items": ids, "meta": meta}

    ids = await recommendation_service.get_feed(req)
    return {"user_id": req.user_id, "items": ids}


@router.get("/trends")
async def get_trending_topics(limit: int = Query(default=10, ge=1, le=50)):
    return await recommendation_service.get_trends(limit=limit)
