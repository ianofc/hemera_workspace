from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def meu_perfil(request):
    # Redireciona para o perfil do usuário logado
    return redirect('yourlife_social:profile_detail', username=request.user.username)

@login_required
def profile_detail(request, username):
    profile_user = get_object_or_404(User, username=username)
    is_me = (request.user == profile_user)
    
    context = {
        'profile_user': profile_user,
        'is_me': is_me,
        # Adicione outros contextos necessários aqui
    }
    return render(request, 'social/profile/profile_detail.html', context)
