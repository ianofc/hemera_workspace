from fastapi import APIRouter
from app.services.recommendation_service import recommendation_service
from pydantic import BaseModel

class RecRequest(BaseModel):
    user_id: str
    context: str

router = APIRouter()
@router.post("/")
async def get_recommendations(req: RecRequest):
    ids = await recommendation_service.get_feed(req)
    return {"user_id": req.user_id, "items": ids}