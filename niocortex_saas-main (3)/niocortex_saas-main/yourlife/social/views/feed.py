from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import random

# Import seguro
try:
    from ..models import Post
except ImportError:
    Post = None

def gerar_eventos_social(user):
    eventos = []
    # 1. Boas-vindas
    eventos.append({
        'id': 'sys_welcome',
        'autor': user,
        'is_system': True,
        'tipo': 'video', 
        'video': {'url': '/static/social/img/system/welcome_neural.mp4'},
        'imagem': None,
        'conteudo': f"🧬 NEUROCONEXÃO ESTABELECIDA.\n\nBem-vindo ao YourLife, {user.first_name}.\nSua jornada digital começa agora. O que você está processando hoje?",
        'data_criacao': user.date_joined,
        'location': 'NioCortex Core',
        'total_likes': 1,
        'total_comentarios': 0,
        'user_liked': True,
    })
    return eventos

@login_required
def create_post(request):
    # Lógica de salvar o post
    if request.method == 'POST' and Post:
        conteudo = request.POST.get('conteudo', '')
        imagem = request.FILES.get('imagem')
        video = request.FILES.get('video')
        
        # Só salva se tiver algum conteúdo
        if conteudo or imagem or video:
            Post.objects.create(
                autor=request.user,
                conteudo=conteudo,
                imagem=imagem,
                video=video,
                location="Via Neural Link" # Flavor text
            )
            
    # Redireciona para o feed para ver o novo post
    return redirect('yourlife_social:home')

@login_required
def home_feed_foryou(request):
    posts = []
    if Post:
        try:
            db_posts = Post.objects.all().select_related('autor', 'autor__profile').order_by('-data_criacao')[:30]
            posts = list(db_posts)
        except:
            posts = []

    if not posts:
        posts = gerar_eventos_social(request.user)

    context = {'posts': posts, 'filter_type': 'foryou'}

    if request.headers.get('HX-Request'):
        return render(request, 'social/components/home/feed_list_content.html', context)
    
    return render(request, 'social/feed/home.html', context)

@login_required
def home_feed_following(request):
    posts = []
    if not posts:
        posts = gerar_eventos_social(request.user)
    
    context = {'posts': posts, 'filter_type': 'following'}
    if request.headers.get('HX-Request'):
        return render(request, 'social/components/home/feed_list_content.html', context)
    return render(request, 'social/feed/home.html', context)
