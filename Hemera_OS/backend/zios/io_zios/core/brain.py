import google.generativeai as genai
from core.config import settings
from core.logger import logger

if settings.GEMINI_API_KEY:
    genai.configure(api_key=settings.GEMINI_API_KEY)

def consult_gemini(system_prompt: str, user_input: str) -> str:
    if not settings.GEMINI_API_KEY:
        return "[MODO GUERRILHA] Sem chave API. Resposta simulada pelo Cérebro."

    try:
        model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=system_prompt)
        response = model.generate_content(user_input)
        return response.text
    except Exception as e:
        logger.error(f"Erro Gemini: {e}")
        return "[IA OFFLINE] Falha na conexão. Usando protocolos de segurança."