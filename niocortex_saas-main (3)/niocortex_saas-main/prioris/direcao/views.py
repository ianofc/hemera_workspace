from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Sum

# Importação dos Modelos Locais
from .models import MetaInstitucional, ReuniaoEstrategica, AnoLetivo

# Importação de Modelos de Outros Módulos (para KPIs)
# Usamos try/except para evitar crash se o módulo ainda não estiver migrado
try:
    from lumenios.pedagogico.models import Aluno
    from ledger.financeiro.models import BoletoAluno
except ImportError:
    Aluno = None
    BoletoAluno = None

# ==============================================================================
# DASHBOARD PRINCIPAL
# ==============================================================================
@login_required
def dashboard_direcao(request):
    "Cockpit da Direção: Visão 360º da Escola."
    
    # 1. KPIs Financeiros (Resumo)
    faturamento_previsto = 0
    faturamento_realizado = 0
    inadimplencia_count = 0
    
    if BoletoAluno:
        faturamento_previsto = BoletoAluno.objects.filter(status='PENDENTE').aggregate(Sum('valor'))['valor__sum'] or 0
        faturamento_realizado = BoletoAluno.objects.filter(status='PAGO').aggregate(Sum('valor'))['valor__sum'] or 0
        inadimplencia_count = BoletoAluno.objects.filter(status='VENCIDO').count()

    # 2. KPIs Pedagógicos/Comerciais
    total_alunos = 0
    ocupacao = 0
    
    if Aluno:
        total_alunos = Aluno.objects.count()
        capacidade_escola = 1500 
        ocupacao = int((total_alunos / capacidade_escola) * 100) if capacidade_escola > 0 else 0

    # 3. Listagens Rápidas
    metas = MetaInstitucional.objects.all().order_by('prazo')[:5]
    reunioes = ReuniaoEstrategica.objects.all().order_by('-data')[:5]

    context = {
        'kpi_financeiro': {
            'previsto': faturamento_previsto,
            'realizado': faturamento_realizado,
            'inadimplencia_qtd': inadimplencia_count
        },
        'kpi_escola': {
            'total_alunos': total_alunos,
            'ocupacao': ocupacao
        },
        'metas': metas,
        'reunioes': reunioes
    }
    
    return render(request, 'direcao/dashboard/dashboard.html', context)

# ==============================================================================
# 1. CRUD: ANO LETIVO
# ==============================================================================

class AnoLetivoListView(LoginRequiredMixin, ListView):
    model = AnoLetivo
    template_name = 'direcao/anoletivo/listar.html'
    context_object_name = 'anos_letivos'
    ordering = ['-ano']

class AnoLetivoCreateView(LoginRequiredMixin, CreateView):
    model = AnoLetivo
    fields = ['ano', 'tema_anual', 'inicio', 'fim', 'ativo']
    template_name = 'direcao/anoletivo/form.html'
    success_url = reverse_lazy('prioris_direcao:anoletivo_list')

class AnoLetivoUpdateView(LoginRequiredMixin, UpdateView):
    model = AnoLetivo
    fields = ['ano', 'tema_anual', 'inicio', 'fim', 'ativo']
    template_name = 'direcao/anoletivo/form.html'
    success_url = reverse_lazy('prioris_direcao:anoletivo_list')

class AnoLetivoDeleteView(LoginRequiredMixin, DeleteView):
    model = AnoLetivo
    template_name = 'direcao/anoletivo/confirmar_exclusao.html'
    success_url = reverse_lazy('prioris_direcao:anoletivo_list')


# ==============================================================================
# 2. CRUD: METAS INSTITUCIONAIS
# ==============================================================================

class MetaInstitucionalListView(LoginRequiredMixin, ListView):
    model = MetaInstitucional
    template_name = 'direcao/metas/listar.html'
    context_object_name = 'metas'

class MetaInstitucionalCreateView(LoginRequiredMixin, CreateView):
    model = MetaInstitucional
    fields = ['titulo', 'descricao', 'prazo', 'status', 'kpi_alvo']
    template_name = 'direcao/metas/form.html'
    success_url = reverse_lazy('prioris_direcao:metainstitucional_list')

class MetaInstitucionalUpdateView(LoginRequiredMixin, UpdateView):
    model = MetaInstitucional
    fields = ['titulo', 'descricao', 'prazo', 'status', 'kpi_alvo']
    template_name = 'direcao/metas/form.html'
    success_url = reverse_lazy('prioris_direcao:metainstitucional_list')

class MetaInstitucionalDeleteView(LoginRequiredMixin, DeleteView):
    model = MetaInstitucional
    template_name = 'direcao/metas/confirmar_exclusao.html'
    success_url = reverse_lazy('prioris_direcao:metainstitucional_list')


# ==============================================================================
# 3. CRUD: REUNIÕES ESTRATÉGICAS
# ==============================================================================

class ReuniaoEstrategicaListView(LoginRequiredMixin, ListView):
    model = ReuniaoEstrategica
    template_name = 'direcao/reunioes/listar.html'
    context_object_name = 'reunioes'
    ordering = ['-data']

class ReuniaoEstrategicaCreateView(LoginRequiredMixin, CreateView):
    model = ReuniaoEstrategica
    fields = ['titulo', 'pauta', 'data', 'participantes', 'decisoes_tomadas']
    template_name = 'direcao/reunioes/form.html'
    success_url = reverse_lazy('prioris_direcao:reuniaoestrategica_list')

class ReuniaoEstrategicaUpdateView(LoginRequiredMixin, UpdateView):
    model = ReuniaoEstrategica
    fields = ['titulo', 'pauta', 'data', 'participantes', 'decisoes_tomadas']
    template_name = 'direcao/reunioes/form.html'
    success_url = reverse_lazy('prioris_direcao:reuniaoestrategica_list')

class ReuniaoEstrategicaDeleteView(LoginRequiredMixin, DeleteView):
    model = ReuniaoEstrategica
    template_name = 'direcao/reunioes/confirmar_exclusao.html'
    success_url = reverse_lazy('prioris_direcao:reuniaoestrategica_list')
