from django.urls import path
from .views import dashboard

app_name = 'vionex_crm'

urlpatterns = [
    path('dashboard/', dashboard.index, name='dashboard'),
    # Rotas adicionais seriam migradas para cá apontando para .views.cadastros, etc.
]
