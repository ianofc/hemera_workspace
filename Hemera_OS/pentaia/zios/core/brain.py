from google import genai
from identity.priors import get_liquid_prompt
from core.config import settings

class ZiosBrain:
    """Interface Neural estabilizada para o ZIOS."""
    def __init__(self, memory):
        self.memory = memory
        # Inicializa o cliente forçando a versão v1beta para garantir suporte ao gemini-1.5-pro
        self.client = genai.Client(
            api_key=settings.GOOGLE_API_KEY,
            http_options={'api_version': 'v1beta'}
        )

    def think(self, user_input, context):
        user_id = context.get("user_id", "ian_master") if context else "ian_master"
        memories = self.memory.recall(user_input)
        
        # Gera o prompt líquido baseado na identidade do Ian
        liquid_prompt = get_liquid_prompt(memories, user_input, user_id)
        
        try:
            # Chamada ao modelo gemini-1.5-pro com as instruções do sistema
            response = self.client.models.generate_content(
                model='gemini-1.5-pro',
                config={'system_instruction': liquid_prompt},
                contents=user_input
            )
            return response.text
        except Exception as e:
            return f"❌ Erro na síntese neural: {str(e)}"