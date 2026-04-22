
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime, time, timedelta
import requests # Para API de feriados se necessario, ou mock local
from lumenios.pedagogico.models import Turma, Aluno, Horario

@login_required
def professor_dashboard(request):
    user = request.user
    
    # --- 1. Lógica de Lembretes (Simulada via Sessão para evitar Migração agora) ---
    if request.method == 'POST':
        if 'novo_lembrete' in request.POST:
            texto = request.POST.get('texto_lembrete')
            if texto:
                lembretes = request.session.get('lembretes_prof', [])
                lembretes.append({'id': len(lembretes)+1, 'texto': texto, 'feito': False})
                request.session['lembretes_prof'] = lembretes
                request.session.modified = True
        elif 'delete_lembrete' in request.POST:
            l_id = int(request.POST.get('delete_lembrete'))
            lembretes = request.session.get('lembretes_prof', [])
            lembretes = [l for l in lembretes if l['id'] != l_id]
            request.session['lembretes_prof'] = lembretes
            request.session.modified = True
        return redirect('professor_dashboard')

    lembretes = request.session.get('lembretes_prof', [])

    # --- 2. Dados Acadêmicos ---
    if user.is_superuser:
        turmas = Turma.objects.all()
        horarios = Horario.objects.all()
    else:
        turmas = Turma.objects.filter(professor_regente=user)
        horarios = Horario.objects.filter(turma__professor_regente=user)

    # --- 3. Grade Horária (Estrutura para o Visual Legado) ---
    dias_semana = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta']
    # Define slots fixos para a tabela visual
    tempos_aula = [
        '07:00 - 07:50', '07:50 - 08:40', '08:40 - 09:30', '09:50 - 10:40', '10:40 - 11:30',
        '13:00 - 13:50', '13:50 - 14:40', '14:40 - 15:30', '15:50 - 16:40', '16:40 - 17:30'
    ]
    
    grade = {tempo: {dia: None for dia in dias_semana} for tempo in tempos_aula}
    dia_map = {0: 'Segunda', 1: 'Terça', 2: 'Quarta', 3: 'Quinta', 4: 'Sexta'}
    
    for h in horarios:
        dia_str = dia_map.get(h.dia_semana)
        if not dia_str: continue
        
        hora_inicio_str = h.hora_inicio.strftime('%H:%M')
        
        for slot in grade.keys():
            if slot.startswith(hora_inicio_str):
                is_ac = "AC" in (h.disciplina or "") or (h.turma and h.disciplina != h.turma.nome)
                grade[slot][dia_str] = {
                    'id': h.turma.id if h.turma else 0,
                    'nome': h.disciplina or h.turma.nome,
                    'turma_nome': h.turma.nome if h.turma else '',
                    'alunos_count': h.turma.alunos.count() if h.turma else 0,
                    'is_ac': is_ac
                }
                break

    # --- 4. Stats ---
    stats = {
        'total_turmas': turmas.count(),
        'total_alunos': Aluno.objects.filter(turma__in=turmas).count(),
        'aulas_hoje': horarios.filter(dia_semana=timezone.now().weekday()).count()
    }

    return render(request, 'professor/dashboard.html', {
        'user': user,
        'turmas': turmas,
        'grade': grade,
        'dias_semana': dias_semana,
        'tempos_aula': tempos_aula, # Necessário para iterar na ordem certa
        'stats': stats,
        'lembretes': lembretes,
        'hoje': timezone.now()
    })

# Mantendo as funções auxiliares necessárias
@login_required
def salvar_horario(request):
    if request.method == 'POST':
        dia_str = request.POST.get('dia_semana')
        hora_range = request.POST.get('hora_inicio')
        tipo = request.POST.get('tipo')
        id_turma = request.POST.get('id_turma')
        texto_ac = request.POST.get('texto_ac')
        
        mapa_dias = {'Segunda': 0, 'Terça': 1, 'Quarta': 2, 'Quinta': 3, 'Sexta': 4}
        dia_int = mapa_dias.get(dia_str)
        
        try:
            inicio_str = hora_range.split(' - ')[0].strip()
            hora_inicio = datetime.strptime(inicio_str, '%H:%M').time()
            dummy_dt = datetime(2000, 1, 1, hora_inicio.hour, hora_inicio.minute)
            hora_fim = (dummy_dt + timedelta(minutes=50)).time()
        except:
            return redirect('professor_dashboard')

        if dia_int is not None and hora_inicio:
            Horario.objects.filter(dia_semana=dia_int, hora_inicio=hora_inicio, turma__professor_regente=request.user).delete()
            
            novo = None
            if tipo == 'turma' and id_turma:
                turma = get_object_or_404(Turma, id=id_turma)
                novo = Horario(dia_semana=dia_int, hora_inicio=hora_inicio, hora_fim=hora_fim, turma=turma, disciplina=turma.nome)
            elif tipo == 'ac' and texto_ac:
                t_padrao = Turma.objects.filter(professor_regente=request.user).first()
                if t_padrao:
                    novo = Horario(dia_semana=dia_int, hora_inicio=hora_inicio, hora_fim=hora_fim, turma=t_padrao, disciplina=f'AC - {texto_ac}')
            
            if novo: novo.save()

    return redirect('professor_dashboard')

@login_required
def corporate_dashboard(request): return redirect('professor_dashboard')

@login_required
def teacher_schedule(request): return redirect('professor_dashboard')
