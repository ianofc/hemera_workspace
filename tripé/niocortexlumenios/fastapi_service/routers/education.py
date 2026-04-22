# niocortex/fastapi_service/routers/education.py

from fastapi import APIRouter, HTTPException, Depends, Header
from pydantic import BaseModel
from typing import List, Optional, Any
import random 

# Simulação do "Core Brain" (No futuro, isso chamará o OpenAI/Gemini real)
# from core.brain import Thinker 

router = APIRouter(prefix="/v1/education", tags=["Guardian: Education"])

# --- Schemas de Entrada (Modelos de Dados) ---

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
    metricas: dict # {media: float, frequencia: float, notas_recentes: list}

# --- Lógica Simulada (Mock Inteligente) ---
# No ambiente real, aqui entraria o 'await Thinker.process(...)'

@router.post("/exam")
async def generate_exam(req: ExamRequest):
    """ Gera uma prova formatada em HTML """
    # Mock sofisticado para validação imediata
    html_content = f"""
    <div class="prova-header">
        <h3>Avaliação de {req.tema}</h3>
        <p><strong>Nível:</strong> {req.nivel} | <strong>Dificuldade:</strong> {req.dificuldade.title()}</p>
    </div>
    <hr class="my-4">
    <div class="questoes space-y-6">
    """
    
    for i in range(1, req.qtd_questoes + 1):
        if "multipla_escolha" in req.tipo_questoes:
            html_content += f"""
            <div class="questao mb-4">
                <p class="font-bold text-gray-800">{i}. (BNCC-mock) Questão sobre {req.tema} focada em análise crítica:</p>
                <p class="text-sm text-gray-600 mb-2">Enunciado contextualizado gerado pela IA...</p>
                <ul class="list-none space-y-1 ml-4 text-sm">
                    <li>(A) Alternativa plausível 1</li>
                    <li>(B) Alternativa correta</li>
                    <li>(C) Distrator comum</li>
                    <li>(D) Outra possibilidade</li>
                </ul>
            </div>
            """
    
    html_content += "</div>"
    
    return {
        "status": "success",
        "conteudo": html_content,
        "gabarito": "1-B, 2-C, 3-A... (Gerado pelo IO Zios AI)",
        "metadata": {"source": "IO Zios AI Guardian Module"}
    }

@router.post("/lesson_plan")
async def generate_lesson_plan(req: LessonPlanRequest):
    """ Gera plano de aula """
    bncc_codes = ["EF0"+str(random.randint(5,9))+"HI"+str(random.randint(10,20)) for _ in range(2)]
    
    html_plano = f"""
    <div class="plano-aula">
        <h2 class="text-xl font-bold text-blue-800">{req.tema}</h2>
        <div class="grid grid-cols-2 gap-4 my-4 text-sm">
            <div><strong>Disciplina:</strong> {req.disciplina}</div>
            <div><strong>Metodologia:</strong> {req.metodologia}</div>
        </div>
        
        <h4 class="font-bold mt-4 border-b">1. Objetivos de Aprendizagem</h4>
        <ul class="list-disc pl-5 mb-4">
            <li>Compreender o conceito fundamental de {req.tema}.</li>
            <li>Relacionar o tema com o cotidiano do aluno ({req.nivel}).</li>
        </ul>

        <h4 class="font-bold mt-4 border-b">2. Roteiro ({req.duracao})</h4>
        <ul class="list-decimal pl-5 space-y-2">
            <li><strong>Introdução (10min):</strong> Contextualização com pergunta disparadora.</li>
            <li><strong>Desenvolvimento (Metodologia {req.metodologia}):</strong> Atividade prática em grupos.</li>
            <li><strong>Fechamento:</strong> Quiz rápido ou mapa mental.</li>
        </ul>
    </div>
    """
    
    return {
        "status": "success",
        "conteudo": html_plano,
        "codigos_bncc": bncc_codes
    }

@router.post("/activity")
async def generate_activity(req: ActivityRequest):
    tipo = "Jogo Educativo" if req.ludico else "Lista de Exercícios"
    
    html_ativ = f"""
    <div class="atividade-box border p-4 rounded bg-gray-50">
        <h3 class="font-bold text-lg mb-2">{tipo}: {req.tema}</h3>
        <p class="mb-4 text-sm text-gray-600">Instruções para o professor aplicar em sala.</p>
        
        <div class="conteudo-pratico bg-white p-4 border rounded">
            {'[Caça-Palavras Gerado]' if req.ludico else '[Lista de 5 Questões Práticas]'}
        </div>
    </div>
    """
    return {"status": "success", "conteudo": html_ativ}

@router.post("/analyze_student")
async def analyze_student(req: StudentAnalysisRequest):
    """ Análise preditiva de risco """
    media = req.metricas['media']
    risco = "Baixo"
    sugestao = "Manter acompanhamento padrão."
    
    if media < 6.0:
        risco = "Alto"
        sugestao = "Ativar protocolo de recuperação e agendar reunião com pais."
    elif media < 7.5:
        risco = "Médio"
        sugestao = "Sugerir atividades extras de reforço via portal."

    return {
        "analise_textual": f"O aluno {req.nome} apresenta desempenho de média {media}. O padrão de notas sugere estabilidade.",
        "risco_evasao": risco,
        "sugestao_acao": sugestao,
        "pontos_fortes": ["Assiduidade", "Participação"], # Mock
        "pontos_atencao": ["Matemática Básica"] # Mock
    }