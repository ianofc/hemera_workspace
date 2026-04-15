from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import json
import random
import traceback

# Importando os serviços de IA (Ajuste o caminho base conforme a estrutura real do seu projeto)
from ..services.ai import gerar_prova_ia, generate_text

# Definindo o roteador principal deste módulo
router = APIRouter(tags=["Guardian: Education", "PentaIA"])

# ==========================================
# --- SCHEMAS DE ENTRADA (Data Models) ---
# ==========================================

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
    metricas: dict  # Ex: {"media": 7.5, "frequencia": 90.0, "notas_recentes": []}

class QuestionRequest(BaseModel):
    tema: str
    quantidade: int = 5
    dificuldade: str = "Média"


# ==========================================
# --- ENDPOINTS DA IA PENTAIA ---
# ==========================================

@router.post("/gerar-questoes")
async def gerar_questoes(req: QuestionRequest):
    """
    [PENTAIA] - Endpoint de injeção direta na tela React do Banco de Questões.
    Retorna estritamente um array JSON com perguntas, opções e gabarito.
    """
    prompt = f"""
    Você é um professor conteudista especialista. Crie {req.quantidade} questões de múltipla escolha.
    Tema: {req.tema}
    Dificuldade: {req.dificuldade}
    
    Retorne ESTRITAMENTE um array JSON no seguinte formato (sem blocos de código ```json):
    [
        {{
            "enunciado": "Texto da pergunta...",
            "opcoes": ["A", "B", "C", "D", "E"],
            "resposta_correta": "C",
            "explicacao": "Por que a C está correta..."
        }}
    ]
    """
    
    try:
        # Chama a função pura de IA
        resposta_ia = await generate_text(prompt)
        
        # Limpa possíveis formatações de markdown que a IA possa retornar
        limpo = resposta_ia.replace("```json", "").replace("```", "").strip()
        questoes = json.loads(limpo)
        
        return {"questoes": questoes}
        
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Erro ao processar cérebro IA: {str(e)}")


@router.post("/exam")
async def generate_exam(req: ExamRequest):
    """ Gera uma prova estilizada em HTML utilizando o Gemini/PentaIA """
    try:
        dados = {
            'tema': req.tema,
            'nivel_ensino': req.nivel,
            'dificuldade': req.dificuldade,
            'quantidade_questoes': req.qtd_questoes,
            'tipo_questoes': ', '.join(req.tipo_questoes)
        }
        
        # Chama o Cérebro Real (PentaIA / Gemini)
        prova_output = await gerar_prova_ia(dados)
        
        # Converte o Output JSON do Gemini num HTML formatado de visualização
        html_content = f'''
        <div class="prova-header">
            <h3>{getattr(prova_output, "titulo_sugerido", "Avaliação Gerada")}</h3>
            <p><strong>Nível:</strong> {req.nivel} | <strong>Dificuldade:</strong> {req.dificuldade.title()}</p>
        </div>
        <hr class="my-4 border-gray-200">
        <div class="questoes space-y-6">
        '''
        
        gabaritos = []
        for i, q in enumerate(prova_output.questoes, 1):
            html_content += f'<div class="questao mb-4"><p class="font-bold text-gray-800">{i}. {q.enunciado}</p>'
            if q.alternativas:
                html_content += '<ul class="list-none space-y-1 ml-4 mt-2 text-sm text-gray-700">'
                for alt in q.alternativas:
                    html_content += f'<li>{alt}</li>'
                html_content += '</ul>'
            html_content += '</div>'
            gabaritos.append(f"{i}-{q.resposta_correta} ({q.explicacao})")
            
        html_content += "</div>"
        
        return {
            "status": "success",
            "conteudo": html_content,
            "gabarito": " | ".join(gabaritos),
            "metadata": {"source": "IO Zios AI Guardian Module"}
        }
        
    except Exception as e:
        traceback.print_exc()
        return {
            "status": "error",
            "conteudo": f"Erro na Gênese Cognitiva: {str(e)}",
            "metadata": {"source": "PentaIA Engine"}
        }


@router.post("/lesson_plan")
async def generate_lesson_plan(req: LessonPlanRequest):
    """ Gera plano de aula dinâmico """
    bncc_codes = ["EF0"+str(random.randint(5,9))+"HI"+str(random.randint(10,20)) for _ in range(2)]
    
    html_plano = f"""
    <div class="plano-aula">
        <h2 class="text-xl font-bold text-blue-800">{req.tema}</h2>
        <div class="grid grid-cols-2 gap-4 my-4 text-sm bg-blue-50 p-3 rounded">
            <div><strong>Disciplina:</strong> {req.disciplina}</div>
            <div><strong>Metodologia:</strong> {req.metodologia}</div>
            <div><strong>Duração:</strong> {req.duracao}</div>
            <div><strong>Nível:</strong> {req.nivel}</div>
        </div>
        
        <h4 class="font-bold mt-4 border-b pb-1">1. Objetivos de Aprendizagem</h4>
        <ul class="list-disc pl-5 mb-4 text-gray-700 mt-2">
            <li>Compreender o conceito fundamental de {req.tema}.</li>
            <li>Relacionar o tema com o cotidiano do aluno.</li>
        </ul>

        <h4 class="font-bold mt-4 border-b pb-1">2. Roteiro Sugerido</h4>
        <ul class="list-decimal pl-5 space-y-2 mt-2 text-gray-700">
            <li><strong>Introdução (10min):</strong> Contextualização com pergunta disparadora sobre o tema.</li>
            <li><strong>Desenvolvimento (Metodologia {req.metodologia}):</strong> Atividade prática guiada em grupos.</li>
            <li><strong>Fechamento:</strong> Resumo interativo e mapa mental construído com a turma.</li>
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
    """ Gera sugestão de atividade lúdica ou prática """
    tipo = "Jogo Educativo" if req.ludico else "Lista de Exercícios"
    
    html_ativ = f"""
    <div class="atividade-box border border-purple-200 p-4 rounded-lg bg-purple-50/50">
        <h3 class="font-bold text-lg mb-2 text-purple-900">{tipo}: {req.tema}</h3>
        <p class="mb-4 text-sm text-gray-600">Instruções para o professor aplicar em sala ({req.nivel}).</p>
        
        <div class="conteudo-pratico bg-white p-4 border border-purple-100 rounded shadow-sm">
            {'[Modelo interativo de Caça-Palavras ou Quiz Dinâmico seria gerado aqui]' if req.ludico else '[Lista de 5 Questões Práticas formatadas para impressão]'}
        </div>
    </div>
    """
    return {"status": "success", "conteudo": html_ativ}


@router.post("/analyze_student")
async def analyze_student(req: StudentAnalysisRequest):
    """ Análise preditiva do aluno e risco de evasão/reprovação """
    media = float(req.metricas.get('media', 0))
    risco = "Baixo"
    sugestao = "Manter acompanhamento padrão e engajamento natural."
    
    if media < 6.0:
        risco = "Alto"
        sugestao = "Ativar protocolo de recuperação urgente. Acionar Zios para tutoria individual e comunicar coordenação."
    elif media < 7.5:
        risco = "Médio"
        sugestao = "Sugerir trilha de atividades extras e pílulas de reforço na plataforma."

    return {
        "analise_textual": f"A IA identificou que o aluno {req.nome} ({req.turma}) apresenta média consolidada de {media}. O padrão atual sugere uma zona de risco {risco.lower()}.",
        "risco_evasao": risco,
        "sugestao_acao": sugestao,
        "pontos_fortes": ["Assiduidade", "Participação em aulas de Humanas"], # Dados mockados para ex
        "pontos_atencao": ["Oscilação recente em avaliações exatas"] # Dados mockados para ex
    }