from django.db import models
from django.utils import timezone

class CategoriaFinanceira(models.Model):
    nome = models.CharField(max_length=100, null=True, blank=True)
    tipo = models.CharField(max_length=10, choices=[('RECEITA', 'Receita'), ('DESPESA', 'Despesa')], null=True, blank=True)
    def __str__(self): return self.nome or "Categoria"

class CentroCusto(models.Model):
    nome = models.CharField(max_length=100, null=True, blank=True)
    codigo = models.CharField(max_length=20, null=True, blank=True)
    def __str__(self): return self.nome or "Centro"

class Fornecedor(models.Model):
    nome = models.CharField(max_length=200, null=True, blank=True)
    cnpj_cpf = models.CharField(max_length=20, null=True, blank=True)
    ativo = models.BooleanField(default=True)
    def __str__(self): return self.nome or "Fornecedor"

class PlanoSaaS(models.Model):
    nome = models.CharField(max_length=100, null=True, blank=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    ativo = models.BooleanField(default=True)
    def __str__(self): return self.nome or "Plano"

class AssinaturaEscola(models.Model):
    escola_nome = models.CharField(max_length=200, null=True, blank=True)
    plano = models.ForeignKey(PlanoSaaS, on_delete=models.SET_NULL, null=True, blank=True)
    ativa = models.BooleanField(default=True)
    def __str__(self): return self.escola_nome or "Assinatura"

class ContratoAluno(models.Model):
    aluno_nome = models.CharField(max_length=200, null=True, blank=True)
    ativo = models.BooleanField(default=True)
    def __str__(self): return self.aluno_nome or "Contrato"

class BoletoAluno(models.Model):
    contrato = models.ForeignKey(ContratoAluno, on_delete=models.SET_NULL, null=True, blank=True)
    aluno_nome = models.CharField(max_length=200, null=True, blank=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    status = models.CharField(max_length=20, default='PENDENTE', null=True, blank=True)
    def __str__(self): return self.aluno_nome or "Boleto"

class Transacao(models.Model):
    descricao = models.CharField(max_length=200, null=True, blank=True)
    valor = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, null=True, blank=True)
    tipo = models.CharField(max_length=10, null=True, blank=True)
    def __str__(self): return self.descricao or "Transação"

class ContasPagar(models.Model):
    descricao = models.CharField(max_length=200, null=True, blank=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    def __str__(self): return self.descricao or "Conta Pagar"

class ContasReceber(models.Model):
    descricao = models.CharField(max_length=200, null=True, blank=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    def __str__(self): return self.descricao or "Conta Receber"
