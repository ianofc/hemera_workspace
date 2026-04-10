import os
import django
from django.core.management import call_command
from django.db import connection
import sqlite3
import uuid
import random
from datetime import date, timedelta

# Configuração
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'niocortex.settings')
try:
    from dotenv import load_dotenv
    load_dotenv()
except: pass

django.setup()

BACKUP_SQLITE = r"C:\Users\Ian Santos\Desktop\VSCODE\MultiVerso IO\niocortex_saas\backup_cortex_2025-11-27_07-10\gestao_alunos.db"
AVATAR_API = "https://ui-avatars.com/api/?name={}&background=random&color=fff&size=256"

# ==============================================================================
# 1. FUNÇÕES DE LIMPEZA
# ==============================================================================
def clean_migrations():
    print("🧹 Limpando migrações locais...")
    apps = ['core', 'yourlife/social', 'lumenios/pedagogico', 'lumenios/plataforma']
    for app in apps:
        mig_path = os.path.join(app.replace('/', os.sep), 'migrations')
        if os.path.exists(mig_path):
            for f in os.listdir(mig_path):
                if f != '__init__.py' and f != '__pycache__':
                    try:
                        os.remove(os.path.join(mig_path, f))
                    except: pass
    print("   [OK] Migrações deletadas.")

def reset_db_schema():
    print("☢️  RESETANDO SUPABASE (DROP SCHEMA)...")
    with connection.cursor() as cursor:
        cursor.execute("DROP SCHEMA public CASCADE;")
        cursor.execute("CREATE SCHEMA public;")
        cursor.execute("GRANT ALL ON SCHEMA public TO postgres;")
        cursor.execute("GRANT ALL ON SCHEMA public TO public;")
    print("   [OK] Banco limpo.")

# ==============================================================================
# 2. FUNÇÕES DE MIGRAÇÃO
# ==============================================================================
def create_structure():
    print("🔨 Recriando estrutura do banco...")
    call_command('makemigrations', 'core')
    call_command('makemigrations', 'yourlife_social')
    call_command('makemigrations', 'pedagogico')
    call_command('makemigrations', 'plataforma')
    
    print("🚀 Aplicando no Supabase...")
    call_command('migrate')
    print("   [OK] Tabelas criadas.")

# ==============================================================================
# 3. FUNÇÕES DE IMPORTAÇÃO (SEED)
# ==============================================================================
def get_random_dob(fase_vida):
    today = date.today()
    if fase_vida == 'BEBE': start = today - timedelta(days=365*3); end = today
    elif fase_vida == 'CRIANCA': start = today - timedelta(days=365*12); end = today - timedelta(days=365*4)
    elif fase_vida == 'JOVEM': start = today - timedelta(days=365*18); end = today - timedelta(days=365*13)
    elif fase_vida == 'ADULTO': start = today - timedelta(days=365*30); end = today - timedelta(days=365*19)
    else: return date(2000, 1, 1)
    
    delta = (end - start).days
    return start + timedelta(days=random.randrange(delta if delta > 0 else 1))

def get_fase_nivel(nome_turma):
    nome = nome_turma.lower()
    if 'infantil' in nome or 'pre' in nome: return 'bebe', 'BEBE'
    if 'fundamental' in nome: return 'fundamental', 'CRIANCA'
    if 'medio' in nome or 'médio' in nome: return 'medio', 'JOVEM'
    if 'superior' in nome: return 'superior', 'ADULTO'
    return 'medio', 'JOVEM'

def import_data():
    from core.models import CustomUser, School
    from lumenios.pedagogico.models import Turma, Aluno
    from yourlife.social.models import Friendship

    print("🌱 Importando dados...")

    # ESCOLA
    escola, _ = School.objects.get_or_create(nome="NioCortex Academy", defaults={'tipo': 'PRIVATE'})

    # IAN
    ian, _ = CustomUser.objects.get_or_create(
        username='ian',
        defaults={
            'email': 'ianworktech@gmail.com', 'first_name': 'Ian', 'last_name': 'Santos',
            'role': 'PROFESSOR', 'is_staff': True, 'is_superuser': True, 'is_premium': True,
            'tenant_type': 'INDIVIDUAL', 'nivel_ensino': 'superior', 'fase_vida': 'ADULTO',
            'data_nascimento': date(1993, 4, 29), 'genero': 'M',
            'avatar': 'uploads/imgs/perfil_1_1764786138.jpeg'
        }
    )
    ian.set_password('123456'); ian.save()
    print("   ✅ Ian criado.")

    # ANA
    ana, _ = CustomUser.objects.get_or_create(
        username='ana_uni',
        defaults={
            'email': 'ana@uni.com', 'first_name': 'Ana', 'last_name': 'Silva',
            'role': 'ALUNO', 'nivel_ensino': 'superior', 'fase_vida': 'ADULTO',
            'is_premium': True, 'school': escola, 'data_nascimento': date(2003, 5, 15)
        }
    )
    ana.set_password('123'); ana.save()
    Friendship.objects.get_or_create(user_from=ian, user_to=ana, status='ACCEPTED')
    Friendship.objects.get_or_create(user_from=ana, user_to=ian, status='ACCEPTED')
    print("   ✅ Ana criada.")

    # IMPORTAR DO SQLITE
    if not os.path.exists(BACKUP_SQLITE):
        print("   ⚠️ Backup SQLite não encontrado. Pulando importação.")
        return

    conn = sqlite3.connect(BACKUP_SQLITE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM turmas")
    turmas_old = cursor.fetchall()
    
    print(f"   📦 Importando {len(turmas_old)} turmas...")

    for t_old in turmas_old:
        turma_dj, _ = Turma.objects.get_or_create(
            nome=t_old['nome'],
            defaults={'ano_letivo': 2025, 'professor_regente': ian, 'tenant_id': str(uuid.uuid4())}
        )
        
        nivel, fase = get_fase_nivel(t_old['nome'])
        cursor.execute("SELECT * FROM alunos WHERE id_turma = ?", (t_old['id'],))
        
        for a_old in cursor.fetchall():
            nome = a_old['nome']
            parts = nome.split()
            first = parts[0]
            last = ' '.join(parts[1:]) if len(parts) > 1 else 'Aluno'
            username = f"{first.lower()}.{last.lower().replace(' ', '')}"[:20]
            
            if CustomUser.objects.filter(username=username).exists():
                username = f"{username}{random.randint(10,99)}"

            user_aluno, created = CustomUser.objects.get_or_create(
                username=username,
                defaults={
                    'first_name': first, 'last_name': last,
                    'email': a_old['email_responsavel'] if 'email_responsavel' in a_old.keys() else f"{username}@nio.com",
                    'role': 'ALUNO', 'nivel_ensino': nivel, 'fase_vida': fase,
                    'is_premium': False, 'data_nascimento': get_random_dob(fase), 'genero': 'O',
                    'school': escola
                }
            )
            if created: user_aluno.set_password('123456'); user_aluno.save()

            # Tenta vincular turma (sem crash)
            try: user_aluno.turma = turma_dj; user_aluno.save()
            except: pass

            if not Aluno.objects.filter(nome=nome).exists():
                Aluno.objects.create(
                    nome=nome, turma=turma_dj, 
                    matricula_id=f"2025-{turma_dj.id}-{random.randint(1000,9999)}",
                    usuario=user_aluno, tenant_id=turma_dj.tenant_id
                )
            
            Friendship.objects.get_or_create(user_from=ian, user_to=user_aluno, status='ACCEPTED')
            Friendship.objects.get_or_create(user_from=user_aluno, user_to=ian, status='ACCEPTED')

    conn.close()
    print("   ✅ Importação concluída.")

if __name__ == "__main__":
    clean_migrations()
    reset_db_schema()
    create_structure()
    import_data()
    print("\n🎉 SISTEMA PRONTO! Rode 'python manage.py runserver'")