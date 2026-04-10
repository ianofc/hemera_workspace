from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Módulos reunificados no padrão Super App
    path('', include('stage.publico.urls')),
    path('core/', include('core.urls')),
    path('social/', include('yourlife.social.urls', namespace='yourlife_social')),
    
    # Módulos Profissionais
    path('hub/', include('hub.secretaria.urls')),
    path('rh/', include('humanex.rh.urls')),
    path('financeiro/', include('ledger.financeiro.urls')),
    path('pedagogico/', include('lumenios.pedagogico.urls')),
    path('plataforma/', include('lumenios.plataforma.urls')),
    path('coordenacao/', include('orbit.coordenacao.urls')),
    path('direcao/', include('prioris.direcao.urls')),
    path('crm/', include('vionex.crm.urls')),
    path('talkio-app/', include('talkio.chat.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
