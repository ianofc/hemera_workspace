import os
import sys
import django

# Add backend root to python path
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

# Initialize Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'niocortex.settings')
django.setup()
