from fastapi import FastAPI
from routers.v1 import analyst

app = FastAPI(title="ZIOS: Adaptive Life OS")
app.include_router(analyst.router, prefix="/v1")

@app.get("/")
async def health():
    return {"status": "ZIOS ONLINE"}