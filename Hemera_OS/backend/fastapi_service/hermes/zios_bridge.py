import sys
import os
import asyncio
import logging
from typing import Optional, Dict

logger = logging.getLogger("hermes.zios_bridge")

# Garante que o diretório pai (backend) esteja no path para que possamos importar o módulo zios
backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if backend_dir not in sys.path:
    sys.path.append(backend_dir)

# Importação resiliente do ZIOS para suportar ambientes sem chaves no .env
ZIOS_AVAILABLE = False
try:
    from zios.core.zios import ZiosOrchestrator
    ZIOS_AVAILABLE = True
except Exception as e:
    logger.warning(f"ZIOS não disponível ou não configurado: {e}. Usando FallbackZiosOrchestrator.")

class FallbackZiosOrchestrator:
    """
    Fallback mock do ZiosOrchestrator para quando a API Key ou dependências do ZIOS não estiverem prontas.
    """
    def __init__(self, user_id: str):
        self.user_id = user_id

    def process(self, input_data: str, context: Optional[dict] = None) -> str:
        clean_input = input_data.replace("/zios", "").replace("@zios", "").strip()
        return f"🤖 [ZIOS Fallback Mode] Processado comando para '{self.user_id}': '{clean_input}'"

class ZiosBridge:
    """
    Bridge ZIOS: Conecta a mensageria Hermes à Inteligência Cognitiva ZIOS.
    Processa comandos ZIOS de forma assíncrona (canal lateral) para não interromper a conversa humana.
    """
    def __init__(self, connection_pool):
        self.pool = connection_pool

    def is_zios_command(self, text: str) -> bool:
        """
        Verifica se a mensagem contém um comando destinado ao ZIOS.
        """
        if not text:
            return False
        stripped = text.strip()
        return stripped.startswith("/zios") or stripped.startswith("@zios")

    async def handle_message(self, user_id: str, text: str, context: Optional[dict] = None):
        """
        Processa uma mensagem enviada pelo usuário. Se for um comando ZIOS, intercepta,
        processa assincronamente e envia a resposta de volta via canal lateral.
        """
        if not self.is_zios_command(text):
            return

        # Executa o processamento em background para liberar o fluxo de chat imediatamente
        asyncio.create_task(self._process_and_respond(user_id, text, context))

    async def _process_and_respond(self, user_id: str, text: str, context: Optional[dict]):
        """
        Gera a resposta do ZIOS (rodando a função síncrona em uma thread em segundo plano)
        e envia via WebSocket.
        """
        logger.info(f"Iniciando processamento de comando ZIOS para o usuário {user_id}")
        
        # Inicializa o orchestrator apropriado
        if ZIOS_AVAILABLE:
            try:
                orchestrator = ZiosOrchestrator(user_id)
            except Exception as e:
                logger.error(f"Erro ao instanciar ZiosOrchestrator: {e}. Usando mock fallback.")
                orchestrator = FallbackZiosOrchestrator(user_id)
        else:
            orchestrator = FallbackZiosOrchestrator(user_id)

        # Como o processamento do ZIOSBrain pode envolver requisições HTTP síncronas bloqueantes,
        # rodamos o processamento em uma thread separada para não travar o loop de eventos principal.
        try:
            full_context = context or {}
            if "user_id" not in full_context:
                full_context["user_id"] = user_id

            response = await asyncio.to_thread(orchestrator.process, text, full_context)
        except Exception as e:
            logger.error(f"Erro durante o processamento neural do ZIOS: {e}")
            response = f"❌ Erro na ponte ZIOS: {e}"

        # Envia a resposta de volta ao usuário pelo pool de WebSocket (marcando como canal de controle lateral)
        import json
        payload = {
            "sender_id": "zios",
            "recipient_id": user_id,
            "content": response,
            "is_control": True,
            "is_encrypted": False
        }
        
        await self.pool.send_personal_message(json.dumps(payload), user_id)
        logger.info(f"Resposta do ZIOS enviada com sucesso para o usuário {user_id} via canal lateral.")
