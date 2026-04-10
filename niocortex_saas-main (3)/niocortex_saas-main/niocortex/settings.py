from pathlib import Path
import os
from dotenv import load_dotenv
import dj_database_url

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-chave-padrao-dev')

DEBUG = True

ALLOWED_HOSTS = ['*']

# --- CORREÇÃO CSRF E SEGURANÇA ---
CSRF_TRUSTED_ORIGINS = [
    'http://127.0.0.1:8000',
    'http://localhost:8000',
]
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False

INSTALLED_APPS = [
    'django_htmx',
    'daphne',  # OBRIGATÓRIO: Primeiro da lista para ASGI
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'channels',  # WebSockets e Gerenciamento de Background

    # Apps do Projeto
    'core',
    'yourlife.social',
    'hub.secretaria',
    'humanex.rh',
    'ledger.financeiro',
    'lumenios.pedagogico',
    'lumenios.plataforma',
    'orbit.coordenacao',
    'prioris.direcao',
    'vionex.crm',
    'stage.publico',
    'talkio.chat',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django_htmx.middleware.HtmxMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'niocortex.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
            BASE_DIR / 'templates-cortex',
            BASE_DIR / 'lumenios' / 'templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'core.context_processors.module_context',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Configuração ASGI/WSGI
ASGI_APPLICATION = 'niocortex.asgi.application'
WSGI_APPLICATION = 'niocortex.wsgi.application'

# --- BANCO DE DADOS ---
database_url = os.getenv('DATABASE_URL')
if not database_url:
    # Fallback seguro
    database_url = "postgresql://postgres:2511CorteXEduc@db.qnknyonohlorjfhzkkpz.supabase.co:5432/postgres"

if database_url and "postgres" in database_url:
    DATABASES = {
        'default': dj_database_url.parse(database_url)
    }
else:
    raise Exception("ERRO CRÍTICO: DATABASE_URL do Supabase não encontrada.")

# --- CONFIGURAÇÃO REDIS (CACHE & CHANNELS) ---

# 1. CACHE
# Melhora performance geral e armazena sessões de usuário
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# Configura o Django para salvar as sessões no Redis ao invés do Banco de Dados
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

# 2. CHANNELS
# Essencial para o TalkIO funcionar rápido (WebSockets)
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}

# --- AUTH & REDIRECTS ---
AUTH_USER_MODEL = 'core.CustomUser'
LOGIN_REDIRECT_URL = 'yourlife_social:home'
LOGOUT_REDIRECT_URL = 'yourlife_social:login'
LOGIN_URL = 'yourlife_social:login'

# --- I18N / STATIC ---
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
MERCADO_PAGO_ACCESS_TOKEN = os.getenv('MP_ACCESS_TOKEN', 'seu_token_aqui')