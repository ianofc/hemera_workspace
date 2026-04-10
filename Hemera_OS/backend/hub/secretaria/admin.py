from django.contrib import admin
from .models import (
    Matricula, DocumentoAluno, HistoricoEscolar, SolicitacaoSecretaria
)

admin.site.register(Matricula)
admin.site.register(DocumentoAluno)
admin.site.register(HistoricoEscolar)
admin.site.register(SolicitacaoSecretaria)
