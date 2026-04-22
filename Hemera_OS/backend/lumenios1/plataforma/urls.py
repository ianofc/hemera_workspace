from django.urls import path
from . import views

app_name = 'lumenios'

urlpatterns = [
    path('professor/horario/salvar/', views.salvar_horario, name='salvar_horario'),
    # --- ÁREA DO PROFESSOR (NOVO) ---
    path('professor/dashboard/', views.dashboard_professor, name='dashboard_professor'),
    path('professor/criar-curso/', views.criar_curso, name='criar_curso'),
    path('professor/curso/<int:curso_id>/', views.gerenciar_curso, name='gerenciar_curso'),
    path('professor/editor/<int:curso_id>/', views.editor_conteudo, name='editor_conteudo'),

    # --- ÁREA DO ALUNO (LEGADO/EXISTENTE) ---
    path('aluno/home/', views.dashboard_aluno, name='dashboard_aluno'),
    path('aluno/perfil/', views.perfil_aluno, name='perfil_aluno'),
    path('aluno/disciplinas/', views.disciplinas_aluno, name='disciplinas'),
    path('aluno/aula/demo/', views.sala_de_aula_demo, name='sala_de_aula_demo'),
    path('aluno/aula/<int:conteudo_id>/', views.sala_de_aula, name='sala_de_aula'),
    
    # Extras
    path('aluno/biblioteca/', views.biblioteca_aluno, name='biblioteca'),
    path('aluno/complementar/', views.ensino_complementar, name='complementar'),
    path('aluno/avaliacoes/', views.avaliacoes_aluno, name='avaliacoes'),
    path('aluno/desempenho/', views.desempenho_analytics, name='desempenho'),
    path('aluno/zios/', views.zios_investigate, name='zios'),
]