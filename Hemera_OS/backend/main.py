from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import database

app = FastAPI(title="Hemera OS Core API")

# Dependência do Banco
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home():
    return {"status": "Hemera OS Backend Operacional", "engine": "SQLite"}

@app.post("/auth/login")
def login_simulado(email: str, role: str):
    # Por enquanto, apenas valida a estrutura
    return {"id": 1, "email": email, "role": role}