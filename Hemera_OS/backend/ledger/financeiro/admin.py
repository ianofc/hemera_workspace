from django.contrib import admin
from .models import (
    CategoriaFinanceira, CentroCusto, Fornecedor, PlanoSaaS, 
    AssinaturaEscola, ContratoAluno, BoletoAluno, Transacao, 
    ContasPagar, ContasReceber
)

admin.site.register(CategoriaFinanceira)
admin.site.register(CentroCusto)
admin.site.register(Fornecedor)
admin.site.register(PlanoSaaS)
admin.site.register(AssinaturaEscola)
admin.site.register(ContratoAluno)
admin.site.register(BoletoAluno)
admin.site.register(Transacao)
admin.site.register(ContasPagar)
admin.site.register(ContasReceber)
