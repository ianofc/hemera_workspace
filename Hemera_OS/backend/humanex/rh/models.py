from django.db import models

class Departamento(models.Model):
    nome = models.CharField(max_length=100, null=True, blank=True)
    def __str__(self): return self.nome or "Depto"

class Cargo(models.Model):
    nome = models.CharField(max_length=100, null=True, blank=True)
    departamento = models.ForeignKey(Departamento, on_delete=models.SET_NULL, null=True, blank=True)
    salario_base = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    def __str__(self): return self.nome or "Cargo"

class Funcionario(models.Model):
    nome = models.CharField(max_length=200, null=True, blank=True)
    cargo = models.ForeignKey(Cargo, on_delete=models.SET_NULL, null=True, blank=True)
    cpf = models.CharField(max_length=14, null=True, blank=True)
    data_admissao = models.DateField(null=True, blank=True)
    salario = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    ativo = models.BooleanField(default=True)
    def __str__(self): return self.nome or "Funcionario"

class FolhaPagamento(models.Model):
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE, null=True, blank=True)
    mes_referencia = models.DateField(null=True, blank=True)
    valor_liquido = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    status = models.CharField(max_length=20, default='RASCUNHO', null=True, blank=True)

class PontoEletronico(models.Model):
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE, null=True, blank=True)
    data = models.DateField(null=True, blank=True)
    entrada = models.TimeField(null=True, blank=True)
    saida = models.TimeField(null=True, blank=True)

class Beneficio(models.Model):
    nome = models.CharField(max_length=100, null=True, blank=True)
    valor = models.DecimalField(max_digits=8, decimal_places=2, default=0.00, null=True, blank=True)

class AvaliacaoDesempenho(models.Model):
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE, null=True, blank=True)
    nota = models.IntegerField(default=0, null=True, blank=True)
