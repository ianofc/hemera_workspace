from django.urls import path
from .views import auth, aluno, professor, pedagogical, social, ia

app_name = 'core'

urlpatterns = [
    # --- Auth ---
    path('login/', auth.login_view, name='login'),
    path('logout/', auth.logout_view, name='logout'),
    path('register/', auth.register_view, name='register'),
    
    # --- Roteador Principal ---
    path('dashboard/', auth.dashboard_router_view, name='dashboard'), 
    
    # --- Dashboard Específico do Aluno (A rota que faltava) ---
    path('aluno/dashboard/', aluno.aluno_dashboard, name='aluno_dashboard'),

    # --- Ferramentas do Aluno ---
    path('carteirinha/', aluno.carteirinha_digital, name='carteirinha_digital'),
    path('boletim/', aluno.boletim_view, name='boletim'),
    path('grade/', aluno.grade_horaria, name='grade_horaria'),
    
    # --- IA & Talkio ---
    path('talkio/', ia.talkio_view, name='talkio_app'),

    # --- Extras do Aluno ---
    path('biblioteca/', aluno.biblioteca_view, name='student_library'),
    path('carreira/', aluno.carreira_view, name='student_career'),
    path('loja/', aluno.loja_view, name='student_store'),
    path('tcc/', aluno.tcc_view, name='student_tcc'),
    path('diario/', aluno.diario_view, name='student_diary'),
]
