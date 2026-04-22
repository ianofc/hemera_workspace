
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg, Count, Q
from .models import Turma, Aluno, Atividade, Nota, PlanoDeAula, DiarioClasse, Frequencia
from .forms import TurmaForm, AlunoForm # Assume que o fix anterior criou estes forms

# ==============================================================================
# 1. DASHBOARD E LISTAGEM
# ==============================================================================

@login_required
def listar_turmas(request):
    # Lógica do Cortex: Filtrar apenas turmas do professor logado
    # Se for admin, vê todas (modo Deus)
    if request.user.is_superuser:
        turmas = Turma.objects.all().annotate(num_alunos=Count('alunos')).order_by('nome')
    else:
        turmas = Turma.objects.filter(professor_regente=request.user).annotate(num_alunos=Count('alunos')).order_by('nome')
    
    return render(request, 'pedagogico/turmas/listar_turmas.html', {'turmas': turmas})

@login_required
def detalhar_turma(request, turma_id):
    turma = get_object_or_404(Turma, id=turma_id)
    
    # Busca dados relacionados para o Dashboard da Turma
    alunos = turma.alunos.all().order_by('nome')
    atividades_recentes = turma.atividades.order_by('-data_aplicacao')[:5]
    planos_proximos = turma.planos_aula.filter(status='Planejado').order_by('data_prevista')[:5]
    
    context = {
        'turma': turma,
        'alunos': alunos,
        'atividades': atividades_recentes,
        'planos': planos_proximos,
        'total_alunos': alunos.count()
    }
    return render(request, 'pedagogico/turmas/detalhar_turmas.html', context)

# ==============================================================================
# 2. GESTÃO CRUD (Turmas e Alunos)
# ==============================================================================

@login_required
def editar_turma(request, turma_id):
    turma = get_object_or_404(Turma, id=turma_id)
    if request.method == 'POST':
        form = TurmaForm(request.POST, instance=turma)
        if form.is_valid():
            form.save()
            messages.success(request, 'Turma atualizada com sucesso!')
            return redirect('pedagogico:detalhar_turma', turma_id=turma.id)
    else:
        form = TurmaForm(instance=turma)
    return render(request, 'pedagogico/turmas/editar.html', {'form': form, 'turma': turma})

@login_required
def excluir_turma(request, turma_id):
    turma = get_object_or_404(Turma, id=turma_id)
    if request.method == 'POST':
        turma.delete()
        messages.success(request, 'Turma removida.')
        return redirect('pedagogico:listar_turmas')
    return render(request, 'pedagogico/turmas/exclusao_turmas.html', {'obj': turma, 'tipo': 'Turma'})

@login_required
def form_turmas(request):
    if request.method == 'POST':
        form = TurmaForm(request.POST)
        if form.is_valid():
            nova_turma = form.save(commit=False)
            nova_turma.professor_regente = request.user
            nova_turma.save()
            messages.success(request, 'Nova turma criada!')
            return redirect('pedagogico:listar_turmas')
    else:
        form = TurmaForm()
    return render(request, 'pedagogico/turmas/form_turmas.html', {'form': form})

# --- ALUNOS ---

@login_required
def adicionar_aluno(request, turma_id):
    turma = get_object_or_404(Turma, id=turma_id)
    if request.method == 'POST':
        form = AlunoForm(request.POST)
        if form.is_valid():
            aluno = form.save(commit=False)
            aluno.turma = turma
            aluno.tenant_id = turma.tenant_id
            aluno.save()
            messages.success(request, 'Aluno matriculado com sucesso!')
            return redirect('pedagogico:detalhar_turma', turma_id=turma.id)
    else:
        form = AlunoForm()
    return render(request, 'pedagogico/alunos/form_alunos.html', {'form': form, 'turma': turma})

@login_required
def editar_aluno(request, aluno_id):
    aluno = get_object_or_404(Aluno, id=aluno_id)
    if request.method == 'POST':
        form = AlunoForm(request.POST, instance=aluno)
        if form.is_valid():
            form.save()
            return redirect('pedagogico:detalhar_turma', turma_id=aluno.turma.id)
    else:
        form = AlunoForm(instance=aluno)
    return render(request, 'pedagogico/alunos/editar_aluno.html', {'form': form, 'aluno': aluno})

@login_required
def excluir_aluno(request, aluno_id):
    aluno = get_object_or_404(Aluno, id=aluno_id)
    turma_id = aluno.turma.id
    if request.method == 'POST':
        aluno.delete()
        return redirect('pedagogico:detalhar_turma', turma_id=turma_id)
    return render(request, 'pedagogico/alunos/exclusao_alunos.html', {'obj': aluno, 'tipo': 'Aluno'})

@login_required
def listar_alunos(request):
    alunos = Aluno.objects.filter(turma__professor_regente=request.user).order_by('nome')
    return render(request, 'pedagogico/alunos/listar_alunos.html', {'alunos': alunos})

@login_required
def form_alunos(request):
    # Rota genérica para criar aluno sem turma pré-definida (opcional)
    return render(request, 'pedagogico/alunos/form_alunos.html')

# ==============================================================================
# 3. GRADEBOOK (O Coração do Sistema)
# ==============================================================================

@login_required
def gradebook(request):
    # Lógica complexa trazida do 'grade_service.py' do legado
    turma_id = request.GET.get('turma_id')
    
    # 1. Se não selecionou turma, mostra seletor ou a primeira disponível
    turmas = Turma.objects.filter(professor_regente=request.user)
    if not turma_id and turmas.exists():
        turma = turmas.first()
    elif turma_id:
        turma = get_object_or_404(Turma, id=turma_id, professor_regente=request.user)
    else:
        return render(request, 'pedagogico/gradebook/gradebook.html', {'error': 'Nenhuma turma encontrada'})

    # 2. Busca dados para a matriz
    alunos = turma.alunos.all().order_by('nome')
    atividades = turma.atividades.all().order_by('data_aplicacao')
    notas = Nota.objects.filter(atividade__turma=turma)

    # 3. Monta Dicionário de Notas: { aluno_id: { atividade_id: NotaObj } }
    mapa_notas = {}
    for nota in notas:
        if nota.aluno_id not in mapa_notas:
            mapa_notas[nota.aluno_id] = {}
        mapa_notas[nota.aluno_id][nota.atividade.id] = nota

    # 4. Prepara estrutura para o Template iterar
    tabela_notas = []
    for aluno in alunos:
        linha = {'aluno': aluno, 'notas': []}
        soma = 0
        pesos = 0
        
        for atividade in atividades:
            nota_obj = mapa_notas.get(aluno.id, {}).get(atividade.id)
            valor = nota_obj.valor if nota_obj else None
            linha['notas'].append({'atividade_id': atividade.id, 'valor': valor})
            
            # Cálculo simples de média (pode ser aprimorado)
            if valor is not None:
                soma += valor
                pesos += 1
        
        linha['media'] = round(soma / pesos, 1) if pesos > 0 else '-'
        tabela_notas.append(linha)

    context = {
        'turma_ativa': turma,
        'turmas': turmas,
        'atividades': atividades,
        'tabela_notas': tabela_notas,
    }
    return render(request, 'pedagogico/gradebook/gradebook.html', context)

# ==============================================================================
# 4. FERRAMENTAS & OUTROS
# ==============================================================================

@login_required
def gerador_atividades(request):
    return render(request, 'pedagogico/ferramentas/gerador_atividades.html')

@login_required
def gerador_provas(request):
    return render(request, 'pedagogico/ferramentas/gerador_provas.html')

@login_required
def gerador_planejamentos(request):
    return render(request, 'pedagogico/ferramentas/gerador_planejamentos.html')
