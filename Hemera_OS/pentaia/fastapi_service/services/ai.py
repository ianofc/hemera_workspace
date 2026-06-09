import os
import json
from google import genai
from google.genai import types
from ..schemas import ProvaGeradaOutput, QuestaoItem

api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")

async def generate_text(prompt: str) -> str:
    """Função base para gerar textos genéricos de forma assíncrona"""
    if not api_key:
        return "Erro: Chave da API do Gemini não configurada na PentaIA."
        
    try:
        client = genai.Client(api_key=api_key)
        response = await client.aio.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        return response.text
    except Exception as e:
        print(f"Falha de Conexão PentaIA: {e}")
        return "Erro interno ao processar a inteligência da PentaIA."

async def gerar_prova_ia(dados: dict) -> ProvaGeradaOutput:
    """Gera uma avaliação estruturada baseada no currículo escolar"""
    tema = dados.get('tema')
    nivel = dados.get('nivel_ensino', 'Ensino Fundamental')
    dificuldade = dados.get('dificuldade', 'medio')
    quantidade = dados.get('quantidade_questoes', 5)
    tipo = dados.get('tipo_questoes', 'multipla_escolha')

    prompt = f"""
    Atue como um educador focado em validação de conhecimento e conformidade com a BNCC.
    Crie uma avaliação de {nivel} sobre {tema} com nível de dificuldade '{dificuldade}'.
    A prova deve conter {quantidade} questões do tipo '{tipo}'.
    Retorne a resposta estritamente estruturada em JSON contendo 'titulo_sugerido' e a lista de 'questoes' com 'enunciado', 'alternativas' (se aplicável), 'resposta_correta' e 'explicacao'.
    """

    if not api_key:
        return ProvaGeradaOutput(
            titulo_sugerido=f"Avaliação de {tema} (Mock)",
            questoes=[
                QuestaoItem(
                    enunciado=f"O que caracteriza o conceito fundamental de {tema}?",
                    alternativas=["Alternativa A", "Alternativa B", "Alternativa C", "Alternativa D"],
                    resposta_correta="Alternativa A",
                    explicacao="Explicação padrão do fallback."
                )
            ]
        )

    try:
        client = genai.Client(api_key=api_key)
        response = await client.aio.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=ProvaGeradaOutput,
            )
        )
        data = json.loads(response.text)
        return ProvaGeradaOutput(**data)
    except Exception as e:
        print(f"Falha ao gerar prova estruturada via Gemini: {e}")
        return ProvaGeradaOutput(
            titulo_sugerido=f"Avaliação de {tema} (Fallback)",
            questoes=[
                QuestaoItem(
                    enunciado=f"Qual das seguintes alternativas melhor descreve o tema {tema}?",
                    alternativas=["Opção A", "Opção B", "Opção C", "Opção D"],
                    resposta_correta="Opção A",
                    explicacao=f"Esta é a explicação padrão de segurança sobre {tema}."
                )
            ]
        )

async def gerar_recomendacao_cursos_tas(perfil_usuario: dict) -> list:
    """Gera sugestões de cursos baseando-se no comportamento e preferências do aluno (Accubens/Dopamina)"""
    prompt = f"""
    Você é o TAS (Total Analysis System), o motor de recomendação bio-inspirado do Hemera OS.
    Com base nas preferências e notas do perfil do usuário fornecido abaixo, recomende 3 cursos ou caminhos de aprendizagem
    no Moodle/Hemera Lyceum que se alinhem com o que ele mais gosta ou precisa reforçar.
    
    Perfil do Usuário:
    {perfil_usuario}
    
    Retorne a resposta estritamente como um array JSON (sem blocos de código markdown) no formato:
    [
        {{
            "titulo": "Nome do Curso",
            "categoria": "Categoria do Curso (Ex: Matemática, Tecnologia, História)",
            "match_score": 95,
            "descricao": "Justificativa curta da recomendação de acordo com as preferências do perfil."
        }}
    ]
    """
    if not api_key:
        return [
            {"titulo": "Introdução à Agroecologia e Robótica Livre", "categoria": "Tecnologia", "match_score": 90, "descricao": "Com base no seu perfil prático e diário de campo no Héfesto."},
            {"titulo": "História Geral e Organizações Sociais", "categoria": "Humanas", "match_score": 85, "descricao": "Ideal para expandir seus conhecimentos da Segunda Mente em história."},
            {"titulo": "Gamificação no Ensino Superior com Olimpo", "categoria": "Pedagogia", "match_score": 80, "descricao": "Recomendado para entender as mecânicas de XP e engajamento."}
        ]
    try:
        client = genai.Client(api_key=api_key)
        response = await client.aio.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )
        return json.loads(response.text)
    except Exception as e:
        print(f"Erro ao gerar recomendações do TAS: {e}")
        return [
            {"titulo": "Introdução à Agroecologia e Robótica Livre", "categoria": "Tecnologia", "match_score": 90, "descricao": "Com base no seu perfil prático e diário de campo no Héfesto."}
        ]

async def buscar_noticias_externas_iris() -> list:
    """Varre/Gera notícias recentes EdTech fora do projeto para o jornal da IRIS"""
    prompt = """
    Você é o IRIS (Integrated Real-time Insight System), o motor de inteligência e percepção externa da PentaIA.
    Elabore ou resuma 3 notícias reais ou altamente verossímeis sobre educação, tecnologia, novas tendências de IA pedagógica,
    regulamentações do MEC ou diretrizes da BNCC no Brasil e no mundo.
    
    Retorne a resposta estritamente como um array JSON (sem blocos de código markdown) no formato:
    [
        {{
            "titulo": "Título da Notícia",
            "fonte": "Fonte jornalística (Ex: G1, MEC, Forbes Education)",
            "snippet": "Breve resumo de duas frases sobre a notícia.",
            "url": "https://exemplo.com"
        }}
    ]
    """
    if not api_key:
        return [
            {"titulo": "MEC aprova novas diretrizes para o uso de IA Generativa nas salas de aula brasileiras", "fonte": "MEC Portal", "snippet": "A regulamentação visa garantir o uso ético e seguro de assistentes pedagógicos virtuais para o ensino básico.", "url": "https://mec.gov.br"},
            {"titulo": "Como o aprendizado ativo está transformando o desempenho escolar em exatas", "fonte": "Educação em Foco", "snippet": "Novas pesquisas comprovaram que metodologias ativas aumentam em 20% a retenção de conceitos matemáticos.", "url": "https://educacaoemfoco.com"},
            {"titulo": "O crescimento global de EdTechs focadas em micro-learning para o Ensino Médio", "fonte": "Forbes Education", "snippet": "Plataformas de pílulas de conhecimento vêm crescendo 35% ao ano como reforço pós-pandemia.", "url": "https://forbes.com"}
        ]
    try:
        client = genai.Client(api_key=api_key)
        response = await client.aio.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )
        return json.loads(response.text)
    except Exception as e:
        print(f"Erro ao buscar notícias externas via IRIS: {e}")
        return [
            {"titulo": "MEC aprova novas diretrizes para o uso de IA Generativa nas salas de aula brasileiras", "fonte": "MEC Portal", "snippet": "A regulamentação visa garantir o uso ético e seguro de assistentes pedagógicos virtuais para o ensino básico.", "url": "https://mec.gov.br"}
        ]