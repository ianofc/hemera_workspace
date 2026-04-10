# fastapi_service/services/ai.py
import os
import google.generativeai as genai
import json
from ..schemas import AnalisePedagogicaOutput, ProvaGeradaOutput

# Configuração
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY não encontrada nas variáveis de ambiente.")

genai.configure(api_key=GOOGLE_API_KEY)

# Modelo Otimizado para JSON (Usando 2.5-flash conforme seu log)
model = genai.GenerativeModel(
    'gemini-2.5-flash', 
    generation_config={"response_mime_type": "application/json"}
)

async def gerar_analise_aluno(dados: dict) -> AnalisePedagogicaOutput:
    prompt = f"""
    Atue como um Coordenador Pedagógico sênior. Analise os dados deste aluno:
    Aluno: {dados['nome_aluno']} ({dados['turma']})
    Média: {dados['media_atual']}
    Frequência: {dados['frequencia_percentual']}%
    Histórico Notas: {dados['historico_notas']}
    Obs: {dados['observacoes_recentes']}

    Gere um relatório JSON estrito seguindo este schema:
    {{
        "resumo_desempenho": "texto",
        "pontos_fortes": ["item1", "item2"],
        "pontos_atencao": ["item1", "item2"],
        "sugestoes_acao": ["acao1", "acao2", "acao3"],
        "risco_evasao": "Baixo/Médio/Alto"
    }}
    """
    
    response = await model.generate_content_async(prompt)
    # O Pydantic fará a validação final se o JSON está correto
    return AnalisePedagogicaOutput.model_validate_json(response.text)

async def gerar_prova_ia(dados: dict) -> ProvaGeradaOutput:
    prompt = f"""
    Crie uma prova escolar sobre: {dados['tema']}
    Nível: {dados['nivel_ensino']}
    Dificuldade: {dados['dificuldade']}
    Qtd: {dados['quantidade_questoes']}
    Tipo: {dados['tipo_questoes']}

    Retorne APENAS JSON válido neste formato:
    {{
        "titulo_sugerido": "Título da Prova",
        "questoes": [
            {{
                "enunciado": "Pergunta...",
                "alternativas": ["A) ...", "B) ..."] (ou null se discursiva),
                "resposta_correta": "A",
                "explicacao": "Breve explicação"
            }}
        ]
    }}
    """
    
    response = await model.generate_content_async(prompt)
    return ProvaGeradaOutput.model_validate_json(response.text)