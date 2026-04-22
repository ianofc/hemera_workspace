from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.api.v1.api import api_router
import traceback

app = FastAPI(title="TAS Engine")

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    print(f"🔥 ERRO NO SERVIDOR: {exc}")
    traceback.print_exc()
    return JSONResponse(status_code=500, content={"detail": str(exc), "trace": "Verifique o terminal"})

app.include_router(api_router, prefix="/api/v1")
@app.get("/health")
async def health(): return {"status": "online"}