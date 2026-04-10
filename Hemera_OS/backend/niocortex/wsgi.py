# niocortex_saas/niocortex/wsgi.py

import os
from django.core.wsgi import get_wsgi_application

# Aponta para o settings correto
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'niocortex.settings')

application = get_wsgi_application()