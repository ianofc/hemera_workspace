# tas/run_tas.py (modo desenvolvimento apenas)
#!/usr/bin/env python3
"""
TAS - Script de conveniência para desenvolvimento local
NO DOCKER: Use main.py diretamente
"""

import subprocess
import sys
import os

def run():
    print("🚀 [TAS ORCHESTRATOR - DEV MODE]")
    print("⚠️  Para Docker, use: python main.py")
    print("-" * 50)
    
    # Instala dependências se necessário
    if os.path.exists("requirements.txt"):
        print("📦 Verificando dependências...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", "-r", "requirements.txt"])
    
    # Inicializa banco se script existir
    if os.path.exists("scripts/init_db.py"):
        print("🗄️ Inicializando banco...")
        env = os.environ.copy()
        env["PYTHONPATH"] = os.getcwd()
        subprocess.run([sys.executable, "scripts/init_db.py"], env=env)
    
    # Roda uvicorn
    print("🔥 Iniciando TAS...")
    env = os.environ.copy()
    env["PYTHONPATH"] = os.getcwd()
    env["RELOAD"] = "true"
    
    try:
        subprocess.run([
            sys.executable, "main.py"
        ], env=env)
    except KeyboardInterrupt:
        print("\n🛑 Desligado.")

if __name__ == "__main__":
    run()