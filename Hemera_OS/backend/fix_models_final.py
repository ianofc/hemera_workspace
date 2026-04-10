import os
import sys
import django
from django.core.management import call_command

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip())
    print(f"✅ Arquivo corrigido: {path}")

# MODELO CORRIGIDO (Com TODOS os campos: Sociais + Mídia + Sistema)
core_models_fixed = """
import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models

class School(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=255)
    tipo = models.CharField(max_length=50, default='SaaS_Head', blank=True)
    tenant_id = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta: db_table = 'core_school'
    def __str__(self): return self.nome

class CustomUser(AbstractUser):
    # --- Identificação ---
    cpf = models.CharField(max_length=14, blank=True, null=True, unique=True)
    matricula = models.CharField(max_length=50, blank=True, null=True, unique=True)
    role = models.CharField("Cargo", max_length=20, default='ALUNO') 
    
    # --- Contato & Localização ---
    telefone = models.CharField(max_length=20, blank=True, null=True)
    endereco = models.TextField("Endereço", blank=True, null=True)
    cidade_natal = models.CharField(max_length=100, blank=True, null=True)
    cidade_atual = models.CharField(max_length=100, blank=True, null=True)
    
    # --- Perfil Social & Profissional ---
    data_nascimento = models.DateField(null=True, blank=True)
    genero = models.CharField(max_length=20, blank=True)
    bio = models.TextField(blank=True)
    hobby = models.CharField(max_length=100, blank=True)
    atuacao = models.CharField("Área de Atuação", max_length=100, blank=True)
    local_trabalho = models.CharField("Local de Trabalho", max_length=200, blank=True)
    instituicao_ensino = models.CharField("Instituição de Ensino", max_length=200, blank=True)
    
    status_relacionamento = models.CharField(max_length=50, blank=True, choices=[
        ('SOLTEIRO', 'Solteiro(a)'), ('NAMORANDO', 'Namorando'), 
        ('CASADO', 'Casado(a)'), ('DIVORCIADO', 'Divorciado(a)')
    ])

    # --- CAMPOS RESTAURADOS (Essenciais para a lógica do sistema) ---
    nivel_ensino = models.CharField(max_length=20, default='medio', null=True, blank=True)
    fase_vida = models.CharField(max_length=20, default='JOVEM', null=True, blank=True)

    # --- Sistema / SaaS ---
    school = models.ForeignKey('School', on_delete=models.SET_NULL, null=True, blank=True)
    turma = models.ForeignKey('pedagogico.Turma', on_delete=models.SET_NULL, null=True, blank=True)
    tenant_type = models.CharField(max_length=20, default='PUBLIC')
    tenant_id = models.UUIDField(null=True, blank=True)
    
    # --- Mídia (Legado/Atalho) ---
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    capa = models.ImageField(upload_to='covers/', blank=True, null=True)

    # --- Permissões ---
    is_premium = models.BooleanField(default=False)
    is_gestor = models.BooleanField(default=False)
    is_aluno = models.BooleanField(default=False)
    is_professor = models.BooleanField(default=False)

    class Meta: db_table = 'core_customuser'
"""

if __name__ == "__main__":
    # 1. Reescreve o arquivo
    write_file('core/models.py', core_models_fixed)
    
    # 2. Configura Django para rodar migração
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'niocortex.settings')
    try:
        django.setup()
        print(">>> Criando migrações para restaurar campos...")
        call_command('makemigrations', 'core')
        print(">>> Aplicando no banco...")
        call_command('migrate', 'core')
        print("\n✅ CORREÇÃO CONCLUÍDA! Agora rode o orchestrator.py novamente.")
    except Exception as e:
        print(f"❌ Erro ao rodar migração: {e}")