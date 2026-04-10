# Setup ATHENES - Windows PowerShell

Write-Host "🏛️  Configurando ATHENES..." -ForegroundColor Cyan

# Frontend
Write-Host "📦 Instalando Frontend..." -ForegroundColor Yellow
Set-Location frontend
npm install
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Frontend instalado!" -ForegroundColor Green
} else {
    Write-Host "❌ Erro no frontend" -ForegroundColor Red
}
Set-Location ..

# Backend
Write-Host "🐍 Configurando Backend..." -ForegroundColor Yellow
Set-Location backend

# Criar venv se não existir
if (-not (Test-Path "venv")) {
    python -m venv venv
}

# Ativar venv
& .\venv\Scripts\Activate.ps1

# Instalar dependências
pip install django djangorestframework django-cors-headers django-filter pillow python-dotenv

# Criar migrations
python manage.py makemigrations
python manage.py migrate

Write-Host "✅ Backend configurado!" -ForegroundColor Green

Set-Location ..

Write-Host ""
Write-Host "🚀 Para iniciar:" -ForegroundColor Cyan
Write-Host "  Frontend: cd frontend; npm run dev" -ForegroundColor White
Write-Host "  Backend:  cd backend; .\venv\Scripts\Activate.ps1; python manage.py runserver" -ForegroundColor White
Write-Host "  FastAPI:  cd backend; .\venv\Scripts\Activate.ps1; uvicorn fastapi_app.main:app --reload --port 8001" -ForegroundColor White
