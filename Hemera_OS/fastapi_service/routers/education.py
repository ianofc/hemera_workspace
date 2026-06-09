# fastapi_service/routers/education.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import random

from ..services.rag import rag_engine
from ..services import ai
from ..schemas import AlunoPerformanceInput

router = APIRouter(prefix="/v1/education", tags=["Guardian: Education"])

# --- Schemas de Entrada (Mantidos para compatibilidade retroativa) ---

class ExamRequest(BaseModel):
    tema: str
    nivel: str
    dificuldade: str = "medio"
    qtd_questoes: int = 5
    tipo_questoes: List[str] = ["multipla_escolha"]
    contexto_bncc: bool = True

class LessonPlanRequest(BaseModel):
    tema: str
    disciplina: str
    nivel: str
    duracao: str
    metodologia: str

class ActivityRequest(BaseModel):
    tema: str
    nivel: str
    ludico: bool = False

class StudentAnalysisRequest(BaseModel):
    nome: str
    turma: str
    metricas: dict  # {media: float, frequencia: float, notas_recentes: list}


# --- Rota de Geração de Provas Inteligentes (RAG Grounded) ---

@router.post("/exam")
async def generate_exam(req: ExamRequest):
    """
    Gera uma avaliação estruturada e personalizada ancorada nas diretrizes e apostilas (RAG).
    Retorna tanto o HTML renderizado quanto a estrutura completa com fontes rastreadas.
    """
    # 1. Recuperar chunks relevantes de conhecimento usando RAG
    query_busca = f"{req.tema} {req.nivel}"
    chunks = rag_engine.retrieve(query=query_busca, limit=req.qtd_questoes)

    # 2. Mapear para o formato do serviço de IA
    tipo_q = "discursiva" if "discursiva" in req.tipo_questoes else "multipla_escolha"
    dados_ia = {
        "tema": req.tema,
        "nivel_ensino": req.nivel,
        "dificuldade": req.dificuldade,
        "quantidade_questoes": req.qtd_questoes,
        "tipo_questoes": tipo_q
    }

    # 3. Chamar IA (Gemini com Grounding RAG)
    prova_gerada = await ai.gerar_prova_ia(dados_ia, chunks)

    # 4. Construir o HTML a partir da prova gerada pela IA
    html_content = f"""
    <div class="prova-header p-4 bg-gray-50 border-b border-gray-200">
        <h3 class="text-xl font-bold text-gray-800">{prova_gerada.titulo_sugerido}</h3>
        <p class="text-sm text-gray-600"><strong>Nível:</strong> {req.nivel} | <strong>Dificuldade:</strong> {req.dificuldade.title()}</p>
    </div>
    <hr class="my-4">
    <div class="questoes space-y-6 p-4">
    """

    for i, q in enumerate(prova_gerada.questoes, 1):
        html_content += f"""
        <div class="questao mb-6 border-l-4 border-blue-500 pl-4">
            <p class="font-bold text-gray-800">{i}. {q.enunciado}</p>
        """
        
        if q.alternativas:
            html_content += """
            <ul class="list-none space-y-1 ml-4 my-2 text-sm">
            """
            for alt in q.alternativas:
                html_content += f"<li>{alt}</li>"
            html_content += "</ul>"
            
        html_content += f"""
            <div class="resposta-detalhada mt-2 text-xs text-green-700 bg-green-50 p-2 rounded">
                <strong>Gabarito Esperado:</strong> {q.resposta_correta} <br>
                <strong>Explicação:</strong> {q.explicacao}
            </div>
        """
        
        if q.fontes_ancoradas:
            html_content += """
            <div class="fontes-rastreadas mt-1 text-[10px] text-gray-500">
                <strong>Ancoragem de Fontes RAG:</strong>
            """
            for f in q.fontes_ancoradas:
                html_content += f"<span>[{f.documento}, p. {f.pagina}] </span>"
            html_content += "</div>"
            
        html_content += "</div>"

    html_content += "</div>"

    # Formatar o texto do gabarito para resposta rápida
    gabarito_elementos = []
    for idx, q in enumerate(prova_gerada.questoes, 1):
        gabarito_elementos.append(f"{idx}-{q.resposta_correta}")
    gabarito_resumido = ", ".join(gabarito_elementos) + " (Ancorado no HemeraLM RAG)"

    return {
        "status": "success",
        "conteudo": html_content.strip(),
        "gabarito": gabarito_resumido,
        "prova_estruturada": prova_gerada.model_dump(),
        "metadata": {
            "source": "HemeraLM Pedagogical RAG",
            "documentos_consultados": prova_gerada.documentos_consultados
        }
    }


# --- Rota de Geração de Planos de Aula (RAG Grounded) ---

@router.post("/lesson_plan")
async def generate_lesson_plan(req: LessonPlanRequest):
    """
    Gera um plano de aula detalhado ancorado nas diretrizes curriculares (BNCC) e apostilas via RAG.
    """
    query_busca = f"{req.disciplina} {req.tema} {req.nivel}"
    chunks = rag_engine.retrieve(query=query_busca, limit=3)

    dados_ia = {
        "tema": req.tema,
        "disciplina": req.disciplina,
        "nivel": req.nivel,
        "duracao": req.duracao,
        "metodologia": req.metodologia
    }

    plano_aula = await ai.gerar_plano_aula_ia(dados_ia, chunks)

    return {
        "status": "success",
        "conteudo": plano_aula.conteudo_plano_html,
        "codigos_bncc": plano_aula.habilidades_bncc_associadas,
        "fontes_ancoradas": [f.model_dump() for f in plano_aula.fontes_ancoradas],
        "plano_estruturado": plano_aula.model_dump()
    }


# --- Rota de Geração de Atividades Didáticas (RAG Grounded) ---

@router.post("/activity")
async def generate_activity(req: ActivityRequest):
    """
    Gera atividades pedagógicas lúdicas ou exercícios estruturados com grounding de apostilas.
    """
    query_busca = f"{req.tema} {req.nivel}"
    chunks = rag_engine.retrieve(query=query_busca, limit=3)

    dados_ia = {
        "tema": req.tema,
        "nivel": req.nivel,
        "ludico": req.ludico
    }

    atividade = await ai.gerar_atividade_ia(dados_ia, chunks)

    return {
        "status": "success",
        "conteudo": atividade.conteudo_atividade_html,
        "instrucoes_professor": atividade.instrucoes_professor,
        "fontes_ancoradas": [f.model_dump() for f in atividade.fontes_ancoradas],
        "atividade_estruturada": atividade.model_dump()
    }


# --- Rota de Análise de Desempenho do Aluno ---

@router.post("/analyze_student")
async def analyze_student(req: StudentAnalysisRequest):
    """
    Analisa métricas de notas, faltas e histórico escolar de um estudante gerando um laudo coordenador.
    """
    dados_ia = {
        "nome_aluno": req.nome,
        "turma": req.turma,
        "media_atual": req.metricas.get("media", 0.0),
        "frequencia_percentual": req.metricas.get("frequencia", 100.0),
        "historico_notas": req.metricas.get("notas_recentes", []),
        "observacoes_recentes": req.metricas.get("observacoes", [])
    }

    analise_res = await ai.gerar_analise_aluno(dados_ia)

    return {
        "status": "success",
        "analise_textual": analise_res.resumo_desempenho,
        "risco_evasao": analise_res.risco_evasao,
        "sugestao_acao": ", ".join(analise_res.sugestoes_acao),
        "pontos_fortes": analise_res.pontos_fortes,
        "pontos_atencao": analise_res.pontos_atencao,
        "analise_estruturada": analise_res.model_dump()
    }