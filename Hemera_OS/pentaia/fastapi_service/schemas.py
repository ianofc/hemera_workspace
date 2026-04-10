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

# --- GERADOR DE PROVAS ---

class GerarProvaInput(BaseModel):
    tema: str
    nivel_ensino: str = Field(description="Ex: 9º Ano, Ensino Médio")
    quantidade_questoes: int = 5
    tipo_questoes: str = Field(default="multipla_escolha", description="'multipla_escolha' ou 'discursiva'")
    dificuldade: str = "medio"

class QuestaoItem(BaseModel):
    enunciado: str
    alternativas: Optional[List[str]] = None  # A, B, C, D (apenas se multipla_escolha)
    resposta_correta: str  # Gabarito ou resposta esperada
    explicacao: str  # Por que esta é a resposta?

class ProvaGeradaOutput(BaseModel):
    titulo_sugerido: str
    questoes: List[QuestaoItem]