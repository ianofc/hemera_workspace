import os
import sys
import django
import sqlite3
import uuid
import random
from datetime import date, timedelta

# Configuração do Django
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'niocortex.settings')
django.setup()

from core.models import CustomUser, School
from lumenios.pedagogico.models import Turma, Aluno
from yourlife.social.models import Friendship

BACKUP_SQLITE = r"C:\Users\Ian Santos\Desktop\VSCODE\MultiVerso IO\niocortex_saas\backup_cortex_2025-11-27_07-10\gestao_alunos.db"
AVATAR_API = "https://ui-avatars.com/api/?name={}&background=random&color=fff&size=256"
COVER_API = "https://picsum.photos/seed/{}/1200/400"

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def get_random_dob(fase_vida):
    today = date.today()
    if fase_vida == 'BEBE': start_date = today - timedelta(days=365*3)
    elif fase_vida == 'CRIANCA': start_date = today - timedelta(days=365*12)
    elif fase_vida == 'JOVEM': start_date = today - timedelta(days=365*18)
    elif fase_vida == 'ADULTO': start_date = today - timedelta(days=365*30)
    else: return date(2000, 1, 1)
    
    end_date = today - timedelta(days=365)
    if start_date >= end_date: start_date = end_date - timedelta(days=1)
    
    days_between = (end_date - start_date).days
    return start_date + timedelta(days=random.randrange(days_between))

def get_fase_nivel(nome_turma):
    nome = nome_turma.lower()
    if 'infantil' in nome or 'pre' in nome: return 'bebe', 'BEBE'
    if 'fundamental' in nome: return 'fundamental', 'CRIANCA'
    if 'medio' in nome or 'médio' in nome: return 'medio', 'JOVEM'
    if 'superior' in nome: return 'superior', 'ADULTO'
    return 'medio', 'JOVEM'

def run_migration():
    print("🚀 INICIANDO MIGRAÇÃO V5 (CORREÇÃO DE TIPOS)...")

    # 1. CRIAR ESCOLA PADRÃO
    escola, _ = School.objects.get_or_create(nome="NioCortex Academy", defaults={'tipo': 'PRIVATE'})

    # 2. CRIAR IAN
    ian, created = CustomUser.objects.get_or_create(
        username='ian',
        defaults={
            'email': 'ianworktech@gmail.com', 'first_name': 'Ian', 'last_name': 'Santos',
            'role': 'PROFESSOR', 'is_staff': True, 'is_superuser': True, 'is_premium': True,
            'tenant_type': 'INDIVIDUAL', 'nivel_ensino': 'superior', 'fase_vida': 'ADULTO',
            'data_nascimento': date(1993, 4, 29), 'genero': 'M',
            'avatar': 'uploads/imgs/perfil_1_1764786138.jpeg'
        }
    )
    if created: 
        ian.set_password('123456')
        ian.save()
        print("✅ Ian criado.")
    else: 
        print("ℹ️  Ian já existe.")

    # 3. CONECTAR AO SQLITE
    if not os.path.exists(BACKUP_SQLITE):
        print(f"❌ Backup não encontrado: {BACKUP_SQLITE}")
        return

    conn = sqlite3.connect(BACKUP_SQLITE)
    conn.row_factory = dict_factory
    cursor = conn.cursor()

    # 4. MIGRAR
    cursor.execute("SELECT * FROM turmas")
    turmas_old = cursor.fetchall()
    print(f"📦 Importando {len(turmas_old)} turmas...")

    for t_old in turmas_old:
        # Criar Turma
        turma_dj, _ = Turma.objects.get_or_create(
            nome=t_old['nome'],
            defaults={'ano_letivo': 2025, 'professor_regente': ian, 'tenant_id': str(uuid.uuid4())}
        )
        
        nivel, fase = get_fase_nivel(t_old['nome'])
        cursor.execute("SELECT * FROM alunos WHERE id_turma = ?", (t_old['id'],))
        alunos_old = cursor.fetchall()
        
        for a_old in alunos_old:
            nome = a_old['nome']
            parts = nome.split()
            first = parts[0]
            last = ' '.join(parts[1:]) if len(parts) > 1 else 'Aluno'
            username = f"{first.lower()}.{last.lower().replace(' ', '')}"[:20]
            
            if CustomUser.objects.filter(username=username).exists():
                username = f"{username}{random.randint(10,99)}"

            dob = get_random_dob(fase)
            
            # --- CRIAÇÃO SEGURA DO USUÁRIO ---
            user_aluno, created_u = CustomUser.objects.get_or_create(
                username=username,
                defaults={
                    'first_name': first, 'last_name': last,
                    'email': a_old.get('email_responsavel', f"{username}@niocortex.com"),
                    'role': 'ALUNO', 'nivel_ensino': nivel, 'fase_vida': fase,
                    'is_premium': False, 'data_nascimento': dob, 'genero': random.choice(['M', 'F']),
                    'school': escola,
                    'bio': f'Aluno de {t_old["nome"]}'
                }
            )
            
            if created_u:
                user_aluno.set_password('123456')
                user_aluno.save()

            # Tenta vincular turma no User (Se falhar por tipo, ignora, pois o vínculo principal é no Aluno)
            try:
                user_aluno.turma = turma_dj
                user_aluno.save()
            except:
                pass 

            # --- CRIAÇÃO DO ALUNO (COM VÍNCULO CORRETO) ---
            if not Aluno.objects.filter(nome=nome).exists():
                Aluno.objects.create(
                    nome=nome,
                    turma=turma_dj, 
                    matricula_id=f"2025-{turma_dj.id}-{random.randint(1000,9999)}",
                    usuario=user_aluno, # Aqui vai funcionar agora que a coluna existe
                    tenant_id=turma_dj.tenant_id
                )

            # Social
            Friendship.objects.get_or_create(user_from=ian, user_to=user_aluno, status='ACCEPTED')
            Friendship.objects.get_or_create(user_from=user_aluno, user_to=ian, status='ACCEPTED')

        print(f"   ↳ Turma '{t_old['nome']}' ok.")

    conn.close()

    # 5. ANA UNIVERSITÁRIA
    ana, created_ana = CustomUser.objects.get_or_create(
        username='ana_uni',
        defaults={
            'email': 'ana@uni.com', 'first_name': 'Ana', 'last_name': 'Silva',
            'role': 'ALUNO', 'nivel_ensino': 'superior', 'fase_vida': 'ADULTO',
            'is_premium': True, 'school': escola, 'data_nascimento': date(2003, 5, 15)
        }
    )
    if created_ana:
        ana.set_password('123')
        ana.save()
        Friendship.objects.get_or_create(user_from=ian, user_to=ana, status='ACCEPTED')
        Friendship.objects.get_or_create(user_from=ana, user_to=ian, status='ACCEPTED')
        print("✅ Ana criada.")
    else:
        print("ℹ️  Ana já existe.")

    print("\n🎉 SUCESSO TOTAL! SERVIDOR PRONTO.")

if __name__ == "__main__":
    run_migration()