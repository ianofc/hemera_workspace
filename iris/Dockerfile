# iris/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Evita buffer de logs
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Limita reload para evitar "Cannot allocate memory"
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8003", "--reload", "--reload-dir", "/app", "--reload-include", "*.py"]