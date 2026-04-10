import os

# ==============================================================================
# 1. URLS.PY (A COLUNA VERTEBRAL)
# ==============================================================================
# Define TODAS as rotas que uma rede social precisa.
URLS_CONTENT = """from django.urls import path
from .views import feed, auth, profile, general, groups, events, interactions, chat

app_name = 'yourlife_social'

urlpatterns = [
    # --- FEED & HOME ---
    path('', feed.home_feed_foryou, name='home'),
    path('feed/foryou/', feed.home_feed_foryou, name='home_feed_foryou'),
    path('feed/following/', feed.home_feed_following, name='home_feed_following'),
    
    # --- CRIAÇÃO DE CONTEÚDO ---
    path('post/create/', feed.create_post, name='create_post'),

    # --- INTERAÇÕES (Likes/Comments) ---
    path('post/<str:post_id>/like/', interactions.toggle_like, name='toggle_like'),
    path('post/<str:post_id>/comment/', interactions.add_comment, name='add_comment'),

    # --- DISCOVERY & MEDIA ---
    path('explore/', general.explore_view, name='explore'),
    path('reels/', general.reels_view, name='reels'),

    # --- COMUNIDADES (GROUPS) - O ERRO ESTAVA AQUI ---
    path('groups/', groups.groups_list_view, name='groups_list'),
    path('groups/create/', groups.group_create_view, name='group_create'),
    path('groups/<int:group_id>/', groups.group_detail_view, name='group_detail'),

    # --- EVENTOS (EVENTS) ---
    path('events/', events.events_list_view, name='events_list'),
    path('events/calendar/', events.calendar_view, name='calendar'),
    path('events/<int:event_id>/', events.event_detail_view, name='event_detail'),

    # --- MESSENGER (TALKIO) ---
    path('talkio/', chat.chat_view, name='talkio_app'),

    # --- PERFIL & CONFIGURAÇÕES ---
    path('profile/me/', profile.profile_detail, {'username': 'me'}, name='meu_perfil'),
    path('profile/<str:username>/', profile.profile_detail, name='profile_detail'),
    path('settings/', general.settings_view, name='settings_page'),
    path('support/', general.support_view, name='support_page'),
    path('theme/', general.theme_view, name='settings_theme'),

    # --- AUTH ---
    path('login/', auth.login_view, name='login'),
    path('logout/', auth.logout_view, name='logout'),
]
"""

# ==============================================================================
# 2. VIEWS: GROUPS.PY (Comunidades)
# ==============================================================================
GROUPS_VIEW = """from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def groups_list_view(request):
    # Renderiza a lista de comunidades (estilo Facebook Groups / Reddit)
    return render(request, 'social/groups/list.html')

@login_required
def group_detail_view(request, group_id):
    # Renderiza a home de um grupo específico
    return render(request, 'social/groups/detail.html')

@login_required
def group_create_view(request):
    return render(request, 'social/groups/create.html')
"""

# ==============================================================================
# 3. VIEWS: EVENTS.PY (Eventos/Calendário)
# ==============================================================================
EVENTS_VIEW = """from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def events_list_view(request):
    # Lista de eventos próximos (estilo Eventbrite / Facebook Events)
    return render(request, 'social/events/list.html')

@login_required
def event_detail_view(request, event_id):
    return render(request, 'social/events/detail.html')

@login_required
def calendar_view(request):
    return render(request, 'social/events/calendar.html')
"""

# ==============================================================================
# 4. VIEWS: GENERAL.PY (Complementos)
# ==============================================================================
GENERAL_VIEW = """from django.shortcuts import render
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
"""

def fix_all_routes():
    files = [
        {'path': 'yourlife/social/urls.py', 'content': URLS_CONTENT, 'name': 'Rotas (URLs)'},
        {'path': 'yourlife/social/views/groups.py', 'content': GROUPS_VIEW, 'name': 'View Grupos'},
        {'path': 'yourlife/social/views/events.py', 'content': EVENTS_VIEW, 'name': 'View Eventos'},
        {'path': 'yourlife/social/views/general.py', 'content': GENERAL_VIEW, 'name': 'View Geral/Explorar'},
    ]

    print("🛠️ Consertando a Rede Social inteira...")
    
    for f in files:
        try:
            os.makedirs(os.path.dirname(f['path']), exist_ok=True)
            with open(f['path'], 'w', encoding='utf-8') as file:
                file.write(f['content'])
            print(f"✅ {f['name']} corrigido.")
        except Exception as e:
            print(f"❌ Erro em {f['path']}: {e}")

    print("\n🚀 PRONTO. Todas as seções (Feed, Grupos, Eventos, Explorar) agora têm rotas válidas.")
    print("👉 Reinicie o servidor. O erro 'NoReverseMatch' deve desaparecer para sempre.")

if __name__ == "__main__":
    fix_all_routes()