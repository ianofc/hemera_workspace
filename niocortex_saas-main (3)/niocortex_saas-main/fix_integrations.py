import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip())
    print(f"✅ Arquivo corrigido: {path}")

# ==============================================================================
# 1. CORE SIGNALS (CORRIGIDO)
# ==============================================================================
# - Removemos a referência ao model 'Profile' (que não existe mais).
# - Corrigimos a criação de Aluno para usar 'usuario=' em vez de 'user='.
# - Adicionamos a criação automática do Álbum "Fotos de Perfil".

core_signals = """
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from core.models import CustomUser

# Tenta importar os modelos satélites (com tratamento de erro para evitar crash)
try:
    from lumenios.pedagogico.models import Aluno
except ImportError:
    Aluno = None

try:
    from yourlife.social.models import Album
except ImportError:
    Album = None

@receiver(post_save, sender=CustomUser)
def gerenciar_integracoes_usuario(sender, instance, created, **kwargs):
    if created:
        print(f"   ---> [Signal] Integrando usuário: {instance.username}")
        
        # 1. Integração com Pedagógico (Cria Aluno se for role='ALUNO')
        if instance.role == 'ALUNO' and Aluno:
            try:
                Aluno.objects.get_or_create(
                    usuario=instance, # CORREÇÃO: O campo é 'usuario', não 'user'
                    defaults={
                        'nome': f"{instance.first_name} {instance.last_name}",
                        'matricula': instance.matricula,
                        'turma': instance.turma
                    }
                )
            except Exception as e:
                print(f"   [!] Erro ao criar Aluno auto: {e}")

        # 2. Integração com Social (Cria Álbum Padrão)
        if Album:
            try:
                Album.objects.get_or_create(
                    usuario=instance,
                    titulo="Fotos de Perfil",
                    defaults={
                        'descricao': 'Album automático para fotos de perfil',
                        'privacidade': 'PUBLIC'
                    }
                )
                Album.objects.get_or_create(
                    usuario=instance,
                    titulo="Linha do Tempo",
                    defaults={'privacidade': 'PUBLIC'}
                )
            except Exception as e:
                print(f"   [!] Erro ao criar Álbuns auto: {e}")

@receiver(post_save, sender=CustomUser)
def salvar_integracoes(sender, instance, **kwargs):
    # Atualiza dados do Aluno se o User mudar
    if instance.role == 'ALUNO' and Aluno:
        try:
            if hasattr(instance, 'aluno_perfil'):
                instance.aluno_perfil.save()
        except:
            pass
"""

# ==============================================================================
# 2. PEDAGOGICO MODELS (GARANTIA)
# ==============================================================================
# Garante que o campo seja 'usuario' para bater com o signal acima.

pedagogico_models = """
from django.db import models
from django.conf import settings

class Turma(models.Model):
    nome = models.CharField(max_length=100)
    ano_letivo = models.IntegerField(default=2026)
    periodo = models.CharField(max_length=20, default='Matutino')
    def __str__(self): return self.nome

class Aluno(models.Model):
    # Link direto com o Auth User
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='aluno_perfil'
    )
    
    # Dados redundantes para performance ou histórico
    nome = models.CharField(max_length=255)
    matricula = models.CharField(max_length=50, blank=True)
    turma = models.ForeignKey(Turma, on_delete=models.SET_NULL, null=True, blank=True, related_name='alunos')
    
    # Dados acadêmicos específicos
    nota_media = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    frequencia = models.DecimalField(max_digits=5, decimal_places=2, default=100.0)
    
    # Responsável
    nome_responsavel = models.CharField(max_length=255, blank=True)
    telefone_responsavel = models.CharField(max_length=20, blank=True)

    def __str__(self): return f"Aluno: {self.nome}"

class Disciplina(models.Model):
    nome = models.CharField(max_length=100)
    professor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='disciplinas')
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name='disciplinas')
    def __str__(self): return f"{self.nome} ({self.turma})"

# ... Outros modelos (Frequencia, Nota) podem ser adicionados aqui se necessário
"""

if __name__ == "__main__":
    write_file('core/signals.py', core_signals)
    write_file('lumenios/pedagogico/models.py', pedagogico_models)
    
    print("\n--- CORREÇÃO DE INTEGRAÇÃO CONCLUÍDA ---")
    print("1. core/signals.py foi reescrito para parar de buscar 'Profile' e usar 'usuario'.")
    print("2. Agora você pode rodar 'python orchestrator.py' novamente.")