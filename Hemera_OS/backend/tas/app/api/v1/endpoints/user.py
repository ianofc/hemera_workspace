from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.future import select
from app.db.session import get_db
from app.db.base_user import UserProfileModel

router = APIRouter()

class ProfileUpdate(BaseModel):
    user_id: str
    blacklisted_tags: list = None
    blacklisted_authors: list = None
    priority_interests: list = None

@router.post("/update_profile")
async def update_profile(data: ProfileUpdate, db=Depends(get_db)):
    result = await db.execute(select(UserProfileModel).filter_by(user_id=data.user_id))
    profile = result.scalars().first()
    
    if not profile:
        profile = UserProfileModel(user_id=data.user_id)
        db.add(profile)
    
    if data.blacklisted_tags is not None: profile.blacklisted_tags = data.blacklisted_tags
    if data.blacklisted_authors is not None: profile.blacklisted_authors = data.blacklisted_authors
    
    await db.commit()
    return {"status": "success", "user_id": data.user_id}