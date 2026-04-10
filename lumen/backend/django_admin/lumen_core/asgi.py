
import os, django
from django.core.asgi import get_asgi_application
from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lumen_core.settings")
django.setup()

django_app = get_asgi_application()

fastapi_app = FastAPI(title="LUMEN API")

@fastapi_app.get("/health")
def health():
    return {"status": "ok"}

app = fastapi_app
app.mount("/admin", WSGIMiddleware(django_app))
