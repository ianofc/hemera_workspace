import os
import django
import sys
import sqlite3
import random
import uuid
import re
from datetime import date, datetime

# 1. Configura Ambiente Django
sys.stdout.reconfigure(encoding='utf-8')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'niocortex.settings')
django.setup()

from core.models import CustomUser, School
from django.contrib.auth.models import Group
from django.conf import settings

# Tenta importar modelos específicos (com tratamento de erro)
try:
    from lumenios.pedagogico.models import Turma, Aluno
except ImportError:
    print("[AVISO] App Pedagogico não encontrado. As turmas serão criadas apenas como grupos/referência.")
    Turma = None
    Aluno = None

# ==============================================================================
# 2. FUNÇÕES UTILITÁRIAS
# ==============================================================================
def gerar_cpf():
    return f"{random.randint(100,999)}.{random.randint(100,999)}.{random.randint(100,999)}-{random.randint(10,99)}"

def gerar_nascimento_adolescente():
    """Gera data para alunos de 14 a 18 anos"""
    ano_atual = date.today().year
    ano = ano_atual - random.randint(14, 18)
    return date(ano, random.randint(1, 12), random.randint(1, 28))

def get_db_path(filename):
    """Encontra os bancos de dados na estrutura de pastas"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # Procura na pasta de backup especifica
    path = os.path.join(base_dir, 'backup_cortex_2025-11-27_07-10', filename)
    if os.path.exists(path):
        return path
    return None

# ==============================================================================
# 3. ETAPA 1: ORQUESTRAR SEED.PY (Base)
# ==============================================================================
def run_seed_base():
    print("\n>>> [1/6] Executando Seed Base (Escola)...")
    escola, _ = School.objects.get_or_create(
        nome='Niocortex Central',
        defaults={'tipo': 'SaaS_Head'}
    )
    if not escola.tenant_id:
        escola.tenant_id = uuid.uuid4()
        escola.save()
    print(f"    Escola Garantida: {escola.nome}")
    return escola

# ==============================================================================
# 4. ETAPA 2: MIGRAR DO SQLITE (migrar_ian_v2.py adaptado)
# ==============================================================================
def run_sqlite_migration(escola):
    print("\n>>> [2/6] Migrando dados dos Backups SQLite...")
    
    db_alunos = get_db_path('gestao_alunos.db')
    
    if not db_alunos:
        print("    [!] Arquivo gestao_alunos.db não encontrado. Pulando importação legado.")
        return

    try:
        conn = sqlite3.connect(db_alunos)
        cursor = conn.cursor()
        
        # Tenta ler a tabela de alunos (ajuste o nome da tabela conforme seu backup real)
        # Assumindo que existe uma tabela 'alunos' ou similar. 
        # Se não souber o nome, listamos as tabelas:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"    Tabelas encontradas no SQLite: {tables}")
        
        # Lógica genérica de importação (adaptar se a tabela tiver outro nome)
        if ('alunos',) in tables:
            cursor.execute("SELECT nome, email FROM alunos")
            for linha in cursor.fetchall():
                nome, email = linha
                if not email: email = f"{nome.split()[0].lower()}@escola.com"
                
                user, created = CustomUser.objects.get_or_create(
                    username=nome.split()[0].lower() + '_' + str(random.randint(100,999)),
                    defaults={
                        'first_name': nome.split()[0],
                        'email': email,
                        'school': escola,
                        'role': 'ALUNO'
                    }
                )
        conn.close()
        print("    Importação SQLite concluída.")
    except Exception as e:
        print(f"    [!] Erro ao ler SQLite: {e}")

# ==============================================================================
# 5. ETAPA 3: PROCESSAR ALUNOS.TXT
# ==============================================================================
def processar_txt_alunos(escola):
    print("\n>>> [3/6] Processando alunos.txt...")
    arquivo_txt = 'alunos.txt'
    
    if not os.path.exists(arquivo_txt):
        print("    [!] alunos.txt não encontrado.")
        return

    turmas_nomes = ['1º Ano A', '2º Ano A', '3º Ano A']
    turmas_objs = []
    
    # Cria turmas se o modulo pedagogico existir
    if Turma:
        for nome in turmas_nomes:
            t, _ = Turma.objects.get_or_create(nome=nome, defaults={'ano_letivo': 2026})
            turmas_objs.append(t)

    with open(arquivo_txt, 'r', encoding='utf-8') as f:
        conteudo = f.read()
    
    # Regex para extrair nomes do log "Creating user for: NOME COMPLETO ->"
    nomes = re.findall(r"Creating user for: (.*?) ->", conteudo)
    
    count = 0
    for nome_completo in nomes:
        nome_completo = nome_completo.strip().title()
        parts = nome_completo.split()
        first_name = parts[0]
        last_name = " ".join(parts[1:]) if len(parts) > 1 else ""
        username = f"{first_name.lower()}.{last_name.split()[0].lower() if last_name else ''}{random.randint(10,99)}"
        
        # Sorteia turma
        minha_turma = random.choice(turmas_objs) if turmas_objs else None
        
        user, created = CustomUser.objects.update_or_create(
            username=username,
            defaults={
                'first_name': first_name,
                'last_name': last_name,
                'email': f"{username}@niocortex.edu",
                'role': 'ALUNO',
                'school': escola,
                'tenant_id': escola.tenant_id,
                'cpf': gerar_cpf(),
                'data_nascimento': gerar_nascimento_adolescente(),
                'nivel_ensino': 'medio',
                'fase_vida': 'JOVEM',
                'turma': minha_turma, # Vincula à turma
                'is_aluno': True
            }
        )
        if created:
            user.set_password('123456')
            user.save()
            count += 1
            
    print(f"    {count} alunos importados do TXT e matriculados no Ensino Médio.")

# ==============================================================================
# 6. ETAPA 4: SEU PERFIL (IAN SANTOS)
# ==============================================================================
def configurar_admin(escola):
    print("\n>>> [4/6] Configurando Admin Ian Santos...")
    ian, _ = CustomUser.objects.update_or_create(
        username='iansantos',
        defaults={
            'first_name': 'Ian',
            'last_name': 'Santos',
            'email': 'ian@niocortex.com.br',
            'role': 'DIRETOR',
            'data_nascimento': date(1993, 4, 29), # 29-04-1993
            'cpf': '000.000.000-01',
            'is_staff': True,
            'is_superuser': True,
            'is_gestor': True,
            'is_professor': True,
            'school': escola,
            'tenant_id': escola.tenant_id,
            'nivel_ensino': 'medio',
            'fase_vida': 'ADULTO'
        }
    )
    ian.set_password('134679') # Senha solicitada
    ian.save()
    print("    [OK] Ian Santos configurado.")

# ==============================================================================
# 7. ETAPA 5: PERFIS EXTRAS (Ana Uni + Bebê)
# ==============================================================================
def criar_perfis_extras(escola):
    print("\n>>> [5/6] Criando Perfis Extras...")
    
    # Ana Faculdade
    ana, _ = CustomUser.objects.update_or_create(
        username='ana_uni',
        defaults={
            'first_name': 'Ana', 'last_name': 'Universitária',
            'role': 'ALUNO', 'nivel_ensino': 'superior',
            'school': escola, 'is_aluno': True
        }
    )
    ana.set_password('ana123456')
    ana.save()
    
    # Bebê e Pais
    bebe, _ = CustomUser.objects.update_or_create(
        username='bebe_maternal',
        defaults={
            'first_name': 'Enzo', 'role': 'ALUNO', 'nivel_ensino': 'infantil',
            'data_nascimento': date(2024, 1, 1), 'school': escola
        }
    )
    bebe.set_password('123456'); bebe.save()
    
    mae, _ = CustomUser.objects.update_or_create(
        username='mae_bebe', defaults={'first_name': 'Maria', 'role': 'RESPONSAVEL'}
    )
    mae.set_password('123456'); mae.save()
    print("    [OK] Perfis extras criados.")

# ==============================================================================
# 8. ETAPA 6: MATRÍCULAS
# ==============================================================================
def gerar_matriculas():
    print("\n>>> [6/6] Gerando Matrículas...")
    users = CustomUser.objects.filter(matricula__isnull=True)
    count = 0
    ano = date.today().year
    for u in users:
        u.matricula = f"{ano}{u.id}{random.randint(100,999)}"
        u.save()
        count += 1
    print(f"    [OK] {count} novas matrículas geradas.")

# ==============================================================================
# EXECUÇÃO PRINCIPAL
# ==============================================================================
if __name__ == '__main__':
    escola_obj = run_seed_base()
    run_sqlite_migration(escola_obj)
    processar_txt_alunos(escola_obj)
    configurar_admin(escola_obj)
    criar_perfis_extras(escola_obj)
    gerar_matriculas()
    print("\n=== MIGRACAO FINAL CONCLUIDA COM SUCESSO ===")