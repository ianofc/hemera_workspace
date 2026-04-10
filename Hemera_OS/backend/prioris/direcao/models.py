from django.db import models
from django.conf import settings
import uuid

class AnoLetivo(models.Model):
    """ Define o ciclo estratégico da escola """
    ano = models.IntegerField(unique=True)
    tema_anual = models.CharField(max_length=200, blank=True, help_text="Ex: Ano da Inovação Tecnológica")
    inicio = models.DateField()
    fim = models.DateField()
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return str(self.ano)

class MetaInstitucional(models.Model):
    """ KPIs e Objetivos da Direção """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant_id = models.UUIDField(editable=False, db_index=True)
    
    titulo = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    
    categoria = models.CharField(max_length=50, choices=[
        ('FINANCEIRO', 'Financeiro'),
        ('PEDAGOGICO', 'Pedagógico'),
        ('CAPTACAO', 'Captação/Retenção'),
        ('INFRA', 'Infraestrutura')
    ])
    
    meta_valor = models.DecimalField(max_digits=10, decimal_places=2, help_text="Valor alvo (ex: 1000 alunos ou R$ 500k)")
    valor_atual = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    prazo = models.DateField()
    
    STATUS_CHOICES = [
        ('EM_ANDAMENTO', 'Em Andamento'),
        ('ATINGIDA', 'Meta Atingida'),
        ('NAO_ATINGIDA', 'Não Atingida'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='EM_ANDAMENTO')

    def __str__(self):
        return f"{self.titulo} ({self.get_status_display()})"

    @property
    def progresso_percentual(self):
        if self.meta_valor == 0: return 0
        return int((self.valor_atual / self.meta_valor) * 100)

class ReuniaoEstrategica(models.Model):
    """ Atas e Pautas de Reuniões da Direção """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant_id = models.UUIDField(editable=False, db_index=True)
    
    titulo = models.CharField(max_length=200)
    data = models.DateTimeField()
    participantes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='reunioes_direcao')
    pauta = models.TextField()
    decisoes_tomadas = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titulo} - {self.data.strftime('%d/%m/%Y')}"