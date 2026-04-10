from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ..models import Post

@login_required
def explore_view(request):
    # Grid de Mídia (Masonry)
    try:
        media_posts = Post.objects.exclude(imagem='', video='').order_by('-data_criacao')[:50]
    except:
        media_posts = []
    return render(request, 'social/search/explore.html', {'media_posts': media_posts})

@login_required
def reels_view(request):
    return render(request, 'social/reels/index.html')

@login_required
def settings_view(request):
    return render(request, 'social/pages/settings.html')

@login_required
def support_view(request):
    return render(request, 'social/pages/support.html')

@login_required
def theme_view(request):
    return render(request, 'social/pages/themes.html')
