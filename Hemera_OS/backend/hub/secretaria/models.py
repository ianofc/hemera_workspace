from django.db import models
class Matricula(models.Model):
    codigo = models.CharField(max_length=20, null=True, blank=True)
    aluno_nome = models.CharField(max_length=200, null=True, blank=True)
    status = models.CharField(max_length=20, default='ATIVA', null=True, blank=True)
    def __str__(self): return self.aluno_nome or "Matrícula"

class DocumentoAluno(models.Model):
    matricula = models.ForeignKey(Matricula, on_delete=models.CASCADE, null=True, blank=True)
    tipo = models.CharField(max_length=50, null=True, blank=True)

class HistoricoEscolar(models.Model):
    matricula = models.ForeignKey(Matricula, on_delete=models.CASCADE, null=True, blank=True)
    media_final = models.DecimalField(max_digits=4, decimal_places=2, default=0.00, null=True, blank=True)

class SolicitacaoSecretaria(models.Model):
    matricula = models.ForeignKey(Matricula, on_delete=models.CASCADE, null=True, blank=True)
    tipo = models.CharField(max_length=100, null=True, blank=True)
