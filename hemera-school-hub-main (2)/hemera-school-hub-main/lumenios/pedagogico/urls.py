from django.urls import path
from . import views

app_name = 'pedagogico'

urlpatterns = [
    # Alunos
    path('alunos/', views.listar_alunos, name='listar_alunos'),
    path('alunos/novo/', views.form_alunos, name='novo_aluno'),
    
    # Turmas
    path('turmas/', views.listar_turmas, name='listar_turmas'),
    path('turmas/nova/', views.form_turmas, name='form_turmas'),  # ADICIONADO
        path('turmas/editar/<int:turma_id>/', views.editar_turma, name='editar_turma'),
    path('turmas/<int:turma_id>/', views.detalhar_turma, name='detalhar_turma'),
    
    # Ferramentas
    path('gradebook/', views.gradebook, name='gradebook'),
    path('ferramentas/atividades/', views.gerador_atividades, name='gerador_atividades'),
    path('ferramentas/provas/', views.gerador_provas, name='gerador_provas'),
    path('ferramentas/planejamento/', views.gerador_planejamentos, name='gerador_planejamentos'), # ADICIONADO
    path('turmas/<int:turma_id>/adicionar-aluno/', views.adicionar_aluno, name='adicionar_aluno'),
    path('alunos/<int:aluno_id>/editar/', views.editar_aluno, name='editar_aluno'),
    path('alunos/<int:aluno_id>/excluir/', views.excluir_aluno, name='excluir_aluno'),
    path('turmas/<int:turma_id>/excluir/', views.excluir_turma, name='excluir_turma'),
]
