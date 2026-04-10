from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Importamos as views reais do social para não duplicar lógica
from yourlife.social.views.auth import login_view as social_login
from yourlife.social.views.auth import logout_view as social_logout
from yourlife.social.views.auth import register_view as social_register

# --- Wrappers de Autenticação ---

def login_view(request):
    return social_login(request)

def logout_view(request):
    return social_logout(request)

def register_view(request):
    return social_register(request)

# --- Roteador de Dashboard (A FUNÇÃO QUE FALTAVA) ---
@login_required
def dashboard_router_view(request):
    user = request.user
    # Redireciona com base no papel do usuário
    if 'PROFESSOR' in user.role:
        return redirect('lumenios:dashboard_professor')
    elif 'ALUNO' in user.role:
        return redirect('lumenios:dashboard_aluno')
    elif 'SECRETARIA' in user.role:
        return redirect('hub_secretaria:dashboard')
    elif 'DIRECAO' in user.role:
        return redirect('prioris_direcao:dashboard')
    elif 'RH' in user.role:
        return redirect('humanex_rh:dashboard')
    else:
        # Padrão para social se não tiver papel específico
        return redirect('yourlife_social:home')
