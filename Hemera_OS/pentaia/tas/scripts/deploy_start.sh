#!/bin/bash
set -e

echo "🚀 [DEPLOY] Iniciando TAS Engine em Modo Produção..."

# 1. Instala dependências silenciosamente
pip install --no-cache-dir -r requirements.txt

# 2. Sincroniza Tabelas do Supabase
echo "🗄️ Sincronizando Schema no Supabase..."
python scripts/init_db.py
python scripts/sync_user_db.py

# 3. Inicia o Gunicorn (O Servidor Industrial)
echo "🔥 TAS Online. Gerindo conexões via Gunicorn..."
exec gunicorn -c gunicorn_conf.py app.main:app