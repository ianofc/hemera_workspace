from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def global_id_card(request):
    """
    Carteirinha digital acessível para qualquer usuário logado (Professor, Aluno, etc)
    """
    return render(request, 'core/ferramentas/carteirinha.html')