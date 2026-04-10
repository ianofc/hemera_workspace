from django.db import models
from django.conf import settings
from django.utils import timezone

class Turma(models.Model):
    nome = models.CharField(max_length=100)
    ano_letivo = models.IntegerField(default=2026)
    periodo = models.CharField(max_length=20, default='Matutino')
    # Adicionado related_name para facilitar acesso reverso (user.turmas_regente)
    professor_regente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='turmas_regente')

    def __str__(self): return self.nome

class Disciplina(models.Model):
    nome = models.CharField(max_length=100)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name='disciplinas')
    professor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='disciplinas_lecionadas')
    def __str__(self): return self.nome

class Horario(models.Model):
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name='horarios')
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    dia_semana = models.IntegerField(choices=[(0,'Seg'),(1,'Ter'),(2,'Qua'),(3,'Qui'),(4,'Sex')])
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()
    def __str__(self): return f"{self.turma} - {self.dia_semana}"

class Aluno(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='perfil_escolar')
    turma = models.ForeignKey(Turma, on_delete=models.SET_NULL, null=True, blank=True)
    
    # [CORREÇÃO] Renomeado de matricula_escolar -> matricula (Espelho do Core)
    matricula = models.CharField(max_length=50, unique=True, null=True, blank=True)
    
    nota_media = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    taxa_frequencia = models.DecimalField(max_digits=5, decimal_places=2, default=100.0) 
    
    def __str__(self): return f"Aluno: {self.usuario}"

# --- Demais modelos (Atividade, Nota, Frequencia...) permanecem iguais ---
class Atividade(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    data_entrega = models.DateTimeField()
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    def __str__(self): return self.titulo

class Nota(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    atividade = models.ForeignKey(Atividade, on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=5, decimal_places=2)
    feedback = models.TextField(blank=True)
    def __str__(self): return f"{self.aluno} - {self.valor}"

class Frequencia(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='registros_frequencia')
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    data = models.DateField(default=timezone.now)
    presente = models.BooleanField(default=True)
    def __str__(self): return f"{self.aluno} - {self.data}"

class PlanoDeAula(models.Model):
    titulo = models.CharField(max_length=200)
    conteudo = models.TextField()
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    data = models.DateField()
    def __str__(self): return self.titulo

class DiarioClasse(models.Model):
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    data = models.DateField(auto_now_add=True)
    observacoes = models.TextField()
    def __str__(self): return f"Diário {self.turma} - {self.data}"