import os
import sys

print("=== INICIANDO IO CONSCIOS (PORTA 8001) ===")

print("\n[1/3] Rodando Testes...")
os.system("pytest tests/")

print("\n[2/3] Verificando Banco de Dados...")
if not os.path.exists("zios_brain.db"):
    print("   -> Arquivo zios_brain.db será criado.")

print("\n[3/3] 🚀 INICIANDO SERVIDOR...")
print("   -> Doc: http://localhost:8001/docs")
os.system("uvicorn main:app --reload --host 0.0.0.0 --port 8001")