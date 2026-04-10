from fastapi import APIRouter, Header, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
import os
import random

router = APIRouter(prefix="/v1/education", tags=["Education Module"])

# --- Modelos de Dados (Entrada) ---
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
    metricas: dict  # Ex: {'media': 7.5, 'frequencia': 90}

# --- Segurança ---
async def verify_token(x_service_token: str = Header(..., alias="X-Service-Token")):
    # Pega do .env ou usa default para dev
    expected = os.getenv("SERVICE_TOKEN_SECRET", "segredo_mestre_do_ian_123")
    if x_service_token != expected:
        raise HTTPException(status_code=403, detail="Acesso negado ao Cérebro IO.")

# --- Endpoints ---

@router.post("/exam")
async def generate_exam(req: ExamRequest, token: str = Depends(verify_token)):
    """Gera uma prova estruturada (HTML ou JSON)."""
    
    # Simulação de Inteligência Generativa (Substituir por Gemini no futuro)
    html_content = f"""
    <div class="prova-container font-serif p-8 bg-white shadow-lg rounded-lg">
        <div class="header border-b-2 border-gray-800 pb-4 mb-6 text-center">
            <h2 class="text-2xl font-bold uppercase">{req.tema}</h2>
            <p class="text-sm text-gray-600">Nível: {req.nivel} | Dificuldade: {req.dificuldade.upper()}</p>
        </div>
        
        <div class="questoes space-y-8">
    """
    
    for i in range(1, req.qtd_questoes + 1):
        html_content += f"""
            <div class="questao bg-gray-50 p-4 rounded border border-gray-200">
                <p class="font-bold mb-2 text-gray-800">{i}. Questão sobre {req.tema}:</p>
                <p class="mb-3 text-gray-700">Enunciado contextualizado para {req.nivel}...</p>
                <div class="opcoes ml-4 space-y-2 text-sm text-gray-600">
                    <p class="hover:bg-gray-200 p-1 rounded cursor-pointer">(A) Alternativa plausível</p>
                    <p class="hover:bg-gray-200 p-1 rounded cursor-pointer">(B) Alternativa correta</p>
                    <p class="hover:bg-gray-200 p-1 rounded cursor-pointer">(C) Distrator comum</p>
                    <p class="hover:bg-gray-200 p-1 rounded cursor-pointer">(D) Outra possibilidade</p>
                </div>
            </div>
        """
    
    html_content += "</div><div class='mt-8 text-center text-xs text-gray-400'>Gerado por IO CONSCIOS</div></div>"

    return {
        "status": "success",
        "conteudo": html_content,
        "gabarito": "1-B, 2-C, 3-A...",
        "metadata": {"source": "IO Guardian Module"}
    }

@router.post("/lesson_plan")
async def generate_lesson_plan(req: LessonPlanRequest, token: str = Depends(verify_token)):
    """Cria um roteiro de aula detalhado."""
    html_plano = f"""
    <div class="plano-aula p-6 bg-white rounded shadow-sm border-l-4 border-blue-500">
        <h1 class="text-2xl font-bold text-blue-900 mb-2">{req.tema}</h1>
        <div class="flex flex-wrap gap-4 text-sm text-gray-600 mb-6 bg-gray-100 p-2 rounded">
            <span>📚 <strong>Disciplina:</strong> {req.disciplina}</span>
            <span>🎓 <strong>Nível:</strong> {req.nivel}</span>
            <span>⏱️ <strong>Duração:</strong> {req.duracao}</span>
        </div>
        
        <h3 class="font-bold text-lg mb-2 text-blue-700">Objetivos de Aprendizagem</h3>
        <ul class="list-disc pl-5 mb-6 space-y-1 text-gray-700">
            <li>Compreender os conceitos fundamentais de {req.tema}.</li>
            <li>Desenvolver pensamento crítico através da metodologia {req.metodologia}.</li>
        </ul>

        <h3 class="font-bold text-lg mb-2 text-blue-700">Roteiro da Aula</h3>
        <div class="space-y-4">
            <div class="bg-blue-50 p-3 rounded border border-blue-100">
                <span class="font-bold text-blue-800 block">1. Acolhimento (10min)</span>
                <p class="text-sm">Contextualização do tema com pergunta disparadora.</p>
            </div>
            <div class="bg-blue-50 p-3 rounded border border-blue-100">
                <span class="font-bold text-blue-800 block">2. Desenvolvimento ({req.metodologia})</span>
                <p class="text-sm">Atividade prática em grupos focada na resolução do problema.</p>
            </div>
            <div class="bg-blue-50 p-3 rounded border border-blue-100">
                <span class="font-bold text-blue-800 block">3. Fechamento</span>
                <p class="text-sm">Quiz rápido para validação do conhecimento.</p>
            </div>
        </div>
    </div>
    """
    return {"status": "success", "conteudo": html_plano}

@router.post("/activity")
async def generate_activity(req: ActivityRequest, token: str = Depends(verify_token)):
    tipo = "Jogo Educativo" if req.ludico else "Lista de Exercícios"
    html_ativ = f"""
    <div class="atividade border-2 border-dashed border-indigo-300 p-6 rounded-xl bg-indigo-50 text-center">
        <h2 class="text-xl font-bold mb-2 text-indigo-900">{tipo}: {req.tema}</h2>
        <p class="text-gray-600 mb-6">Atividade pronta para projeção ou impressão.</p>
        <div class="content font-mono text-left bg-white p-4 rounded border shadow-inner text-sm">
            [Conteúdo Gerado pela IA para o nível {req.nivel}]
            <br><br>
            1. Encontre as palavras chaves...
            <br>
            2. Relacione as colunas...
        </div>
    </div>
    """
    return {"status": "success", "conteudo": html_ativ}

@router.post("/analyze_student")
async def analyze_student(req: StudentAnalysisRequest, token: str = Depends(verify_token)):
    """Analisa risco de evasão e desempenho."""
    media = req.metricas.get('media', 0)
    
    if media < 6.0:
        risco = "Alto"
        sugestao = "Ativar protocolo de recuperação e agendar reunião com pais."
        cor = "red"
    elif media < 7.5:
        risco = "Médio"
        sugestao = "Sugerir atividades extras de reforço via portal."
        cor = "yellow"
    else:
        risco = "Baixo"
        sugestao = "Manter acompanhamento e parabenizar."
        cor = "green"

    return {
        "analise_textual": f"O aluno {req.nome} apresenta média {media}. O padrão sugere um risco {risco}.",
        "risco_evasao": risco,
        "sugestao_acao": sugestao,
        "cor_alerta": cor
    }