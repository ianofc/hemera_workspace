import os

FILES = {
    # 1. ANALISTA UNIVERSAL: Integrando lógica de Educação e Chat do Legado
    "routers/v1/analyst.py": '''
from fastapi import APIRouter, UploadFile, File
from core.zios import ZiosOrchestrator

router = APIRouter()

@router.post("/analyze/{mode}")
async def analyze_task(mode: str, file: UploadFile = File(None), text: str = None):
    """
    Substitui os routers de 'chat' e 'education' do IO CONSCIUS.
    Modos: 'pedagogico', 'juridico', 'dev', 'estrategico'
    """
    zios = ZiosOrchestrator("ian_master")
    
    # Prepara o contexto baseado no modo (herdando a inteligência do legado)
    context = {"mode": mode, "user_id": "ian_master"}
    
    input_content = text if text else ""
    if file:
        file_data = await file.read()
        input_content += f"\\n[CONTEÚDO DO ARQUIVO]:\\n{file_data.decode('utf-8', errors='ignore')}"
    
    # O Zios processa usando a Persona Líquida
    response = zios.process(input_content, context)
    return {"status": "success", "response": response}
''',

    # 2. AUTO-IMPLEMENTAÇÃO: Habilitando o Zios a criar scripts de integração
    "core/coding.py": '''
import subprocess
import os

class ZiosSelfCoder:
    """Capacidade do Zios de gerar ferramentas para seus novos projetos."""
    def __init__(self, sandbox_path="sandbox/runtime"):
        self.sandbox_path = sandbox_path
        os.makedirs(self.sandbox_path, exist_ok=True)

    def run_tool(self, code: str):
        file_path = os.path.join(self.sandbox_path, "generated_tool.py")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(code)
        return subprocess.run(["python", file_path], capture_output=True, text=True)
'''
}

def finalize_migration():
    print("🚀 ZIOS: Finalizando integração para uso em projetos...")
    for path, content in FILES.items():
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content.strip())
    print("✅ Sucesso: O ZIOS agora pode processar tarefas de Chat e Educação do legado.")

if __name__ == "__main__":
    finalize_migration()