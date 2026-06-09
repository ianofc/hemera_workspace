# fastapi_service/schemas.py
from pydantic import BaseModel, Field
from typing import List, Optional

# --- ANÁLISE DE DESEMPENHO ---

class AlunoPerformanceInput(BaseModel):
    nome_aluno: str
    turma: str
    media_atual: float
    frequencia_percentual: float
    historico_notas: List[float]
    observacoes_recentes: List[str] = []

class AnalisePedagogicaOutput(BaseModel):
    resumo_desempenho: str = Field(description="Visão geral em 1 parágrafo")
    pontos_fortes: List[str]
    pontos_atencao: List[str]
    sugestoes_acao: List[str] = Field(description="3 ações práticas para o professor")
    risco_evasao: str = Field(description="Baixo, Médio ou Alto")

# --- ANCORAGEM DE FONTES (RAG) ---

class SourceReference(BaseModel):
    documento: str = Field(description="Nome do documento ou apostila de origem")
    pagina: int = Field(description="Página de onde a informação foi extraída")
    trecho: str = Field(description="Trecho literal do documento usado como fonte")

# --- GERADOR DE PROVAS ---

class GerarProvaInput(BaseModel):
    tema: str
    nivel_ensino: str = Field(description="Ex: 9º Ano, Ensino Médio")
    quantidade_questoes: int = 5
    tipo_questoes: str = Field(default="multipla_escolha", description="'multipla_escolha' ou 'discursiva'")
    dificuldade: str = "medio"
    usar_rag: bool = Field(default=True, description="Se deve buscar nas fontes do HemeraLM (BNCC, apostilas)")

class QuestaoItem(BaseModel):
    enunciado: str
    alternativas: Optional[List[str]] = None  # A, B, C, D (apenas se multipla_escolha)
    resposta_correta: str  # Gabarito ou resposta esperada
    explicacao: str  # Por que esta é a resposta?
    fontes_ancoradas: List[SourceReference] = Field(default=[], description="Fontes rastreadas da BNCC/apostilas usadas para a questão")

class ProvaGeradaOutput(BaseModel):
    titulo_sugerido: str
    questoes: List[QuestaoItem]
    documentos_consultados: List[str] = Field(default=[], description="Lista de documentos consultados na busca semântica")

# --- PLANOS DE AULA ---

class LessonPlanRAGRequest(BaseModel):
    tema: str
    disciplina: str
    nivel: str
    duracao: str
    metodologia: str
    usar_rag: bool = Field(default=True, description="Se deve associar habilidades BNCC e apostila via RAG")

class LessonPlanRAGOutput(BaseModel):
    tema: str
    disciplina: str
    nivel: str
    duracao: str
    metodologia: str
    conteudo_plano_html: str = Field(description="Plano de aula detalhado formatado em HTML")
    habilidades_bncc_associadas: List[str] = Field(description="Habilidades da BNCC extraídas das fontes")
    fontes_ancoradas: List[SourceReference] = Field(description="Fontes rastreadas da BNCC/apostilas usadas no roteiro")

# --- ATIVIDADES ---

class ActivityRAGRequest(BaseModel):
    tema: str
    nivel: str
    ludico: bool = False
    usar_rag: bool = Field(default=True, description="Se deve buscar contextualização nas fontes")

class ActivityRAGOutput(BaseModel):
    tema: str
    nivel: str
    ludico: bool
    conteudo_atividade_html: str = Field(description="Conteúdo prático da atividade formatado em HTML")
    instrucoes_professor: str = Field(description="Orientações didáticas baseadas na BNCC")
    fontes_ancoradas: List[SourceReference] = Field(description="Fontes rastreadas da BNCC/apostilas usadas")