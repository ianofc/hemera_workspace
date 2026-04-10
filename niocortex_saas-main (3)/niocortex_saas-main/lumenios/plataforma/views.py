
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime, time, timedelta
from types import SimpleNamespace

# Imports dos Models e Forms
from .models import Curso, Matricula, Conteudo, Modulo
from .forms import CursoForm
from lumenios.pedagogico.models import Turma, Aluno, Horario

# ==============================================================================
# 1. DASHBOARD PROFESSOR (COM GRADE E STATS)
# ==============================================================================

@login_required
def dashboard_professor(request):
    user = request.user
    
    # Busca dados
    if user.is_superuser:
        turmas = Turma.objects.all()
        horarios = Horario.objects.all()
        cursos = Curso.objects.all()
    else:
        turmas = Turma.objects.filter(professor_regente=user)
        horarios = Horario.objects.filter(turma__professor_regente=user)
        cursos = Curso.objects.filter(professor=user)
    
    # Grade Horária
    dias_semana = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta']
    tempos_aula = [
        '07:00 - 07:50', '07:50 - 08:40', '08:40 - 09:30', '09:50 - 10:40', '10:40 - 11:30',
        '13:00 - 13:50', '13:50 - 14:40', '14:40 - 15:30', '15:50 - 16:40', '16:40 - 17:30',
        '19:00 - 19:50', '19:50 - 20:40', '20:50 - 21:40', '21:40 - 22:30'
    ]
    
    grade = {tempo: {dia: None for dia in dias_semana} for tempo in tempos_aula}
    dia_map = {0: 'Segunda', 1: 'Terça', 2: 'Quarta', 3: 'Quinta', 4: 'Sexta', 5: 'Sábado', 6: 'Domingo'}
    
    for h in horarios:
        dia_str = dia_map.get(h.dia_semana)
        if not dia_str: continue
        
        h_inicio_str = h.hora_inicio.strftime('%H:%M')
        
        for slot in grade.keys():
            if slot.startswith(h_inicio_str):
                is_ac = "AC" in (h.disciplina or "") or (h.turma and h.disciplina != h.turma.nome)
                
                grade[slot][dia_str] = {
                    'id': h.turma.id if h.turma else 0,
                    'nome': h.disciplina if h.disciplina else (h.turma.nome if h.turma else 'Aula'),
                    'turma_nome': h.turma.nome if h.turma else '',
                    'alunos_count': h.turma.alunos.count() if h.turma else 0,
                    'is_ac': is_ac
                }
                break

    stats = {
        'total_turmas': turmas.count(),
        'total_alunos': Aluno.objects.filter(turma__in=turmas).count(),
        'aulas_hoje': horarios.filter(dia_semana=timezone.now().weekday()).count(),
        'cursos': cursos.count()
    }

    return render(request, 'professor/dashboard.html', {
        'user': user, 'turmas': turmas, 'grade': grade, 
        'dias_semana': dias_semana, 'stats': stats, 'cursos': cursos
    })

@login_required
def salvar_horario(request):
    if request.method == 'POST':
        dia_str = request.POST.get('dia_semana')
        hora_range = request.POST.get('hora_inicio')
        tipo = request.POST.get('tipo')
        id_turma = request.POST.get('id_turma')
        texto_ac = request.POST.get('texto_ac')
        
        mapa_dias = {'Segunda': 0, 'Terça': 1, 'Quarta': 2, 'Quinta': 3, 'Sexta': 4, 'Sábado': 5}
        dia_int = mapa_dias.get(dia_str)
        
        hora_inicio = None
        hora_fim = None
        try:
            inicio_str = hora_range.split(' - ')[0].strip()
            hora_inicio = datetime.strptime(inicio_str, '%H:%M').time()
            dummy_dt = datetime(2000, 1, 1, hora_inicio.hour, hora_inicio.minute)
            hora_fim = (dummy_dt + timedelta(minutes=50)).time()
        except:
            return redirect('lumenios:dashboard_professor')

        if dia_int is not None and hora_inicio:
            Horario.objects.filter(
                dia_semana=dia_int,
                hora_inicio=hora_inicio,
                turma__professor_regente=request.user
            ).delete()
            
            novo = None
            if tipo == 'turma' and id_turma:
                turma = get_object_or_404(Turma, id=id_turma)
                novo = Horario(
                    dia_semana=dia_int,
                    hora_inicio=hora_inicio,
                    hora_fim=hora_fim,
                    turma=turma,
                    disciplina=turma.nome
                )
            elif tipo == 'ac' and texto_ac:
                t_padrao = Turma.objects.filter(professor_regente=request.user).first()
                if t_padrao:
                    novo = Horario(
                        dia_semana=dia_int,
                        hora_inicio=hora_inicio,
                        hora_fim=hora_fim,
                        turma=t_padrao,
                        disciplina=f"AC - {texto_ac}"
                    )

            if novo:
                novo.save()

    return redirect('lumenios:dashboard_professor')

# ==============================================================================
# 2. GESTÃO DE CURSOS (RESTAURADO)
# ==============================================================================

@login_required
def criar_curso(request):
    if request.method == 'POST':
        form = CursoForm(request.POST, request.FILES)
        if form.is_valid():
            curso = form.save(commit=False)
            curso.professor = request.user
            curso.save()
            return redirect('lumenios:dashboard_professor')
    else:
        form = CursoForm()
    return render(request, 'professor/criar_conteudo.html', {'form': form})

@login_required
def gerenciar_curso(request, curso_id):
    try:
        curso = get_object_or_404(Curso, id=curso_id)
    except:
        return redirect('lumenios:dashboard_professor')
    modulos = curso.modulos.all().prefetch_related('conteudos')
    return render(request, 'professor/gerenciar_curso.html', {'curso': curso, 'modulos': modulos})

@login_required
def editor_conteudo(request, curso_id):
    return render(request, 'professor/editor_conteudo.html', {'curso_id': curso_id})

# ==============================================================================
# 3. ÁREA DO ALUNO (RESTAURADO)
# ==============================================================================

@login_required
def dashboard_aluno(request):
    matriculas = Matricula.objects.filter(aluno=request.user)
    return render(request, 'aluno/dashboard.html', {'matriculas': matriculas})

@login_required
def perfil_aluno(request):
    return render(request, 'aluno/dashboard.html', {'section': 'perfil'})

@login_required
def disciplinas_aluno(request):
    matriculas = Matricula.objects.filter(aluno=request.user)
    return render(request, 'extras/disciplina.html', {'matriculas': matriculas})

@login_required
def sala_de_aula(request, conteudo_id=None):
    if not conteudo_id: return redirect('lumenios:dashboard_aluno')
    conteudo_atual = get_object_or_404(Conteudo, id=conteudo_id)
    modulo = conteudo_atual.modulo
    curso = modulo.curso
    modulos = curso.modulos.all().prefetch_related('conteudos')
    
    if conteudo_atual.tipo == 'VIDEO' and conteudo_atual.link:
        if 'watch?v=' in conteudo_atual.link:
            conteudo_atual.embed_link = conteudo_atual.link.replace('watch?v=', 'embed/')
        elif 'youtu.be/' in conteudo_atual.link:
            conteudo_atual.embed_link = conteudo_atual.link.replace('youtu.be/', 'www.youtube.com/embed/')
        else:
            conteudo_atual.embed_link = conteudo_atual.link
    else:
        conteudo_atual.embed_link = None

    return render(request, 'extras/sala_de_aula.html', {'curso': curso, 'modulos': modulos, 'conteudo_atual': conteudo_atual})

@login_required
def sala_de_aula_demo(request):
    class MockQuerySet(list): 
        def all(self): return self
        def count(self): return len(self)
    prof = SimpleNamespace(first_name="Alan", last_name="Turing", avatar=None)
    curso = SimpleNamespace(id=0, titulo="IA Fundamentos", categoria="Tecnologia", professor=prof, imagem_capa=SimpleNamespace(url="https://images.unsplash.com/photo-1620712943543-bcc4688e7485?auto=format&fit=crop&w=1600&q=80"))
    aula1 = SimpleNamespace(id=1, titulo="1. Redes Neurais", tipo="VIDEO", link="https://www.youtube.com/watch?v=aircAruvnKk", embed_link="https://www.youtube.com/embed/aircAruvnKk", arquivo=None, texto_apoio="Intro.")
    mod1 = SimpleNamespace(titulo="Módulo 1", conteudos=MockQuerySet([aula1]))
    return render(request, 'extras/sala_de_aula.html', {'curso': curso, 'modulos': [mod1], 'conteudo_atual': aula1, 'is_demo': True})

@login_required
def biblioteca_aluno(request): return render(request, 'extras/biblioteca.html')
@login_required
def ensino_complementar(request): return render(request, 'extras/complementar.html')
@login_required
def avaliacoes_aluno(request): return render(request, 'extras/avaliacoes.html')
@login_required
def zios_investigate(request): return render(request, 'extras/zios.html', {'tema': request.GET.get('q', 'Aprendizado')})
@login_required
def desempenho_analytics(request): return render(request, 'aluno/desempenho.html', {'media_geral': 0})
