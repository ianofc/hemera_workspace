from django.db import models
class GradeHoraria(models.Model):
    turma = models.CharField(max_length=50, null=True, blank=True)
    dia_semana = models.CharField(max_length=20, null=True, blank=True)
    def __str__(self): return self.turma or "Grade"
class PlanejamentoPedagogico(models.Model):
    titulo = models.CharField(max_length=200, null=True, blank=True)
class OcorrenciaDisciplinar(models.Model):
    aluno_nome = models.CharField(max_length=200, null=True, blank=True)
class ReuniaoPais(models.Model):
    turma = models.CharField(max_length=50, null=True, blank=True)
