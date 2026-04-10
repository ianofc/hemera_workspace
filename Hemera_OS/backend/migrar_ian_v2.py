import os
import uuid
import sys
import django
import sqlite3

# ==============================================================================
# CONFIGURAÇÃO DO AMBIENTE
# ==============================================================================
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'niocortex.settings')
django.setup()

from core.models import CustomUser
from lumenios.pedagogico.models import Turma, Aluno

# CAMINHO DO BACKUP (Confirmado pelo seu log)
BACKUP_PATH = r"C:\Users\Ian Santos\Desktop\VSCODE\MultiVerso IO\niocortex_saas\backup_cortex_2025-11-27_07-10\gestao_alunos.db"

def conectar_sqlite():
    print(f">> Tentando abrir backup: {BACKUP_PATH}...")
    if not os.path.exists(BACKUP_PATH):
        print("❌ Erro: Arquivo não encontrado.")
        return None
    try:
        conn = sqlite3.connect(BACKUP_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        print(f"❌ Falha ao abrir o backup: {e}")
        return None

def migrar_ian():
    conn_src = conectar_sqlite()
    if not conn_src: return

    cursor_src = conn_src.cursor()
    print("\n--- 🕵️‍♀️ DIAGNÓSTICO DO BACKUP ---")

    try:
        # 1. DESCOBRIR COLUNAS DA TABELA USERS
        cursor_src.execute("PRAGMA table_info(users)")
        colunas_info = cursor_src.fetchall()
        colunas_users = [c['name'] for c in colunas_info]
        print(f"📋 Colunas na tabela 'users': {colunas_users}")

        # 2. IDENTIFICAR COLUNA DE NOME
        possiveis_nomes = ['nome', 'name', 'fullname', 'full_name', 'nome_completo', 'apelido']
        coluna_nome = next((col for col in possiveis_nomes if col in colunas_users), None)

        if coluna_nome:
            print(f"✅ Coluna de nome identificada: '{coluna_nome}'")
        else:
            print("⚠️ Nenhuma coluna de nome óbvia encontrada. Usaremos dados manuais para o nome.")

        # 3. BUSCAR O USUÁRIO
        print("\n>> Buscando usuário 'iansantos'...")
        
        query = "SELECT * FROM users WHERE username = 'iansantos'"
        if coluna_nome:
            query += f" OR {coluna_nome} LIKE '%Ian%'"
        
        cursor_src.execute(query + " LIMIT 1")
        old_user = cursor_src.fetchone()

        if not old_user:
            print("❌ Usuário 'iansantos' não encontrado no backup. Abortando.")
            return

        # 4. PREPARAR DADOS PARA O DJANGO
        # Se achou coluna de nome, usa. Se não, força "Ian Santos".
        nome_completo = old_user[coluna_nome] if coluna_nome else "Ian Santos"
        
        # Divide Nome e Sobrenome para o Django
        partes = nome_completo.strip().split()
        first_name = partes[0]
        last_name = ' '.join(partes[1:]) if len(partes) > 1 else 'Santos'
        
        email = old_user['email'] if 'email' in colunas_users else 'ian@niocortex.com'
        
        print(f"   👤 Usuário Encontrado: {nome_completo} (ID: {old_user['id']})")
        print(f"   📧 Email: {email}")

        # 5. CRIAR NO DJANGO
        tenant_uuid = uuid.uuid4()
        
        user_django, created = CustomUser.objects.get_or_create(
            username='ian',
            defaults={
                'email': email,
                'first_name': first_name,
                'last_name': last_name,
                'role': 'PROFESSOR_FREE',
                'tenant_type': 'INDIVIDUAL',
                'tenant_id': tenant_uuid,
                'is_staff': True,
                'is_superuser': True
            }
        )

        if created:
            user_django.set_password('123456')
            user_django.save()
            print("   ✅ Usuário 'ian' criado no Django com sucesso!")
        else:
            print("   ℹ️  Usuário 'ian' já existe no Django. Atualizando vínculo.")
            if not user_django.tenant_id:
                user_django.tenant_id = tenant_uuid
                user_django.save()
            tenant_uuid = user_django.tenant_id

        # 6. MIGRAR TURMAS
        print(f"\n>> Buscando turmas do ID antigo ({old_user['id']})...")
        
        # Verifica nome da coluna de link (user_id, autor_id, id_user...)
        cursor_src.execute("PRAGMA table_info(turmas)")
        cols_turmas = [c['name'] for c in cursor_src.fetchall()]
        col_fk = next((c for c in ['user_id', 'autor_id', 'id_user', 'professor_id'] if c in cols_turmas), None)
        
        if not col_fk:
            print(f"❌ Não foi possível identificar a coluna de vínculo (FK) na tabela 'turmas'. Colunas: {cols_turmas}")
            return

        cursor_src.execute(f"SELECT * FROM turmas WHERE {col_fk} = ?", (old_user['id'],))
        old_turmas = cursor_src.fetchall()
        print(f"   🏫 {len(old_turmas)} turmas encontradas.")

        mapa_turmas = {} # ID Antigo -> ID Novo

        for t in old_turmas:
            nova_turma, _ = Turma.objects.get_or_create(
                nome=t['nome'],
                tenant_id=tenant_uuid,
                professor_regente=user_django,
                defaults={'ano_letivo': 2025}
            )
            mapa_turmas[t['id']] = nova_turma.id
            print(f"      + {t['nome']} (Migrada)")

        # 7. MIGRAR ALUNOS
        print(f"\n>> Migrando alunos...")
        if mapa_turmas:
            ids_antigos = list(mapa_turmas.keys())
            placeholders = ','.join('?' for _ in ids_antigos)
            
            # Verifica colunas da tabela alunos para evitar erro
            cursor_src.execute("PRAGMA table_info(alunos)")
            cols_alunos = [c['name'] for c in cursor_src.fetchall()]
            
            # Mapeia colunas opcionais
            col_email_resp = 'email_responsavel' if 'email_responsavel' in cols_alunos else None
            col_tel_resp = 'telefone_responsavel' if 'telefone_responsavel' in cols_alunos else None
            col_matricula = 'matricula' if 'matricula' in cols_alunos else None

            query_alunos = f"SELECT * FROM alunos WHERE id_turma IN ({placeholders})"
            cursor_src.execute(query_alunos, ids_antigos)
            old_alunos = cursor_src.fetchall()
            
            print(f"   🎓 {len(old_alunos)} alunos encontrados.")

            count = 0
            for a in old_alunos:
                uuid_turma = mapa_turmas.get(a['id_turma'])
                
                # Monta os dados com segurança
                dados_aluno = {
                    'nome': a['nome'],
                    'tenant_id': tenant_uuid,
                    'turma_id': uuid_turma,
                    'email': a[col_email_resp] if col_email_resp else None,
                    'telefone_responsavel': a[col_tel_resp] if col_tel_resp else None,
                    'matricula_id': str(a[col_matricula]) if col_matricula and a[col_matricula] else None
                }

                if not Aluno.objects.filter(nome=a['nome'], turma_id=uuid_turma).exists():
                    Aluno.objects.create(**dados_aluno)
                    count += 1
            
            print(f"   ✅ {count} alunos importados.")

    except Exception as e:
        print(f"\n❌ ERRO CRÍTICO: {e}")
        import traceback
        traceback.print_exc()
    finally:
        conn_src.close()
        print("\n✅ Script finalizado.")

if __name__ == "__main__":
    migrar_ian()