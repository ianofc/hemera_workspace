import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'niocortex.settings')
django.setup()

with connection.cursor() as cursor:
    print("☢️  INICIANDO LIMPEZA PROFUNDA DO BANCO DE DADOS...")

    # 1. Lista de Apps do Projeto para limpar tabelas
    # Inclui nomes antigos e novos para garantir
    apps_to_clean = [
        'financial', 
        'pedagogical', 'pedagogico', 'lumenios_pedagogico',
        'secretariat', 
        'hr', 
        'crm_sales', 
        'plataforma', 'lumenios_plataforma',
        'core' 
    ]

    # 2. Drop dinâmico das tabelas desses apps
    for app in apps_to_clean:
        print(f"   Procurando tabelas de: {app}...")
        cursor.execute("""
            SELECT table_name FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name LIKE %s
        """, [app + '_%'])
        
        tables = cursor.fetchall()
        for (table_name,) in tables:
            print(f"   🗑️  Apagando tabela: {table_name}")
            cursor.execute(f'DROP TABLE IF EXISTS "{table_name}" CASCADE;')

    # 3. LIMPEZA TOTAL DAS MIGRAÇÕES
    # Apaga tudo para o Django achar que é uma instalação nova
    print("   🧹 Limpando histórico de migrações (django_migrations)...")
    try:
        cursor.execute("DELETE FROM django_migrations WHERE app IN %s;", (tuple(apps_to_clean),))
        # Se quiser ser radical e apagar TUDO (incluindo admin/auth):
        # cursor.execute("DELETE FROM django_migrations;") 
    except Exception as e:
        print(f"   ⚠️  Erro ao limpar migrações: {e}")

    print("\n✅ BANCO LIMPO! Agora o 'python manage.py migrate' deve funcionar.")