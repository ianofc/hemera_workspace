from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models import CustomUser

# Tenta importar modelos satélites
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
        
        # 1. Integração com Pedagógico
        if instance.role == 'ALUNO' and Aluno:
            try:
                # [CORREÇÃO] Passamos apenas matricula e turma. 
                # O 'nome' é pego via instance.first_name quando precisar exibir.
                Aluno.objects.get_or_create(
                    usuario=instance,
                    defaults={
                        'matricula': instance.matricula,
                        'turma': instance.turma
                    }
                )
            except Exception as e:
                print(f"   [!] Erro ao criar Aluno auto: {e}")

        # 2. Integração com Social (Álbuns)
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
    # Sincronização unidirecional Core -> Satélites
    if instance.role == 'ALUNO' and Aluno:
        try:
            # Se já tem perfil escolar, atualiza a matricula e turma caso tenham mudado no Core
            if hasattr(instance, 'perfil_escolar'):
                perfil = instance.perfil_escolar
                mudou = False
                
                if perfil.matricula != instance.matricula:
                    perfil.matricula = instance.matricula
                    mudou = True
                
                if perfil.turma != instance.turma:
                    perfil.turma = instance.turma
                    mudou = True
                
                if mudou:
                    perfil.save()
        except Exception as e:
            # print(f"Erro sync signal: {e}")
            pass