import os
import sys
import django
import uuid

# 1. Configura o ambiente Django para rodar scripts soltos
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'niocortex.settings')
django.setup()

# 2. Importa os modelos do Django
from core.models import CustomUser, School
from lumenios.pedagogico.models import Aluno, Turma

def seed_database():
    print("🌱 Iniciando o plantio de dados (Seeding Django)...")

    # ------------------------------------------------------------------
    # 1. CRIAR ESCOLAS (Tenants)
    # ------------------------------------------------------------------
    escola_privada, _ = School.objects.get_or_create(
        nome="Colégio Cortex Elite",
        defaults={'tenant_id': uuid.uuid4()}
    )
    
    escola_publica, _ = School.objects.get_or_create(
        nome="Escola Estadual Paulo Freire",
        defaults={'tenant_id': uuid.uuid4()}
    )
    
    print("✅ Escolas verificadas.")

    # ------------------------------------------------------------------
    # 2. CRIAR USUÁRIOS DE STAFF
    # ------------------------------------------------------------------
    # Mapeamento de Roles do Django (conforme core/models.py)
    users_data = [
        {"username": "diretor_elite", "email": "diretor@cortex.com", "first": "Diretor", "last": "Augusto", "role": "DIRECAO", "escola": escola_privada},
        {"username": "coord_mariana", "email": "coord@cortex.com", "first": "Coord.", "last": "Mariana", "role": "COORDENACAO", "escola": escola_privada},
        {"username": "sec_roberto", "email": "sec@cortex.com", "first": "Sec.", "last": "Roberto", "role": "SECRETARIA", "escola": escola_privada},
        {"username": "prof_claudio", "email": "prof.biologia@cortex.com", "first": "Prof.", "last": "Cláudio", "role": "PROFESSOR_CORP", "escola": escola_privada},
        {"username": "diretora_lucia", "email": "diretor@publica.com", "first": "Diretora", "last": "Lúcia", "role": "DIRECAO", "escola": escola_publica},
    ]

    for u in users_data:
        user, created = CustomUser.objects.get_or_create(
            username=u["username"],
            defaults={
                "email": u["email"],
                "first_name": u["first"],
                "last_name": u["last"],
                "role": u["role"],
                "school": u["escola"],
                "tenant_id": u["escola"].tenant_id,
                "tenant_type": 'SCHOOL'
            }
        )
        if created:
            user.set_password("123456") # Define a senha com hash do Django
            user.save()
    
    print("✅ Staff criado/atualizado (Senha padrão: 123456).")

    # ------------------------------------------------------------------
    # 3. ATUALIZAR SEU USUÁRIO (ADMIN SUPREMO)
    # ------------------------------------------------------------------
    meu_usuario = CustomUser.objects.filter(username='iansantos').first() or \
                  CustomUser.objects.filter(email='ianworktech@gmail.com').first()

    if not meu_usuario:
        meu_usuario = CustomUser(username='iansantos')

    meu_usuario.email = "ianworktech@gmail.com"
    meu_usuario.first_name = "Ian"
    meu_usuario.last_name = "Santos (Admin)"
    meu_usuario.role = 'ADMIN'
    meu_usuario.is_staff = True
    meu_usuario.is_superuser = True
    meu_usuario.tenant_type = 'INDIVIDUAL'
    
    if not meu_usuario.tenant_id:
        meu_usuario.tenant_id = uuid.uuid4()
    
    meu_usuario.set_password("134679")
    meu_usuario.save()
    
    print(f"👑 Usuário {meu_usuario.get_full_name()} promovido a ADMIN.")
    print(f"   Login: ianworktech@gmail.com | Senha: 134679")

    # ------------------------------------------------------------------
    # 4. CRIAR ALUNOS DE TESTE
    # ------------------------------------------------------------------
    # Cria Turma Padrão para vincular alunos
    turma_elite, _ = Turma.objects.get_or_create(
        nome="3º Ano A - Médio",
        tenant_id=escola_privada.tenant_id,
        defaults={'ano_letivo': 2025}
    )

    alunos_data = [
        {"username": "baby_enzo", "email": "baby@cortex.com", "nome": "Baby Enzo", "escola": escola_privada, "matricula": "2025-INF-01"},
        {"username": "lucas_silva", "email": "medio@cortex.com", "nome": "Lucas Silva", "escola": escola_privada, "matricula": "2025-MED-01"},
        {"username": "ana_uni", "email": "uni@publica.com", "nome": "Ana Universitária", "escola": escola_publica, "matricula": "2025-SUP-01"},
    ]

    for a in alunos_data:
        # 1. Cria Usuário de Login (CustomUser)
        parts = a["nome"].split()
        first = parts[0]
        last = " ".join(parts[1:])
        
        user_aluno, created = CustomUser.objects.get_or_create(
            username=a["username"],
            defaults={
                "email": a["email"],
                "first_name": first,
                "last_name": last,
                "role": 'ALUNO_CORP',
                "school": a["escola"],
                "tenant_id": a["escola"].tenant_id,
                "tenant_type": 'SCHOOL'
            }
        )
        if created:
            user_aluno.set_password("123456")
            user_aluno.save()

        # 2. Cria Registro Acadêmico (Aluno Pedagógico)
        # Verifica se já existe pelo nome e tenant para não duplicar
        if not Aluno.objects.filter(nome=a["nome"], tenant_id=a["escola"].tenant_id).exists():
            Aluno.objects.create(
                nome=a["nome"],
                email=a["email"],
                matricula_id=a["matricula"],
                tenant_id=a["escola"].tenant_id,
                turma=turma_elite if a["escola"] == escola_privada else None
            )

    print("✅ Alunos de teste verificados/criados.")
    print("🚀 Banco populado com sucesso!")

if __name__ == "__main__":
    seed_database()