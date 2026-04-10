from django.urls import path
from . import views

app_name = 'prioris'

urlpatterns = [
    # Rotas para AnoLetivo
    path('anoletivo/', views.AnoLetivoListView.as_view(), name='anoletivo_list'),
    path('anoletivo/novo/', views.AnoLetivoCreateView.as_view(), name='anoletivo_create'),
    path('anoletivo/<uuid:pk>/editar/', views.AnoLetivoUpdateView.as_view(), name='anoletivo_update'),
    path('anoletivo/<uuid:pk>/excluir/', views.AnoLetivoDeleteView.as_view(), name='anoletivo_delete'),

    # Rotas para MetaInstitucional
    path('metainstitucional/', views.MetaInstitucionalListView.as_view(), name='metainstitucional_list'),
    path('metainstitucional/novo/', views.MetaInstitucionalCreateView.as_view(), name='metainstitucional_create'),
    path('metainstitucional/<uuid:pk>/editar/', views.MetaInstitucionalUpdateView.as_view(), name='metainstitucional_update'),
    path('metainstitucional/<uuid:pk>/excluir/', views.MetaInstitucionalDeleteView.as_view(), name='metainstitucional_delete'),

    # Rotas para ReuniaoEstrategica
    path('reuniaoestrategica/', views.ReuniaoEstrategicaListView.as_view(), name='reuniaoestrategica_list'),
    path('reuniaoestrategica/novo/', views.ReuniaoEstrategicaCreateView.as_view(), name='reuniaoestrategica_create'),
    path('reuniaoestrategica/<uuid:pk>/editar/', views.ReuniaoEstrategicaUpdateView.as_view(), name='reuniaoestrategica_update'),
    path('reuniaoestrategica/<uuid:pk>/excluir/', views.ReuniaoEstrategicaDeleteView.as_view(), name='reuniaoestrategica_delete'),

]
