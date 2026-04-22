from sqlalchemy import Column, Integer, String, DateTime, Text, JSON
from sqlalchemy.sql import func
from .database import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(String, index=True)
    action_type = Column(String)
    verdict = Column(String)
    details = Column(JSON)

class SoulMemory(Base):
    __tablename__ = "soul_memories"
    id = Column(Integer, primary_key=True, index=True)
    soul_name = Column(String, index=True)
    content = Column(Text) 
    honor_level = Column(String, default="PRIVATE")
    created_at = Column(DateTime(timezone=True), server_default=func.now())