import subprocess
import sys
import os

def run():
    print("🚀 [TAS ORCHESTRATOR] Iniciando motor...")
    
    # 1. Instala dependências
    print("📦 Instalando dependências...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

    # 2. Inicializa o Banco no Supabase
    print("🗄️ Inicializando Banco de Dados...")
    env = os.environ.copy()
    env["PYTHONPATH"] = os.getcwd()
    subprocess.run([sys.executable, "scripts/init_db.py"], env=env)

    # 3. Liga o Servidor
    print("🔥 Ligando TAS Engine na porta 8000...")
    try:
        subprocess.run([sys.executable, "-m", "uvicorn", "app.main:app", "--reload"], env=env)
    except KeyboardInterrupt:
        print("\n🛑 Motor desligado pelo usuário.")

if __name__ == "__main__":
    run()