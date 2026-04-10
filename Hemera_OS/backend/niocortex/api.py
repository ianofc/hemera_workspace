import json
from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt

def api_status(request):
    return JsonResponse({"status": "ok", "message": "Backend do Hemera_OS está preparado para receber qualquer Frontend React/Vite/Next."})

@csrf_exempt
def api_login(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            email = body.get('email', '')
            password = body.get('password', '')
            
            # Django authenticate usa username ou email dependendo do backend. Nosso CustomUser aceita email como username?
            # CustomUser em core/models.py geralmente define USERNAME_FIELD='username', mas vamos checar via Model
            from core.models import CustomUser
            user = None
            try:
                # Busca pelo email para achar o username real e tentar autenticar
                u = CustomUser.objects.get(email=email)
                user = authenticate(request, username=u.username, password=password)
            except CustomUser.DoesNotExist:
                user = authenticate(request, username=email, password=password)
            
            if user is not None:
                # Login com sucesso! (Gerar JWT real requer libs externas, enviaremos um Token seguro válido p/ frontend mock)
                import uuid
                fake_jwt = str(uuid.uuid4()) # Substituir por djangorestframework-simplejwt no futuro
                
                return JsonResponse({
                    "token": fake_jwt,
                    "user": {
                        "id": str(user.id),
                        "name": user.get_full_name() or user.username,
                        "email": user.email,
                        "role": user.role.lower() if user.role else 'student'
                    }
                })
            else:
                return JsonResponse({"error": "Credenciais inválidas"}, status=401)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Payload inválido"}, status=400)
    return JsonResponse({"error": "Apenas POST"}, status=405)
