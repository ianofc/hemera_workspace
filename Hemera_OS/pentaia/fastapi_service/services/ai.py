import os
from google import genai

# Inicializa o cliente com a nova arquitetura do Google GenAI
# Certifique-se de que a variável de ambiente GEMINI_API_KEY está configurada no seu docker-compose.yml ou .env
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def generate_text(prompt: str) -> str:
    """Função base para gerar textos genéricos (Corrigindo o ImportError)"""
    if not api_key:
        return "Erro: Chave da API do Gemini não configurada."
        
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash', # Modelo atualizado e rápido
            contents=prompt,
        )
        return response.text
    except Exception as e:
        print(f"Falha de Conexão PentaIA: {e}")
        return "Erro interno ao processar a inteligência da PentaIA."

def gerar_prova_ia(tema: str, dificuldade: str, contexto: str = "") -> str:
    """Gera uma avaliação baseada no currículo escolar"""
    prompt = f"Atue como um educador focado em validação de conhecimento. Crie uma avaliação sobre {tema} com nível de dificuldade '{dificuldade}'. Contexto adicional: {contexto}"
    return generate_text(prompt)