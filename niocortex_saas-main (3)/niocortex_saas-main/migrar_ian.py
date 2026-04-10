import os
import uuid
import sys
import django
import psycopg2
from psycopg2.extras import RealDictCursor

# 1. Configurar o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'niocortex.settings')
django.setup()

from core.models import CustomUser
from lumenios.pedagogico.models import Turma, Aluno

# --- CONFIGURAÇÕES DE CONEXÃO (TRANSACTION POOLER - IPv4 COMPATÍVEL) ---
DB_HOST = "aws-1-us-east-2.pooler.supabase.com"
DB_NAME = "postgres"
DB_USER = "postgres.qnknyonohlorjfhzkkpz"
RAW_PASSWORD = "2511CorteXEduc"
DB_PORT = "6543"

def conectar_supabase():
    print(f">> Tentando conectar em: {DB_HOST}...")
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=RAW_PASSWORD,
            port=DB_PORT,
            sslmode='require' 
        )
        print(">> Conexão estabelecida com sucesso!")
        return conn
    except Exception as e:
        print(f"❌ Falha na conexão. Detalhe técnico:")
        print(repr(e)) 
        return None

def migrar_ian():
    conn = conectar_supabase()
    if not conn:
        print(">> Abortando: Sem conexão.")
        return

    cursor = conn.cursor(cursor_factory=RealDictCursor)
    print("--- INICIANDO MIGRAÇÃO DO 'IAN SANTOS' PARA 'IAN' ---")

    try:
        # 1. BUSCAR O USUÁRIO DE ORIGEM (IAN SANTOS - LEGADO)
        # Procuramos especificamente pelo cadastro antigo completo
        print(">> Buscando usuário de origem 'Ian Santos'...")
        cursor.execute("""
            SELECT * FROM users 
            WHERE username = 'iansantos' 
               OR nome ILIKE 'Ian Santos' 
            LIMIT 1
        """)
        old_user = cursor.fetchone()

        if not old_user:
            print("❌ Usuário de origem (Ian Santos) não encontrado no banco legado.")
            return

        print(f"   ✅ Origem encontrada: {old_user.get('nome')} (ID Antigo: {old_user['id']})")

        # 2. PREPARAR DADOS PARA O USUÁRIO DE DESTINO (IAN - DJANGO)
        
        # Lógica de Separação de Nome (Flask -> Django)
        nome_completo = old_user.get('nome', 'Ian Santos').strip()
        partes = nome_completo.split()
        first_name = partes[0]
        last_name = ' '.join(partes[1:]) if len(partes) > 1 else ''
        
        print(f"   ⚙️  Processando nome: '{first_name}' + '{last_name}'")

        # Gerar Tenant ID se necessário
        tenant_uuid = uuid.uuid4()
        
        # Aqui definimos explicitamente que o alvo é o username 'ian'
        target_username = 'ian'
        
        user_django, created = CustomUser.objects.get_or_create(
            username=target_username,
            defaults={
                'email': old_user.get('email', 'ian@exemplo.com'),
                'first_name': first_name,
                'last_name': last_name,
                'role': 'PROFESSOR_FREE', # Força papel de professor
                'tenant_type': 'INDIVIDUAL',
                'tenant_id': tenant_uuid,
            }
        )

        # Se o usuário já existia, garantimos que ele tenha um tenant_id
        if not created:
            print(f"   ℹ️  Usuário de destino '{target_username}' já existe. Atualizando dados se necessário.")
            if not user_django.tenant_id:
                user_django.tenant_id = tenant_uuid
                user_django.save()
            
            # Opcional: Atualizar nomes se estiverem vazios
            if not user_django.first_name:
                user_django.first_name = first_name
                user_django.last_name = last_name
                user_django.save()
                
            tenant_uuid = user_django.tenant_id
        else:
            user_django.set_password('123456') 
            user_django.save()
            print(f"   ✅ Usuário '{target_username}' criado.")

        # 3. MIGRAR TURMAS (USANDO O ID DO 'IAN SANTOS' MAS VINCULANDO AO 'IAN')
        print(f"\n>> Buscando turmas do ID antigo ({old_user['id']})...")
        
        try:
            cursor.execute("SELECT * FROM turmas WHERE id_user = %s", (old_user['id'],))
        except Exception:
            conn.rollback()
            print(f"   (Tentando coluna 'autor_id'...)")
            cursor.execute("SELECT * FROM turmas WHERE autor_id = %s", (old_user['id'],))
            
        old_turmas = cursor.fetchall()
        print(f"   {len(old_turmas)} turmas encontradas.")
        
        mapa_turmas = {} 

        for t in old_turmas:
            nome_turma = t['nome']
            
            # Cria a turma vinculada ao Tenant do usuário 'ian'
            nova_turma, t_created = Turma.objects.get_or_create(
                nome=nome_turma,
                tenant_id=tenant_uuid, 
                defaults={'ano_letivo': 2025}
            )
            mapa_turmas[t['id']] = nova_turma.id
            
            status = "Criada" if t_created else "Já existia"
            print(f"   + Turma '{nome_turma}': {status}")

        # 4. MIGRAR ALUNOS
        print(f"\n>> Migrando alunos...")
        if not mapa_turmas:
            print("   Nenhuma turma para migrar alunos.")
        else:
            ids_antigos = tuple(mapa_turmas.keys())
            
            if len(ids_antigos) == 1:
                query_alunos = f"SELECT * FROM alunos WHERE id_turma = '{ids_antigos[0]}'"
            else:
                query_alunos = f"SELECT * FROM alunos WHERE id_turma IN {ids_antigos}"
            
            cursor.execute(query_alunos)
            old_alunos = cursor.fetchall()
            print(f"   {len(old_alunos)} alunos encontrados na origem.")

            count_alunos = 0
            for a in old_alunos:
                uuid_turma_nova = mapa_turmas.get(a['id_turma'])
                
                # Verifica duplicidade
                if not Aluno.objects.filter(nome=a['nome'], turma_id=uuid_turma_nova).exists():
                    Aluno.objects.create(
                        nome=a['nome'],
                        tenant_id=tenant_uuid, # Vincula ao tenant do professor Ian
                        matricula_id=str(a.get('matricula', '')),
                        email=a.get('email_responsavel', ''),
                        telefone_responsavel=a.get('telefone_responsavel', ''),
                        turma_id=uuid_turma_nova
                    )
                    count_alunos += 1
            
            print(f"   ✅ {count_alunos} alunos novos importados para o professor Ian.")

    except Exception as e:
        print(f"❌ Erro na lógica: {repr(e)}")
        import traceback
        print(traceback.format_exc())
    finally:
        conn.close()
        print("\n✅ Processo finalizado.")

if __name__ == "__main__":
    migrar_ian()