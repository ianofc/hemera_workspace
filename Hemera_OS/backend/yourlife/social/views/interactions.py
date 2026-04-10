from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
try:
    from ..models import Post, Comentario, Like
except ImportError:
    Post = None

@login_required
def toggle_like(request, post_id):
    # Se o ID não for número (ex: 'sys_welcome'), ignora silenciosamente
    if not str(post_id).isdigit():
        return HttpResponse(status=200)

    if not Post:
        return HttpResponse(status=500)

    post = get_object_or_404(Post, id=post_id)
    
    # Lógica de Like/Unlike
    like_qs = Like.objects.filter(post=post, usuario=request.user)
    if like_qs.exists():
        like_qs.delete()
        user_liked = False
    else:
        Like.objects.create(post=post, usuario=request.user)
        user_liked = True

    # Retorna apenas o botão atualizado (HTMX Pattern)
    context = {
        'post': {
            'id': post.id,
            'total_likes': post.likes.count(),
            'user_liked': user_liked,
            'is_system': False
        }
    }
    # Renderiza um mini-template inline apenas para o ícone
    return render(request, 'social/components/partials/like_button.html', context)

@login_required
def add_comment(request, post_id):
    if not str(post_id).isdigit():
        return HttpResponse(status=200)
        
    if request.method == 'POST' and Post:
        post = get_object_or_404(Post, id=post_id)
        conteudo = request.POST.get('conteudo')
        if conteudo:
            Comentario.objects.create(post=post, autor=request.user, conteudo=conteudo)
    
    return HttpResponse(status=204) # Retorna nada (Stay on page)
