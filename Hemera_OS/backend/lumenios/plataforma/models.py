from django.db import models
from django.conf import settings # Importa a referência ao usuário do Core

# REMOVIDO: class Usuario(AbstractUser)... Não podemos ter dois usuários.

class Curso(models.Model):
    CATEGORIAS = (
        ('ESCOLA', 'Ensino Escolar (K-12)'),
        ('TECNICO', 'Profissionalizante/Técnico'),
    )
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    categoria = models.CharField(max_length=10, choices=CATEGORIAS)
    imagem_capa = models.ImageField(upload_to='cursos/', blank=True, null=True)
    
    # ALTERADO: Aponta para o usuário padrão do sistema (core.CustomUser)
    professor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cursos_criados')
    
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

class Modulo(models.Model):
    curso = models.ForeignKey(Curso, related_name='modulos', on_delete=models.CASCADE)
    titulo = models.CharField(max_length=150)
    ordem = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.curso.titulo} - {self.titulo}"

class Conteudo(models.Model):
    TIPOS = (
        ('VIDEO', 'Vídeo Upload'),
        ('YOUTUBE', 'Link do YouTube'),
        ('PDF', 'Documento PDF'),
        ('LIVE', 'Transmissão Ao Vivo'),
        ('EXERCICIO', 'Exercício/Avaliação'),
    )
    modulo = models.ForeignKey(Modulo, related_name='conteudos', on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    tipo = models.CharField(max_length=10, choices=TIPOS)
    arquivo = models.FileField(upload_to='aulas/', blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    texto_apoio = models.TextField(blank=True)

    def __str__(self):
        return self.titulo

class Matricula(models.Model):
    # ALTERADO: Aponta para o usuário padrão do sistema
    aluno = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='matriculas_lumenios', on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, related_name='alunos', on_delete=models.CASCADE)
    progresso = models.FloatField(default=0.0)
    data_matricula = models.DateTimeField(auto_now_add=True)