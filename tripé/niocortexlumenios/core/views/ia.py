import json
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from core.services.ai_client import AIClient

# --- Adicione esta view que estava perdida ---
@login_required
def talkio_view(request):
    """ Interface Full-Screen do Chat (Talkio) """
    context = {
        'user': request.user,
        'is_premium': getattr(request.user, 'is_premium', False)
    }
    return render(request, 'core/talkio.html', context)
# ---------------------------------------------

@login_required
@require_POST
def api_check_zios(request):
    """ Verifica se a IA deve interagir proativamente """
    try:
        data = json.loads(request.body)
        path = data.get('path', '/')
        meta = {} 
        resultado = AIClient.check_proactive_thought(request.user, path, meta)
        return JsonResponse(resultado)
    except Exception as e:
        return JsonResponse({"should_speak": False, "error": str(e)})

@login_required
@require_POST
def api_chat_zios(request):
    """ Chat Universal com a IA """
    try:
        data = json.loads(request.body)
        mensagem = data.get('message', '')
        if not mensagem:
            return JsonResponse({'reply': 'Por favor, digite algo.'})
        resultado = AIClient.chat_universal(mensagem, request.user)
        return JsonResponse(resultado)
    except Exception as e:
        return JsonResponse({'reply': 'Erro de conexão com o Zios AI.'}, status=500)

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from zios.core.brain import ZiosBrain

@login_required
def zios_welcome(request):
    """
    Apresentação oficial do Zios como Life OS.
    """
    brain = ZiosBrain()
    # Zios gera uma saudação personalizada baseada no CustomUser
    msg = brain.process(f"O usuário {request.user.username} acabou de logar. Dê as boas-vindas como seu Mentor.", context='ONBOARDING')
    
    return render(request, 'zios/welcome.html', {
        'zios_message': msg,
        'title': 'Despertar do ZIOS'
    })
