import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models

class School(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=255)
    tipo = models.CharField(max_length=50, default='SaaS_Head', blank=True)
    tenant_id = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'escolas'  # Mapeia para a tabela do Supabase
        
    def __str__(self):
        return self.nome

class CustomUser(AbstractUser):
    # Força a chave primária a ser UUID (compatível com auth.users)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Identificação
    cpf = models.CharField(max_length=14, blank=True, null=True, unique=True)
    matricula = models.CharField(max_length=50, blank=True, null=True, unique=True)
    role = models.CharField("Cargo", max_length=20, default='ALUNO') 
    
    # Contato
    telefone = models.CharField(max_length=20, blank=True, null=True)
    endereco = models.TextField(blank=True, null=True)
    cidade_natal = models.CharField(max_length=100, blank=True, null=True)
    cidade_atual = models.CharField(max_length=100, blank=True, null=True)
    
    # Perfil
    data_nascimento = models.DateField(null=True, blank=True)
    genero = models.CharField(max_length=20, blank=True)
    bio = models.TextField(blank=True)
    hobby = models.CharField(max_length=100, blank=True)
    atuacao = models.CharField("Atuação", max_length=100, blank=True)
    local_trabalho = models.CharField("Local de Trabalho", max_length=200, blank=True)
    instituicao_ensino = models.CharField("Instituição", max_length=200, blank=True)
    status_relacionamento = models.CharField(max_length=50, blank=True)
    nivel_ensino = models.CharField(max_length=20, default='medio', null=True, blank=True)
    fase_vida = models.CharField(max_length=20, default='JOVEM', null=True, blank=True)
    
    # SaaS / Sistema
    school = models.ForeignKey('School', on_delete=models.SET_NULL, null=True, blank=True, db_column='escola_id')
    turma = models.ForeignKey('pedagogico.Turma', on_delete=models.SET_NULL, null=True, blank=True, db_column='turma_id')
    tenant_type = models.CharField(max_length=20, default='PUBLIC')
    tenant_id = models.UUIDField(null=True, blank=True)
    
    # Mídia
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    capa = models.ImageField(upload_to='covers/', blank=True, null=True)
    
    # Permissões
    is_premium = models.BooleanField(default=False)
    is_gestor = models.BooleanField(default=False)
    is_aluno = models.BooleanField(default=False)
    is_professor = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'core_customuser'  # Mantém o user em core_customuser

# --- FUNÇÕES DE UPLOAD E AUXILIARES ---
def upload_chat_attachment(instance, filename):
    return f'post/attachments/{instance.room.id}/{uuid.uuid4()}_{filename}'

class Room(models.Model):
    ROOM_TYPES = (
        ('dm', 'Direct Message'),
        ('group', 'Grupo'),
        ('channel', 'Canal'),
        ('secret', 'Chat Secreto'),
    )
    name = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=20, choices=ROOM_TYPES, default='dm')
    icon = models.ImageField(upload_to='post/group_icons/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    participants = models.ManyToManyField(CustomUser, related_name='chat_rooms')
    admins = models.ManyToManyField(CustomUser, related_name='admin_rooms', blank=True)
    permissions = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def is_group(self):
        return self.type in ['group', 'channel']

    def __str__(self):
        return self.name if self.is_group else f"Chat Privado ({self.id})"

class ChatFolder(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='chat_folders')
    name = models.CharField(max_length=100)
    rooms = models.ManyToManyField(Room, related_name='folders', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'name')
        ordering = ['created_at']

    def __str__(self):
        return f"Agora {self.name} - {self.user.username}"

class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    attachment = models.FileField(upload_to=upload_chat_attachment, blank=True, null=True)
    attachment_type = models.CharField(max_length=50, blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    reply_to = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='replies')
    is_edited = models.BooleanField(default=False)
    forward_from = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='forwarded_messages')
    is_pinned = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Msg {self.id} de {self.sender.username} em {self.room}"

