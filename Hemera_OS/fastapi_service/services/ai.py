# fastapi_service/services/ai.py
import os
import re
import logging
import google.generativeai as genai
from typing import List, Any
from ..schemas import (
    AnalisePedagogicaOutput,
    ProvaGeradaOutput,
    QuestaoItem,
    SourceReference,
    LessonPlanRAGOutput,
    ActivityRAGOutput
)

logger = logging.getLogger("hemera.ai")

# Configuração tolerante a falhas do Gemini API
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
model_initialized = False

if GOOGLE_API_KEY:
    try:
        genai.configure(api_key=GOOGLE_API_KEY)
        model = genai.GenerativeModel(
            'gemini-2.5-flash', 
            generation_config={"response_mime_type": "application/json"}
        )
        model_initialized = True
        logger.info("Modelo Gemini 2.5-flash inicializado com sucesso.")
    except Exception as e:
        logger.error(f"Erro ao inicializar o Gemini API: {str(e)}")
else:
    logger.warning("GOOGLE_API_KEY não configurada. O serviço de IA rodará no modo Mock/Fallback.")

# --- MÉTODOS REAIS DO GEMINI ---

async def gerar_analise_aluno(dados: dict) -> AnalisePedagogicaOutput:
    if not model_initialized:
        # Fallback estático para análises de alunos
        risco = "Alto" if dados['media_atual'] < 6.0 else ("Médio" if dados['media_atual'] < 7.5 else "Baixo")
        sugestao = "Ativar protocolo de recuperação." if risco == "Alto" else "Sugerir atividades extras."
        return AnalisePedagogicaOutput(
            resumo_desempenho=f"O aluno {dados['nome_aluno']} apresenta média {dados['media_atual']} com frequência de {dados['frequencia_percentual']}%.",
            pontos_fortes=["Assiduidade", "Comportamento"],
            pontos_atencao=["Notas recentes abaixo do esperado"],
            sugestoes_acao=[sugestao, "Acompanhamento individual", "Conversar com responsáveis"],
            risco_evasao=risco
        )

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
    try:
        response = await model.generate_content_async(prompt)
        return AnalisePedagogicaOutput.model_validate_json(response.text)
    except Exception as e:
        logger.error(f"Erro na geração da análise do Gemini, usando fallback: {str(e)}")
        # Fallback caso dê erro na API do Google
        return AnalisePedagogicaOutput(
            resumo_desempenho=f"Erro de conexão com a API. Dados básicos: {dados['nome_aluno']} média {dados['media_atual']}.",
            pontos_fortes=["Mapeamento em andamento"],
            pontos_atencao=["Conexão de API temporariamente indisponível"],
            sugestoes_acao=["Reavaliar em instantes"],
            risco_evasao="Baixo"
        )

async def gerar_prova_ia(dados: dict, chunks: List[Any]) -> ProvaGeradaOutput:
    if not model_initialized or os.getenv("HEMERA_FORCE_MOCK", "false").lower() == "true":
        return gerar_prova_fallback(dados, chunks)

    # Grounding das fontes no Prompt
    fontes_texto = ""
    for idx, chunk in enumerate(chunks):
        fontes_texto += f"\n--- FONTE [{idx+1}] ---\nDocumento: {chunk.source}\nPágina: {chunk.page}\nConteúdo:\n{chunk.content}\n"

    prompt = f"""
    Você é o oráculo pedagógico HemeraLM. Crie uma avaliação escolar sobre o tema '{dados['tema']}'.
    Nível de Ensino: {dados['nivel_ensino']}
    Dificuldade: {dados['dificuldade']}
    Quantidade de Questões: {dados['quantidade_questoes']}
    Tipo de Questões: {dados['tipo_questoes']}

    GROUNDING PEDAGÓGICO DE FONTES:
    Abaixo estão trechos da BNCC e de apostilas escolares carregados da base de dados.
    Você deve formular as questões baseando-se estritamente nestes dados, evitando alucinações.
    Se o tema solicitado não puder ser respondido com base nas fontes fornecidas abaixo, crie uma única questão avisando que o tema não foi localizado nas fontes ativas.

    Fontes disponíveis para consulta:
    {fontes_texto}

    Você deve retornar APENAS um JSON válido seguindo exatamente este formato:
    {{
        "titulo_sugerido": "Título da Avaliação",
        "questoes": [
            {{
                "enunciado": "Texto da questão...",
                "alternativas": ["A) ...", "B) ...", "C) ...", "D) ..."] (ou null se for discursiva),
                "resposta_correta": "A" (ou texto da resposta esperada se for discursiva),
                "explicacao": "Explicação didática da resposta...",
                "fontes_ancoradas": [
                    {{
                        "documento": "Nome exato da fonte de onde tirou isso",
                        "pagina": 12,
                        "trecho": "Trecho literal da fonte que comprova/ensina isso"
                    }}
                ]
            }}
        ]
    }}
    """
    try:
        response = await model.generate_content_async(prompt)
        # Validação do schema do Pydantic
        res = ProvaGeradaOutput.model_validate_json(response.text)
        # Injeta os documentos consultados no retorno
        res.documentos_consultados = list(set([c.source for c in chunks]))
        return res
    except Exception as e:
        logger.error(f"Erro na geração da prova no Gemini, usando fallback: {str(e)}")
        return gerar_prova_fallback(dados, chunks)

async def gerar_plano_aula_ia(dados: dict, chunks: List[Any]) -> LessonPlanRAGOutput:
    if not model_initialized or os.getenv("HEMERA_FORCE_MOCK", "false").lower() == "true":
        return gerar_plano_aula_fallback(dados, chunks)

    fontes_texto = ""
    for idx, chunk in enumerate(chunks):
        fontes_texto += f"\n--- FONTE [{idx+1}] ---\nDocumento: {chunk.source}\nPágina: {chunk.page}\nConteúdo:\n{chunk.content}\n"

    prompt = f"""
    Você é o oráculo pedagógico HemeraLM. Crie um Plano de Aula sobre '{dados['tema']}'.
    Disciplina: {dados['disciplina']}
    Nível: {dados['nivel']}
    Duração: {dados['duracao']}
    Metodologia: {dados['metodologia']}

    Fontes de Grounding para embasamento:
    {fontes_texto}

    Gere o plano de aula estruturado em HTML e rastreie quais fontes foram utilizadas para fundamentá-lo.
    Retorne APENAS um JSON válido seguindo exatamente este formato:
    {{
        "tema": "Tema do plano",
        "disciplina": "Disciplina",
        "nivel": "Nível",
        "duracao": "Duração",
        "metodologia": "Metodologia",
        "conteudo_plano_html": "Código HTML do plano contendo objetivos, roteiro passo-a-passo detalhado e fechamento...",
        "habilidades_bncc_associadas": ["EF09HI01", "EF09HI02"] (Códigos BNCC das fontes usadas),
        "fontes_ancoradas": [
            {{
                "documento": "Nome da fonte de origem",
                "pagina": 15,
                "trecho": "Trecho literal da fonte"
            }}
        ]
    }}
    """
    try:
        response = await model.generate_content_async(prompt)
        return LessonPlanRAGOutput.model_validate_json(response.text)
    except Exception as e:
        logger.error(f"Erro na geração do plano de aula no Gemini, usando fallback: {str(e)}")
        return gerar_plano_aula_fallback(dados, chunks)

async def gerar_atividade_ia(dados: dict, chunks: List[Any]) -> ActivityRAGOutput:
    if not model_initialized or os.getenv("HEMERA_FORCE_MOCK", "false").lower() == "true":
        return gerar_atividade_fallback(dados, chunks)

    fontes_texto = ""
    for idx, chunk in enumerate(chunks):
        fontes_texto += f"\n--- FONTE [{idx+1}] ---\nDocumento: {chunk.source}\nPágina: {chunk.page}\nConteúdo:\n{chunk.content}\n"

    prompt = f"""
    Você é o oráculo pedagógico HemeraLM. Crie uma atividade didática sobre '{dados['tema']}'.
    Nível: {dados['nivel']}
    Lúdico: {dados['ludico']} (Se true, faça um jogo ou caça-palavras/desafio, se false faça exercícios práticos)

    Fontes de Grounding para embasamento:
    {fontes_texto}

    Retorne APENAS um JSON válido seguindo exatamente este formato:
    {{
        "tema": "Tema da atividade",
        "nivel": "Nível",
        "ludico": true/false,
        "conteudo_atividade_html": "Código HTML contendo a atividade estruturada para o aluno...",
        "instrucoes_professor": "Orientações didáticas para aplicação...",
        "fontes_ancoradas": [
            {{
                "documento": "Nome da fonte",
                "pagina": 12,
                "trecho": "Trecho literal da fonte"
            }}
        ]
    }}
    """
    try:
        response = await model.generate_content_async(prompt)
        return ActivityRAGOutput.model_validate_json(response.text)
    except Exception as e:
        logger.error(f"Erro na geração da atividade no Gemini, usando fallback: {str(e)}")
        return gerar_atividade_fallback(dados, chunks)


# --- IMPLEMENTAÇÕES DE FALLBACK / TESTE (OFFLINE/ROBUSTO) ---

def gerar_prova_fallback(dados: dict, chunks: List[Any]) -> ProvaGeradaOutput:
    if not chunks:
        # Se nenhuma fonte RAG for encontrada
        return ProvaGeradaOutput(
            titulo_sugerido=f"Avaliação Geral: {dados['tema']}",
            questoes=[
                QuestaoItem(
                    enunciado=f"O assunto '{dados['tema']}' não foi localizado especificamente na base de fontes ativas do HemeraLM. Para fins pedagógicos, descreva o que você entende sobre o tema de forma geral.",
                    alternativas=None,
                    resposta_correta="Resposta pessoal discursiva.",
                    explicacao="Tema ausente na BNCC ou apostilas pré-carregadas.",
                    fontes_ancoradas=[]
                )
            ],
            documentos_consultados=[]
        )

    questoes = []
    docs_consultados = list(set([c.source for c in chunks]))

    for idx, chunk in enumerate(chunks[:dados["quantidade_questoes"]]):
        # Identificar se há menção à Era Vargas ou Guerra Fria para dar enunciados contextualizados
        content_lower = chunk.content.lower()
        
        fonte_ref = SourceReference(
            documento=chunk.source,
            pagina=chunk.page,
            trecho=chunk.content[:150] + "..."
        )

        if "vargas" in content_lower or "clt" in content_lower:
            enunciado = "Getúlio Vargas governou o Brasil entre 1930 e 1945, um período marcado por intensas transformações. Com base nisso e nas fontes do HemeraLM, qual importante marco trabalhista foi outorgado em 1943?"
            alternativas = [
                "A) A Consolidação das Leis do Trabalho (CLT).",
                "B) A instituição do voto feminino apenas.",
                "C) O fechamento total das indústrias nacionais.",
                "D) A abolição do salário mínimo."
            ]
            resposta = "A"
            explicacao = "A CLT foi outorgada em 1943 por Getúlio Vargas durante a fase ditatorial do Estado Novo, centralizando os direitos trabalhistas."
        elif "guerra fria" in content_lower:
            enunciado = "A Guerra Fria (pós-1945) dividiu o planeta sob a chamada 'Ordem Bipolar'. Quais superpotências lideravam essa divisão ideológica global?"
            alternativas = [
                "A) Alemanha e Japão.",
                "B) Estados Unidos (capitalismo) e União Soviética (socialismo).",
                "C) Inglaterra e França.",
                "D) China e Coreia."
            ]
            resposta = "B"
            explicacao = "Os Estados Unidos lideravam o bloco capitalista e a União Soviética liderava o bloco socialista, travando disputas indiretas."
        elif "descolonização" in content_lower:
            enunciado = "O fim da Segunda Guerra Mundial enfraqueceu as nações imperialistas da Europa. O que foi o processo de descolonização afro-asiático?"
            alternativas = [
                "A) O fortalecimento do neocolonialismo inglês na Ásia.",
                "B) A independência política das antigas colônias na África e Ásia em relação às potências europeias.",
                "C) A venda de territórios coloniais para a União Soviética.",
                "D) A fusão de todos os países africanos em uma única federação europeia."
            ]
            resposta = "B"
            explicacao = "O processo permitiu que ex-colônias conquistassem sua independência política aproveitando a fraqueza europeia do pós-guerra."
        elif "energia" in content_lower or "renováveis" in content_lower:
            enunciado = "Fontes de energia são de suma importância para o cotidiano e desenvolvimento industrial. Qual alternativa traz apenas fontes de energia renováveis?"
            alternativas = [
                "A) Carvão mineral e petróleo.",
                "B) Energia solar, eólica e hidrelétrica.",
                "C) Gás natural e urânio.",
                "D) Óleo diesel e xisto betuminoso."
            ]
            resposta = "B"
            explicacao = "Fontes renováveis são as que se regeneram naturalmente em curto prazo, como a luz solar, o vento e a água das hidrelétricas."
        else:
            enunciado = f"Com base na leitura de '{chunk.source}' na página {chunk.page}, assinale a alternativa que condiz com o trecho pedagógico analisado:"
            alternativas = [
                "A) Afirmação verdadeira extraída diretamente das fontes de grounding do HemeraLM.",
                "B) Distrator conceitual incorreto 1.",
                "C) Distrator conceitual incorreto 2.",
                "D) Distrator conceitual incorreto 3."
            ]
            resposta = "A"
            explicacao = f"A opção A está diretamente respaldada pelo texto: '{chunk.content[:70]}...'"

        if dados["tipo_questoes"] == "discursiva":
            questoes.append(
                QuestaoItem(
                    enunciado=enunciado.replace("qual importante marco", "descreva o importante marco").replace("Quais superpotências lideravam", "quais superpotências lideravam"),
                    alternativas=None,
                    resposta_correta=explicacao,
                    explicacao="Gabarito oficial de correção para o professor.",
                    fontes_ancoradas=[fonte_ref]
                )
            )
        else:
            questoes.append(
                QuestaoItem(
                    enunciado=enunciado,
                    alternativas=alternativas,
                    resposta_correta=resposta,
                    explicacao=explicacao,
                    fontes_ancoradas=[fonte_ref]
                )
            )

    # Garante a quantidade exata de questões pedidas
    while len(questoes) < dados["quantidade_questoes"]:
        c = chunks[0]
        fonte_ref = SourceReference(documento=c.source, pagina=c.page, trecho=c.content[:100])
        questoes.append(
            QuestaoItem(
                enunciado=f"Questão extra integradora sobre o material '{c.source}' (página {c.page}): explique sua importância.",
                alternativas=None,
                resposta_correta="Resposta baseada no conteúdo geral da aula.",
                explicacao="Questão integradora complementar.",
                fontes_ancoradas=[fonte_ref]
            )
        )

    return ProvaGeradaOutput(
        titulo_sugerido=f"Avaliação de Aprendizagem: {dados['tema']}",
        questoes=questoes[:dados["quantidade_questoes"]],
        documentos_consultados=docs_consultados
    )

def gerar_plano_aula_fallback(dados: dict, chunks: List[Any]) -> LessonPlanRAGOutput:
    fontes_ancoradas = [
        SourceReference(documento=c.source, pagina=c.page, trecho=c.content[:150] + "...")
        for c in chunks
    ]
    
    habilidades_bncc = []
    for c in chunks:
        # Procurar no texto códigos no formato EF##XX##
        matches = re.findall(r"EF\d{2}[A-Z]{2}\d{2}", c.content)
        habilidades_bncc.extend(matches)
        
    if not habilidades_bncc:
        habilidades_bncc = ["EF09HI01"] if "história" in dados["disciplina"].lower() else ["EF08CI01"]
        
    habilidades_bncc = list(set(habilidades_bncc))
    
    html_plano = f"""
    <div class="plano-aula-rag bg-blue-50 p-6 rounded border border-blue-200">
        <h2 class="text-xl font-bold text-blue-900">Roteiro de Aula: {dados['tema']}</h2>
        <div class="my-3 text-sm">
            <p><strong>Disciplina:</strong> {dados['disciplina']} | <strong>Nível:</strong> {dados['nivel']}</p>
            <p><strong>Metodologia:</strong> {dados['metodologia']} | <strong>Duração:</strong> {dados['duracao']}</p>
        </div>
        
        <h3 class="font-semibold text-blue-800 mt-4">1. Habilidades de Grounding da BNCC</h3>
        <ul class="list-disc pl-5">
            {"".join([f"<li><strong>{h}</strong>: Conectado à base curricular nacional.</li>" for h in habilidades_bncc])}
        </ul>
        
        <h3 class="font-semibold text-blue-800 mt-4">2. Conteúdo e Fundamentação</h3>
        <p class="text-sm">Baseado nas diretrizes e apostilas selecionadas via RAG:</p>
        {"".join([f"<blockquote class='border-l-4 border-blue-500 pl-3 italic my-3 text-sm bg-white p-2'>{c.content[:200]}... <br><span class='text-xs text-gray-500'>({c.source}, p. {c.page})</span></blockquote>" for c in chunks])}
        
        <h3 class="font-semibold text-blue-800 mt-4">3. Roteiro Cronológico ({dados['duracao']})</h3>
        <ol class="list-decimal pl-5 space-y-2 text-sm">
            <li><strong>Introdução (15% do tempo):</strong> Discussão e problematização com base nas fontes.</li>
            <li><strong>Desenvolvimento (70% do tempo):</strong> Atividade com a metodologia '{dados['metodologia']}'.</li>
            <li><strong>Fechamento (15% do tempo):</strong> Ancoragem final e resolução de dúvidas.</li>
        </ol>
    </div>
    """
    
    return LessonPlanRAGOutput(
        tema=dados['tema'],
        disciplina=dados['disciplina'],
        nivel=dados['nivel'],
        duracao=dados['duracao'],
        metodologia=dados['metodologia'],
        conteudo_plano_html=html_plano.strip(),
        habilidades_bncc_associadas=habilidades_bncc,
        fontes_ancoradas=fontes_ancoradas
    )

def gerar_atividade_fallback(dados: dict, chunks: List[Any]) -> ActivityRAGOutput:
    fontes_ancoradas = [
        SourceReference(documento=c.source, pagina=c.page, trecho=c.content[:150] + "...")
        for c in chunks
    ]
    
    tipo_ativ = "Dinâmica de Grupo Lúdica" if dados['ludico'] else "Ficha de Exercícios Dirigidos"
    
    html_ativ = f"""
    <div class="atividade-rag p-6 border border-green-200 rounded bg-green-50">
        <h2 class="text-xl font-bold text-green-900">{tipo_ativ}: {dados['tema']} ({dados['nivel']})</h2>
        <div class="my-4 p-4 bg-white border border-green-100 rounded text-sm">
            <p class="font-semibold mb-2">Desafio Didático:</p>
            <p>Utilize as fontes bibliográficas recomendadas (páginas: {', '.join([str(c.page) for c in chunks])}) para resolver as questões a seguir de forma argumentativa.</p>
        </div>
        <div class="conteudo-pratico text-sm">
            <p><strong>Questão 1:</strong> Com base no material didático e no tema de {dados['tema']}, elabore uma síntese de suas principais consequências históricas ou científicas.</p>
        </div>
    </div>
    """
    
    instrucoes = f"O professor deve agrupar a classe, distribuir os trechos das apostilas e orientar os alunos na busca pelos tópicos: {', '.join([c.source for c in chunks])}."
    
    return ActivityRAGOutput(
        tema=dados['tema'],
        nivel=dados['nivel'],
        ludico=dados['ludico'],
        conteudo_atividade_html=html_ativ.strip(),
        instrucoes_professor=instrucoes,
        fontes_ancoradas=fontes_ancoradas
    )