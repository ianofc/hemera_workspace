FROM python:3.11-slim

# Metadados
LABEL maintainer="PentaIA Engineering Hub"
LABEL service="TAS - Matrix Suite"
LABEL version="2.2.0"

# Ambiente
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PORT=8001 \
    HOST=0.0.0.0 \
    RELOAD=true

# 1. Cria o usuário ANTES de definir o WORKDIR para evitar problemas de permissão base
RUN useradd -m pentaia

WORKDIR /app

# 2. Dependências de sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 3. Instala dependências do Python PRIMEIRO (como root)
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 4. Copia o restante dos arquivos já pertencendo ao usuário 'pentaia'
COPY --chown=pentaia:pentaia . /app/

# 5. Define as permissões finais da pasta (caso o pip tenha deixado lixo como root)
RUN chown -R pentaia:pentaia /app

# 6. Troca para o usuário não-root só no final
USER pentaia

EXPOSE 8001

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8001/ || exit 1

CMD ["python", "main.py"]