import os
import django
from django.db import connection

# Configura o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'niocortex.settings')
django.setup()

def nuke_database():
    print("☢️  INICIANDO LIMPEZA TOTAL DO BANCO DE DADOS (PostgreSQL)...")
    
    with connection.cursor() as cursor:
        # 1. Desconecta a verificação de integridade temporariamente (opcional, mas ajuda)
        # Em Postgres, DROP CASCADE resolve a maioria das constraints.
        
        # 2. Busca TODAS as tabelas do esquema 'public'
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        tables = cursor.fetchall()
        
        if not tables:
            print("   ✅ O banco já está vazio.")
            return

        print(f"   ⚠️  Encontradas {len(tables)} tabelas. Apagando tudo...")

        # 3. Gera e executa o DROP para cada tabela com CASCADE
        for (table_name,) in tables:
            print(f"      🗑️  Apagando: {table_name}")
            # CASCADE garante que tabelas dependentes (como as do admin/auth) também vão embora
            cursor.execute(f'DROP TABLE IF EXISTS "{table_name}" CASCADE;')

    print("\n✅ BANCO ZERADO COM SUCESSO!")
    print("   Agora o Django achará que é uma instalação nova.")
    print("   Execute: python manage.py migrate")

if __name__ == "__main__":
    # Confirmação de segurança
    confirm = input("⚠️  ATENÇÃO: ISSO VAI APAGAR TODOS OS DADOS DO BANCO. TEM CERTEZA? (s/n): ")
    if confirm.lower() == 's':
        try:
            nuke_database()
        except Exception as e:
            print(f"❌ Erro ao limpar o banco: {e}")
            print("   Dica: Se houver erro de permissão, você precisará usar o PGAdmin ou SQL direto.")
    else:
        print("   Operação cancelada.")