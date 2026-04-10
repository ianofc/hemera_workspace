from django.urls import path
from .views import feed, auth, profile, general, groups, events, interactions, chat, posts 

app_name = 'yourlife_social'

urlpatterns = [
    # --- FEED & HOME ---
    path('', feed.home_feed_foryou, name='home'),
    path('feed/foryou/', feed.home_feed_foryou, name='home_feed_foryou'),
    path('feed/following/', feed.home_feed_following, name='home_feed_following'),
    
    # --- CRIAÇÃO DE CONTEÚDO (USANDO O NOVO ARQUIVO POSTS) ---
    # Removi a linha antiga que apontava para feed.create_post
    path('post/create/', posts.create_post, name='create_post'),
    path('post/delete/<int:post_id>/', posts.delete_post, name='delete_post'),

    # --- INTERAÇÕES (Likes/Comments) ---
    path('post/<str:post_id>/like/', interactions.toggle_like, name='toggle_like'),
    path('post/<str:post_id>/comment/', interactions.add_comment, name='add_comment'),
    
    # --- DISCOVERY & MEDIA ---
    path('explore/', general.explore_view, name='explore'),
    path('reels/', general.reels_view, name='reels'),

    # --- COMUNIDADES (GROUPS) ---
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