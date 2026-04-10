import os
import django
import sys
import sqlite3
import random
import uuid
import re
from datetime import date, datetime

# 1. Configura Ambiente Django e Encoding
sys.stdout.reconfigure(encoding='utf-8')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'niocortex.settings')
django.setup()

from django.core.management import call_command
from core.models import CustomUser, School
from django.contrib.auth.models import Group

# Tenta importar Pedagogico (se falhar, segue sem turmas reais)
try:
    from lumenios.pedagogico.models import Turma, Aluno
except ImportError:
    Turma = None
    Aluno = None

# ==============================================================================
# UTILITÁRIOS DE DADOS RANDÔMICOS
# ==============================================================================
CIDADES = ["Salvador", "São Paulo", "Rio de Janeiro", "Curitiba", "Belo Horizonte", "Feira de Santana"]
ATUACOES = ["Tecnologia", "Educação", "Saúde", "Artes", "Engenharia", "Estudante"]
RELACIONAMENTOS = ["SOLTEIRO", "NAMORANDO", "CASADO"]

def gerar_cpf():
    return f"{random.randint(100,999)}.{random.randint(100,999)}.{random.randint(100,999)}-{random.randint(10,99)}"

def gerar_telefone():
    return f"(71) 9{random.randint(1000,9999)}-{random.randint(1000,9999)}"

def gerar_matricula_simples():
    """Gera uma matrícula baseada em Ano + Random para garantir unicidade"""
    ano = date.today().year
    return f"{ano}{random.randint(100000, 999999)}"

def gerar_nascimento(tipo='JOVEM'):
    ano_atual = date.today().year
    if tipo == 'ADULTO':
        ano = ano_atual - random.randint(25, 50)
    elif tipo == 'JOVEM':
        ano = ano_atual - random.randint(14, 18)
    elif tipo == 'BEBE':
        ano = ano_atual - random.randint(0, 2)
    return date(ano, random.randint(1, 12), random.randint(1, 28))

def get_defaults_padrao(role='ALUNO', tipo_idade='JOVEM'):
    """Retorna dicionário com todos os campos obrigatórios preenchidos randomicamente"""
    cidade = random.choice(CIDADES)
    return {
        'cpf': gerar_cpf(),
        'telefone': gerar_telefone(),
        'endereco': f"Rua Aleatória, {random.randint(1,999)}, Bairro Centro",
        'cidade_natal': cidade,
        'cidade_atual': cidade,
        'data_nascimento': gerar_nascimento(tipo_idade),
        'genero': random.choice(['Masculino', 'Feminino', 'Outro']),
        'bio': 'Usuário do sistema NioCortex.',
        'hobby': 'Estudar e Tecnologia',
        'atuacao': 'Estudante' if role == 'ALUNO' else random.choice(ATUACOES),
        'local_trabalho': 'NioCortex' if role != 'ALUNO' else '',
        'instituicao_ensino': 'Colégio Estadual' if role == 'ALUNO' else 'Universidade Federal',
        'status_relacionamento': random.choice(RELACIONAMENTOS),
        'is_premium': True, # Todo mundo premium no teste
        'role': role,
        'nivel_ensino': 'medio' if role == 'ALUNO' else 'superior',
        'fase_vida': tipo_idade,
        # Garante matricula na criação para o Signal pegar corretamente
        'matricula': gerar_matricula_simples() 
    }

# ==============================================================================
# ETAPAS DO PROCESSO
# ==============================================================================

def migrar_estrutura():
    print("\n>>> [1/5] Atualizando Banco de Dados (Migrações)...")
    try:
        call_command('makemigrations', 'core')
        call_command('migrate', 'core')
        # call_command('migrate') # Descomente para rodar geral se precisar
        print("    [OK] Estrutura atualizada.")
    except Exception as e:
        print(f"    [AVISO] Erro na migração: {e}")

def criar_escola_base():
    print("\n>>> [2/5] Garantindo Escola Base...")
    escola, _ = School.objects.get_or_create(
        nome='Niocortex Central',
        defaults={'tipo': 'SaaS_Head'}
    )
    if not escola.tenant_id:
        escola.tenant_id = uuid.uuid4()
        escola.save()
    return escola

def processar_admin_ian(escola):
    print("\n>>> [3/5] Configurando Admin SUPREMO: Ian Santos...")
    
    # Dados Específicos Solicitados
    ian_defaults = get_defaults_padrao('DIRETOR', 'ADULTO')
    ian_defaults.update({
        'first_name': 'Ian',
        'last_name': 'Santos',
        'email': 'ianwokrtech@gmail.com',
        'data_nascimento': date(1993, 4, 29),
        'cpf': '000.000.000-01',
        'is_staff': True,
        'is_superuser': True,
        'is_gestor': True,
        'is_professor': True,
        'school': escola,
        'tenant_id': escola.tenant_id,
        'bio': 'Criador e Administrador do NioCortex.',
        'atuacao': 'Full Stack Developer & Professor',
        'matricula': 'IANADMIN01'
    })

    ian, created = CustomUser.objects.update_or_create(
        username='iansantos',
        defaults=ian_defaults
    )
    ian.set_password('134679') # Senha solicitada
    ian.save()
    print(f"    [OK] Ian Santos configurado. (Senha: 134679)")

def processar_txt_alunos(escola):
    print("\n>>> [4/5] Processando alunos.txt (Ensino Médio)...")
    arquivo_txt = 'alunos.txt'
    
    if not os.path.exists(arquivo_txt):
        print("    [!] alunos.txt não encontrado.")
        return

    # Preparar Turmas
    turmas_objs = []
    if Turma:
        for nome in ['1º Ano A', '2º Ano A', '3º Ano A']:
            t, _ = Turma.objects.get_or_create(nome=nome, defaults={'ano_letivo': 2026})
            turmas_objs.append(t)

    with open(arquivo_txt, 'r', encoding='utf-8') as f:
        conteudo = f.read()
    
    nomes = re.findall(r"Creating user for: (.*?) ->", conteudo)
    
    count = 0
    for nome_completo in nomes:
        nome_completo = nome_completo.strip().title()
        parts = nome_completo.split()
        first = parts[0]
        last = " ".join(parts[1:]) if len(parts) > 1 else ""
        username = f"{first.lower()}.{parts[1].lower() if len(parts)>1 else ''}{random.randint(10,99)}"
        
        defaults = get_defaults_padrao('ALUNO', 'JOVEM')
        defaults.update({
            'first_name': first,
            'last_name': last,
            'email': f"{username}@niocortex.com",
            'school': escola,
            'tenant_id': escola.tenant_id,
            'is_aluno': True,
            'turma': random.choice(turmas_objs) if turmas_objs else None
        })

        user, created = CustomUser.objects.update_or_create(
            username=username,
            defaults=defaults
        )
        if created:
            user.set_password('123456')
            user.save() # Signal dispara criação do Aluno
            count += 1
            
    print(f"    [OK] {count} novos alunos processados de {len(nomes)} nomes.")

def casos_uso_especiais(escola):
    print("\n>>> [5/5] Criando Casos de Uso Especiais (Faculdade & Maternal)...")
    
    # 1. Ana (Faculdade)
    ana_defaults = get_defaults_padrao('ALUNO', 'ADULTO')
    ana_defaults.update({
        'first_name': 'Ana', 'last_name': 'Uni',
        'email': 'ana.uni@niocortex.com',
        'nivel_ensino': 'superior',
        'instituicao_ensino': 'Universidade NioCortex',
        'school': escola, 'is_aluno': True,
        'matricula': 'UNI2026ANA'
    })
    ana, _ = CustomUser.objects.update_or_create(username='ana_uni', defaults=ana_defaults)
    ana.set_password('ana123456')
    ana.save()

    # 2. Bebê (Maternal) e Pais
    bebe_defaults = get_defaults_padrao('ALUNO', 'BEBE')
    bebe_defaults.update({
        'first_name': 'Enzo', 'last_name': 'Baby',
        'email': 'enzo.baby@niocortex.com',
        'nivel_ensino': 'infantil',
        'fase_vida': 'INFANCIA',
        'school': escola,
        'matricula': 'BABY2026ENZO'
    })
    bebe, _ = CustomUser.objects.update_or_create(username='bebe_enzo', defaults=bebe_defaults)
    bebe.set_password('123456'); bebe.save()
    
    pai_defaults = get_defaults_padrao('RESPONSAVEL', 'ADULTO')
    pai_defaults.update({'matricula': 'PAI2026'})
    pai, _ = CustomUser.objects.update_or_create(username='pai_enzo', defaults=pai_defaults)
    pai.set_password('123456'); pai.save()
    
    print("    [OK] Perfis especiais criados.")

if __name__ == '__main__':
    migrar_estrutura() 
    escola = criar_escola_base()
    processar_admin_ian(escola)
    processar_txt_alunos(escola)
    casos_uso_especiais(escola)
    
    print("\n=== SISTEMA PRONTO PARA USO ===")
    print("Login Ian: iansantos / 134679")