# yourlife/social/views/posts.py
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import Post

@login_required
def create_post(request):
    """
    Recebe o formulário direto da Home e salva.
    Sem renderizar templates de criação.
    """
    if request.method == 'POST':
        conteudo = request.POST.get('conteudo', '').strip()
        imagem = request.FILES.get('imagem')
        visibilidade = request.POST.get('visibilidade', 'publico')

        if not conteudo and not imagem:
            messages.warning(request, "Você não pode criar um post vazio.")
            return redirect('yourlife_social:home')

        try:
            Post.objects.create(
                autor=request.user,
                conteudo=conteudo,
                imagem=imagem,
                visibilidade=visibilidade
            )
            messages.success(request, "Post publicado!")
        except Exception as e:
            print(f"Erro ao postar: {e}")
            messages.error(request, "Erro ao publicar o post.")

    # Sempre redireciona para a Home (Feed), nunca para uma tela de sucesso separada
    return redirect('yourlife_social:home')

@login_required
def delete_post(request, post_id):
    # (Mantém a lógica de delete anterior)
    try:
        post = Post.objects.get(id=post_id)
        if post.autor == request.user:
            post.delete()
            messages.success(request, "Post excluído.")
    except Post.DoesNotExist:
        pass
    return redirect('yourlife_social:home')