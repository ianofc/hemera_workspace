from django.http import JsonResponse

# Temporário: Aqui você inicializa o Django Ninja ou DRF futuramente.
# Exemplo com Django Ninja:
# from ninja import NinjaAPI
# api = NinjaAPI()
# @api.get("/status")
# def status(request):
#     return {"status": "ok", "message": "Backend do Hemera_OS está pronto e operante!"}

def api_status(request):
    return JsonResponse({"status": "ok", "message": "Backend do Hemera_OS está preparado para receber qualquer Frontend React/Vite/Next."})
