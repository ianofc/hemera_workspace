import os
import google.generativeai as genai
from django.conf import settings
import traceback
import time

# Configuração da API Key
api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

def get_ai_response(messages, temperature=0.7):
    """
    Wrapper para o Google Gemini focado no modelo 2.5-flash (Disponível na sua conta).
    """
    if not api_key:
        return "⚠️ ERRO CONFIG: GOOGLE_API_KEY não encontrada."

    # Prepara o histórico
    chat_history = []
    last_user_message = ""
    system_instruction = None

    try:
        # 1. Separa System, History e Mensagem Atual
        for msg in messages:
            role = msg.get('role')
            content = msg.get('content', '')
            
            if not content and role != 'model': continue

            if role == 'system':
                system_instruction = content
            elif role == 'user':
                chat_history.append({"role": "user", "parts": [content]})
                last_user_message = content
            elif role in ['assistant', 'model']:
                chat_history.append({"role": "model", "parts": [content]})

        # Remove a última mensagem do usuário do histórico (pois ela será o prompt atual)
        if chat_history and chat_history[-1]['role'] == 'user':
            chat_history.pop()
        
        if not last_user_message:
            return "Não entendi. Pode repetir?"

        # 2. Definição do Modelo (2.5 Confirmado pelo seu log)
        model_name = "gemini-2.5-flash"
        
        print(f"🤖 IA: Iniciando chat com {model_name}...")

        model = genai.GenerativeModel(
            model_name=model_name,
            system_instruction=system_instruction,
            generation_config={"temperature": temperature}
        )

        chat = model.start_chat(history=chat_history)
        response = chat.send_message(last_user_message)
        return response.text

    except Exception as e:
        error_msg = str(e)
        
        # Tratamento específico para Cota Excedida (429)
        if "429" in error_msg or "Quota exceeded" in error_msg:
            print("⏳ Cota excedida. Aguardando 2s para tentar fallback...")
            time.sleep(2)
            return "Minha capacidade de processamento está sobrecarregada no momento. Tente novamente em alguns segundos."

        # Log genérico
        print("\n" + "="*50)
        print("❌ ERRO NO GEMINI AI:")
        traceback.print_exc()
        print("="*50 + "\n")
        
        return f"⚠️ Erro técnico na IA: {error_msg}"

# CLASSE LEGADA (Mantida para compatibilidade)
class AIClient:
    def __init__(self):
        self.api_key = api_key

    @staticmethod
    def check_proactive_thought(user, path, meta):
        """Simulação para evitar erro na view api_check_zios"""
        return {"should_speak": False}

    @staticmethod
    def chat_universal(message, user):
        """Wrapper para o chat universal"""
        return {"reply": get_ai_response([{'role': 'user', 'content': message}])}

    def ask(self, prompt, context=None):
        messages = []
        if context:
            messages.append({'role': 'system', 'content': context})
        messages.append({'role': 'user', 'content': prompt})
        return get_ai_response(messages)

    def generate_content(self, prompt):
        return get_ai_response([{'role': 'user', 'content': prompt}])