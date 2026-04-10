from sqlalchemy import Column, String, JSON
from app.db.base import Base

class UserProfileModel(Base):
    __tablename__ = "user_profiles"
    user_id = Column(String, primary_key=True)
    blacklisted_tags = Column(JSON, default=[])      # O que ele NUNCA quer ver
    blacklisted_authors = Column(JSON, default=[])   # Quem ele bloqueou
    priority_interests = Column(JSON, default=[])    # O que ele quer ver MAIS