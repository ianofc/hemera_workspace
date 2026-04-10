from django.db import models
from django.conf import settings
from django.utils import timezone

User = settings.AUTH_USER_MODEL

class Post(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    conteudo = models.TextField(blank=True, null=True)
    imagem = models.ImageField(upload_to='posts/imgs/', blank=True, null=True)
    video = models.FileField(upload_to='posts/videos/', blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Post de {self.autor} em {self.data_criacao}"

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='curtidas')
    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

class Comentario(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comentarios')
    conteudo = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentário de {self.user} no post {self.post.id}"

class Story(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stories')
    imagem = models.ImageField(upload_to='stories/imgs/', blank=True, null=True)
    video = models.FileField(upload_to='stories/videos/', blank=True, null=True)
    legenda = models.CharField(max_length=200, blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    expira_em = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.expira_em:
            self.expira_em = timezone.now() + timezone.timedelta(hours=24)
        super().save(*args, **kwargs)

class Grupo(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    capa = models.ImageField(upload_to='grupos/capas/', blank=True, null=True)
    membros = models.ManyToManyField(User, related_name='grupos_participantes')
    
    def __str__(self):
        return self.nome

class Evento(models.Model):
    criador = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    data_inicio = models.DateTimeField()
    local = models.CharField(max_length=200)
    participantes = models.ManyToManyField(User, related_name='eventos_confirmados', blank=True)

    def __str__(self):
        return self.titulo

class Friendship(models.Model):
    user_from = models.ForeignKey(User, related_name='friendship_creator', on_delete=models.CASCADE)
    user_to = models.ForeignKey(User, related_name='friendship_receiver', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('PENDING', 'Pendente'), ('ACCEPTED', 'Aceito')], default='PENDING')

    class Meta:
        unique_together = ('user_from', 'user_to')

class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    link = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Notificação para {self.recipient}: {self.message}"
