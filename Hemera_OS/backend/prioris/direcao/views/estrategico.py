from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from ..models import MetaInstitucional, AnoLetivo

class MetaListView(ListView):
    model = MetaInstitucional
    template_name = 'direcao/metas/listar.html'
    context_object_name = 'metas'

class AnoLetivoListView(ListView):
    model = AnoLetivo
    template_name = 'direcao/anoletivo/listar.html'
    context_object_name = 'anos_letivos'

class AnoLetivoCreateView(CreateView):
    """ Resolvendo o erro da linha 9 do urls.py """
    model = AnoLetivo
    fields = '__all__'
    template_name = 'direcao/anoletivo/form.html'
    success_url = reverse_lazy('prioris_direcao:anoletivo_list')

class AnoLetivoUpdateView(UpdateView):
    """ Antecipando erro de edição """
    model = AnoLetivo
    fields = '__all__'
    template_name = 'direcao/anoletivo/form.html'
    success_url = reverse_lazy('prioris_direcao:anoletivo_list')
