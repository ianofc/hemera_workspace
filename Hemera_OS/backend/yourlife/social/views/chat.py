from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def chat_view(request):
    # Renderiza o template principal do Talkio
    return render(request, 'social/talkio/index.html')
