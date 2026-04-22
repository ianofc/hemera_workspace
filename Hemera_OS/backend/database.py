from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Nosso arquivo de banco local
SQLALCHEMY_DATABASE_URL = "sqlite:///./hemera_core.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modelo Inicial (Inspirado no Cortex Educ)
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String) # 'professor' ou 'aluno'
    tenant_id = Column(String, default="escola_padrao")

Base.metadata.create_all(bind=engine)