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
        input_content += f"\n[CONTEÚDO DO ARQUIVO]:\n{file_data.decode('utf-8', errors='ignore')}"
    
    # O Zios processa usando a Persona Líquida
    response = zios.process(input_content, context)
    return {"status": "success", "response": response}