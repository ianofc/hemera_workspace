# Correções rápidas para problemas comuns

## PROBLEMA 1: tsconfig.node.json faltante
# ✅ Já criado!

## PROBLEMA 2: django_filters não instalado
# Solução: Instalar manualmente
pip install django-filter

## PROBLEMA 3: uvicorn em uso
# Solução: Matar processo ou usar porta diferente
# netstat -ano | findstr :8000
# taskkill /PID <PID> /F

## PROBLEMA 4: Ativar venv no Windows
# Use: .\venv\Scripts\Activate.ps1
# Ou: venv\Scripts\activate.bat

## PROBLEMA 5: Permissões no Windows
# Execute o PowerShell como Administrador

## COMANDOS RÁPIDOS:

# 1. Limpar e reinstalar tudo:
# Remove-Item -Recurse -Force frontend/node_modules
# cd frontend; npm install

# 2. Backend do zero:
# cd backend
# python -m venv venv_new
# .\venv_new\Scripts\Activate.ps1
# pip install django djangorestframework django-cors-headers django-filter pillow
# python manage.py migrate

# 3. Rodar sem Docker:
# Terminal 1: cd frontend; npm run dev
# Terminal 2: cd backend; python manage.py runserver
# Terminal 3: cd backend; uvicorn fastapi_app.main:app --reload --port 8001

