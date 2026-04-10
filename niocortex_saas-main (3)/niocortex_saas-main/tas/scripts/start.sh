#!/bin/bash
set -e
echo "🚀 [TAS] Aguardando Banco de Dados..."
until nc -z db 5432; do
  sleep 1
done
echo "✅ [TAS] Banco detectado! Iniciando API..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload