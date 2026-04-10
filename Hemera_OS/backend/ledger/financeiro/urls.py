from django.urls import path
from .views import dashboard

app_name = 'ledger_financeiro'

urlpatterns = [
    path('dashboard/', dashboard.index, name='dashboard'),
    # Rotas adicionais seriam migradas para cá apontando para .views.cadastros, etc.
]
