from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

# Tenta importar os modelos necessários
try:
    from lumenios.plataforma.models import Matricula
except ImportError:
    Matricula = None

# --- DASHBOARD & PERFIL ---

@login_required
def aluno_dashboard(request):
    # Aponta para o template do dashboard do aluno
    return render(request, 'aluno/dashboard.html') 

@login_required
def student_profile(request):
    return render(request, 'social/profile/profile_detail.html', {'profile_user': request.user})

# --- ACADÊMICO ---

@login_required
def student_subjects(request):
    matriculas = []
    
    # 1. Tenta buscar matrículas reais
    if Matricula:
        try:
            matriculas = Matricula.objects.filter(aluno=request.user)
        except:
            pass
            
    # 2. Simula baseado na Turma se não houver matrícula
    if not matriculas and hasattr(request.user, 'perfil_escolar'):
        aluno_perfil = request.user.perfil_escolar
        if aluno_perfil and aluno_perfil.turma:
            for disciplina in aluno_perfil.turma.disciplinas.all():
                matriculas.append({
                    'curso': {'titulo': disciplina.nome, 'professor': disciplina.professor},
                    'progresso': 0
                })

    context = {'matriculas': matriculas}
    return render(request, 'extras/disciplina.html', context)

@login_required
def student_grades(request): return render(request, 'aluno/academico/boletim.html')
@login_required
def boletim_view(request): return render(request, 'aluno/academico/boletim.html')

@login_required
def student_calendar(request): return render(request, 'aluno/calendar.html')

@login_required
def student_timetable(request): return render(request, 'aluno/academico/grade_horaria.html')
@login_required
def grade_horaria(request): return render(request, 'aluno/academico/grade_horaria.html')

@login_required
def student_files(request): return render(request, 'aluno/academico/arquivos.html')

@login_required
def student_lesson(request): return render(request, 'extras/sala_de_aula.html') 

@login_required
def student_activity(request): return render(request, 'aluno/academico/atividade.html')

# --- ADMINISTRATIVO ---

@login_required
def student_financial(request): return render(request, 'aluno/administrativo/financeiro.html')

@login_required
def student_services(request): return render(request, 'aluno/administrativo/secretaria.html')

@login_required
def carteirinha_digital(request): return render(request, 'core/ferramentas/carteirinha.html')
@login_required
def student_id_card(request): return render(request, 'core/ferramentas/carteirinha.html')

# --- EXTRAS & PREMIUM ---

@login_required
def daily_diary(request): return render(request, 'aluno/extras/diario_infantil.html')
@login_required
def diario_view(request): return render(request, 'aluno/extras/diario_infantil.html')

@login_required
def gamification_store(request): return render(request, 'aluno/extras/loja.html')
@login_required
def loja_view(request): return render(request, 'aluno/extras/loja.html')

@login_required
def student_library(request): return render(request, 'aluno/extras/biblioteca.html')
@login_required
def biblioteca_view(request): return render(request, 'aluno/extras/biblioteca.html')

@login_required
def career_center(request): return render(request, 'aluno/extras/carreira.html')
@login_required
def carreira_view(request): return render(request, 'aluno/extras/carreira.html')

@login_required
def thesis_manager(request): return render(request, 'aluno/extras/tcc.html')
@login_required
def tcc_view(request): return render(request, 'aluno/extras/tcc.html')

@login_required
def student_premium_stats(request): return render(request, 'aluno/premium/stats.html')
