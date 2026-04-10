from django.contrib import admin
from .models import (
    Departamento, Cargo, Funcionario, FolhaPagamento, 
    PontoEletronico, Beneficio, AvaliacaoDesempenho
)

# Registro EXPLÍCITO (Isso não falha)
admin.site.register(Departamento)
admin.site.register(Cargo)
admin.site.register(Funcionario)
admin.site.register(FolhaPagamento)
admin.site.register(PontoEletronico)
admin.site.register(Beneficio)
admin.site.register(AvaliacaoDesempenho)
