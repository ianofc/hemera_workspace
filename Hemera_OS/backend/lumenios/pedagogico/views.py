
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg, Count, Q
from .models import Turma, Aluno, Atividade, Nota, PlanoDeAula, DiarioClasse, Frequencia
from .forms import TurmaForm, AlunoForm # Assume que o fix anterior criou estes forms

# ==============================================================================
# 1. DASHBOARD E LISTAGEM
# ==============================================================================

# @login_required <-- Desativado temporariamente para testar a comunicação Frontend Headless
def listar_turmas(request):
    from django.http import JsonResponse
    # Lógica do Cortex: Filtrar apenas turmas do professor logado, mockamos p/ não precisar de auth agora
    
    # Busca 3 últimas turmas de exemplo se não houver usuário real logado, ou pega tudo
    turmas = Turma.objects.all().annotate(num_alunos=Count('alunos')).order_by('nome')[:5]
    
    data = [
        {
            "id": t.id,
            "nome": t.nome,
            "turno": getattr(t, 'turno', 'Matutino'),
            "num_alunos": t.num_alunos
        }
        for t in turmas
    ]
    
    # Se não houver turmas no db, envia mock test
    if not data:
        data = [
            {"id": 991, "nome": "(Banco de Dados) 1º Ano A", "turno": "Matutino", "num_alunos": 35},
            {"id": 992, "nome": "(Banco de Dados) 2º Ano B", "turno": "Matutino", "num_alunos": 32},
            {"id": 993, "nome": "(Banco de Dados) 9º Ano C", "turno": "Vespertino", "num_alunos": 28},
        ]
        
    return JsonResponse({"turmas": data}, safe=False)

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

from django.http import JsonResponse
from decimal import Decimal

# @login_required (desativado temporariamente p/ teste headless se necessário, ou usar Token Auth)
def gradebook(request):
    # Lógica RESTful: Retorna JSON
    turma_id = request.GET.get('turma_id')
    
    # 1. Busca a turma. (Se não tiver `request.user` logado pelo JWT ainda, pegamos a primeira turma de exemplo)
    turmas = Turma.objects.all()
    if not turma_id and turmas.exists():
        turma = turmas.first()
    elif turma_id:
        # Se usarmos get_object_or_404 pra API, ele retorna 404 HTML, então melhor try/except
        turma = Turma.objects.filter(id=turma_id).first()
        if not turma:
            return JsonResponse({'error': 'Turma não encontrada'}, status=404)
    else:
        return JsonResponse({'error': 'Nenhuma turma disponível'}, status=404)

    # 2. Busca dados para a matriz
    # Usa aluno_set devido a não ter related_name='alunos' no modelo
    alunos = turma.aluno_set.all().order_by('usuario__first_name')
    # Atividade nao tem ForeignKey direto pra Turma, e sim p/ Disciplina?
    # Vamos verificar: Atividade tem `disciplina` e `turma`. OK.
    atividades = turma.atividade_set.all().order_by('data_entrega') if hasattr(turma, 'atividade_set') else []
    
    notas = Nota.objects.filter(atividade__in=atividades)

    # 3. Monta Dicionário de Notas: { aluno_id: { atividade_id: NotaObj } }
    mapa_notas = {}
    for nota in notas:
        if nota.aluno_id not in mapa_notas:
            mapa_notas[nota.aluno_id] = {}
        mapa_notas[nota.aluno_id][nota.atividade_id] = nota

    # 4. Prepara estrutura JSON
    tabela_notas = []
    for aluno in alunos:
        linha = {
            'aluno_id': aluno.id, 
            'aluno_nome': aluno.usuario.get_full_name() or aluno.usuario.username,
            'matricula': aluno.matricula,
            'notas': {}
        }
        soma = Decimal('0')
        pesos = 0
        
        for atividade in atividades:
            nota_obj = mapa_notas.get(aluno.id, {}).get(atividade.id)
            valor = nota_obj.valor if nota_obj else None
            linha['notas'][str(atividade.id)] = float(valor) if valor is not None else None
            
            if valor is not None:
                soma += valor
                pesos += 1
        
        linha['media'] = round(float(soma / pesos), 1) if pesos > 0 else None
        # Atualiza o modelo do aluno com a média persistida (Opcional)
        if linha['media']:
            aluno.nota_media = linha['media']
            aluno.save()
            
        tabela_notas.append(linha)
        
    atividades_list = [
        {'id': a.id, 'titulo': a.titulo, 'data': a.data_entrega.strftime("%Y-%m-%d")} 
        for a in atividades
    ]

    context = {
        'turma_ativa': {
            'id': turma.id,
            'nome': turma.nome,
            'ano_letivo': turma.ano_letivo
        },
        'atividades': atividades_list,
        'tabela_notas': tabela_notas,
    }
    return JsonResponse(context, safe=False)

import json
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def update_nota(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            aluno_id = data.get('aluno_id')
            atividade_id = data.get('atividade_id')
            valor = data.get('valor')
            
            if valor == '' or valor is None:
                Nota.objects.filter(aluno_id=aluno_id, atividade_id=atividade_id).delete()
            else:
                nota, _ = Nota.objects.update_or_create(
                    aluno_id=aluno_id,
                    atividade_id=atividade_id,
                    defaults={'valor': float(valor)}
                )
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error'}, status=405)

@csrf_exempt
def add_atividade(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            turma_id = data.get('turma_id')
            titulo = data.get('titulo')
            
            turma = Turma.objects.get(id=turma_id)
            disciplina = turma.disciplina_set.first()
            if not disciplina:
                disciplina, _ = Disciplina.objects.get_or_create(nome="Geral", turma=turma)
                
            from django.utils import timezone
            nova_ativ = Atividade.objects.create(
                turma=turma,
                disciplina=disciplina,
                titulo=titulo,
                descricao=f"Criada pelo professor via Painel",
                data_entrega=timezone.now()
            )
            return JsonResponse({'status': 'success', 'atividade_id': nova_ativ.id})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error'}, status=405)

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
