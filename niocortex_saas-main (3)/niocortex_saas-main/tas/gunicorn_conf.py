import multiprocessing

# Configurações de Performance para Produção
bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1  # Escalabilidade baseada no CPU
worker_class = "uvicorn.workers.UvicornWorker"
timeout = 120
keepalive = 5
loglevel = "info"
errorlog = "-"
accesslog = "-"