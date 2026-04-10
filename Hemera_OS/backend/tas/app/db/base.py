from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, JSON, DateTime
from sqlalchemy.sql import func
import numpy as np

Base = declarative_base()

class ContentModel(Base):
    __tablename__ = "contents"
    id = Column(String, primary_key=True)
    title = Column(String)
    tags = Column(JSON)  # Armazena categorias como ["política", "real_life"]
    safety_label = Column(String) # 'safe', 'nsfw_soft', etc.
    author_id = Column(String)
    # O campo embedding será tratado como ARRAY para busca vetorial
    embedding = Column(JSON) 
    created_at = Column(DateTime(timezone=True), server_default=func.now())