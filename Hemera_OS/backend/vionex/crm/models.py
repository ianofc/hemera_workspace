from django.db import models
class Lead(models.Model):
    nome = models.CharField(max_length=200, null=True, blank=True)
    def __str__(self): return self.nome or "Lead"
class CampanhaMarketing(models.Model):
    nome = models.CharField(max_length=200, null=True, blank=True)
class Atendimento(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, null=True, blank=True)
class FunilVendas(models.Model):
    etapa = models.CharField(max_length=100, null=True, blank=True)
