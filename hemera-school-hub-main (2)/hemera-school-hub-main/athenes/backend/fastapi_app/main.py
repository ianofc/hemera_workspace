from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="ATHENES API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "ATHENES API", "version": "1.0.0"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

# Zeus AI endpoints
@app.post("/api/ai/chat")
async def chat(message: dict):
    return {
        "response": "Esta é uma resposta simulada do Zeus AI. Em produção, integrar com OpenAI.",
        "suggestions": ["Exemplo prático", "Ver fórmulas", "Exercícios"]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
