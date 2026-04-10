import os
from django.core.asgi import get_asgi_application

# 1. Configura o ambiente
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'niocortex.settings')

# 2. Inicializa a aplicação Django HTTP (Deve vir ANTES de importar rotas do Channels)
django_asgi_app = get_asgi_application()

# 3. Importa os componentes do Channels e Rotas (Agora seguro)
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import yourlife.social.routing

# 4. Define a aplicação principal
application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            yourlife.social.routing.websocket_urlpatterns
        )
    ),
})