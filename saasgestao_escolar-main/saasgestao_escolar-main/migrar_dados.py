# Em: ianofc/gestao_alunos/gestao_alunos-ff68344496a489e0f71c2e3b4ba7d354b182337a/migrar_dados.py

import sqlite3
import os
from datetime import date, datetime

# Importa a app Flask e os NOVOS modelos
from app import app, db
from models import User, Turma, Aluno, Atividade, Presenca, PlanoDeAula, Lembrete, Horario, BlocoAula

# Nomes dos ficheiros
# O ficheiro .db com os seus dados (que você renomeou)
SOURCE_DB_PATH = os.path.join(os.path.dirname(__file__), 'backup_completo.db')
# O novo ficheiro .db que será criado
DEST_DB_PATH = os.path.join(os.path.dirname(__file__), 'gestao_alunos.db')

# Converte dados do SQLite (tuplos) para dicionários para ser mais fácil de ler
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def run_migration():
    print(f"Iniciando migração de '{SOURCE_DB_PATH}' para '{DEST_DB_PATH}'...")

    # Verifica se o backup existe
    if not os.path.exists(SOURCE_DB_PATH):
        print(f"ERRO: Ficheiro de backup '{SOURCE_DB_PATH}' não encontrado!")
        print("Por favor, renomeie 'gestao_alunos.db' (o antigo, com dados) para 'backup_completo.db' e tente novamente.")
        return

    # 1. Apaga a base de dados de destino (nova) se ela já existir, para começar do zero
    if os.path.exists(DEST_DB_PATH):
        os.remove(DEST_DB_PATH)
        print(f"Base de dados de destino '{DEST_DB_PATH}' apagada.")

    # 2. Conecta à base de dados de ORIGEM (o seu backup)
    source_conn = sqlite3.connect(SOURCE_DB_PATH)
    source_conn.row_factory = dict_factory
    source_cursor = source_conn.cursor()

    # 3. Cria a nova base de dados de DESTINO (com o novo schema)
    # Usamos o contexto da app para garantir que o SQLAlchemy funciona
    with app.app_context():
        # ATENÇÃO: Se você usou o flask db init, o SQLAlchemy não cria a tabela alembic_version.
        # db.create_all() é a forma correta de criar o novo esquema.
        db.create_all()
        print(f"Nova base de dados '{DEST_DB_PATH}' criada com o novo schema (incluindo ACERTOS e PERFIL).")

        # Mapas para guardar os IDs antigos -> novos
        user_map = {}
        turma_map = {}
        aluno_map = {}
        atividade_map = {}

        # --- ETAPA 1: Migrar Utilizadores (Users) ---
        print("Migrando Utilizadores...")
        source_cursor.execute("SELECT * FROM users")
        old_users = source_cursor.fetchall()
        
        new_user = None # Assume que só há 1 utilizador
        for old_user in old_users:
            new_user = User(
                username=old_user['username'],
                password_hash=old_user['password_hash'],
                
                # CORREÇÃO: Adiciona os novos campos, usando .get() para compatibilidade com backups antigos
                email_contato=old_user.get('email_contato'),
                telefone=old_user.get('telefone'),
                foto_perfil_path=old_user.get('foto_perfil_path'),
                is_professor=old_user.get('is_professor', True), # Assume True se não existir
                is_admin=old_user.get('is_admin', False)         # Assume False se não existir
            )
            db.session.add(new_user)
            db.session.commit() # Commit para obter o ID
            user_map[old_user['id']] = new_user.id
            print(f"  > Utilizador '{new_user.username}' migrado (ID antigo: {old_user['id']} -> ID novo: {new_user.id})")

            # Cria o Horário e Blocos padrão para este utilizador (necessário pelo novo schema)
            novo_horario = Horario(nome=f"Horário de {new_user.username}", autor=new_user)
            db.session.add(novo_horario)
            horarios_texto_padrao = ["13:10", "14:00", "14:50", "16:00", "16:50"]
            for dia in range(5):
                for pos in range(1, 6):
                    bloco = BlocoAula(horario=novo_horario, dia_semana=dia, posicao_aula=pos, texto_horario=horarios_texto_padrao[pos-1])
                    db.session.add(bloco)
            print(f"  > Horário padrão criado para '{new_user.username}'.")
        
        if new_user is None:
             print("AVISO: Nenhum utilizador encontrado no backup. As turmas não terão um 'autor'.")


        # --- ETAPA 2: Migrar Turmas ---
        print("Migrando Turmas...")
        source_cursor.execute("SELECT * FROM turmas")
        old_turmas = source_cursor.fetchall()
        
        for old_turma in old_turmas:
            # ASSUME que todas as turmas pertencem ao PRIMEIRO utilizador migrado
            if new_user:
                new_turma = Turma(
                    nome=old_turma['nome'],
                    descricao=old_turma['descricao'],
                    turno=old_turma['turno'],
                    autor=new_user # Associa ao utilizador
                )
                db.session.add(new_turma)
                db.session.commit()
                turma_map[old_turma['id']] = new_turma.id
                print(f"  > Turma '{new_turma.nome}' migrada.")
            else:
                print(f"  > AVISO: Turma '{old_turma['nome']}' ignorada (nenhum utilizador para associar).")

        # --- ETAPA 3: Migrar Alunos ---
        print("Migrando Alunos...")
        source_cursor.execute("SELECT * FROM alunos")
        old_alunos = source_cursor.fetchall()

        for old_aluno in old_alunos:
            # Converte a data de string para objeto Date
            data_cadastro_obj = None
            if old_aluno['data_cadastro']:
                try:
                    data_cadastro_obj = date.fromisoformat(old_aluno['data_cadastro'])
                except:
                    pass # Deixa como None se o formato for inválido
            
            # Encontra o ID da nova turma
            new_turma_id = turma_map.get(old_aluno['id_turma'])
            
            new_aluno = Aluno(
                nome=old_aluno['nome'],
                matricula=old_aluno['matricula'],
                data_cadastro=data_cadastro_obj,
                id_turma=new_turma_id # Usa o NOVO ID da turma
            )
            db.session.add(new_aluno)
            db.session.commit()
            aluno_map[old_aluno['id']] = new_aluno.id
        print(f"  > {len(old_alunos)} alunos migrados.")

        # --- ETAPA 4: Migrar Atividades ---
        print("Migrando Atividades...")
        source_cursor.execute("SELECT * FROM atividades")
        old_atividades = source_cursor.fetchall()

        for old_atividade in old_atividades:
            data_obj = None
            if old_atividade['data']:
                try:
                    data_obj = date.fromisoformat(old_atividade['data'])
                except:
                    pass
            
            new_turma_id = turma_map.get(old_atividade['id_turma'])

            new_atividade = Atividade(
                id_turma=new_turma_id, # Usa o NOVO ID da turma
                titulo=old_atividade['titulo'],
                data=data_obj,
                peso=old_atividade['peso'],
                descricao=old_atividade['descricao'],
                tipo=old_atividade.get('tipo', 'Atividade'), # Adicionado tipo
                nome_arquivo_anexo=old_atividade.get('nome_arquivo_anexo'),
                path_arquivo_anexo=old_atividade.get('path_arquivo_anexo')
            )
            db.session.add(new_atividade)
            db.session.commit()
            atividade_map[old_atividade['id']] = new_atividade.id
        print(f"  > {len(old_atividades)} atividades migrados.")

        # --- ETAPA 5: Migrar Planos de Aula ---
        print("Migrando Planos de Aula...")
        source_cursor.execute("SELECT * FROM planos_de_aula")
        old_planos = source_cursor.fetchall()

        for old_plano in old_planos:
            data_prevista_obj = None
            if old_plano['data_prevista']:
                try:
                    data_prevista_obj = date.fromisoformat(old_plano['data_prevista'])
                except:
                    pass
            
            new_turma_id = turma_map.get(old_plano['id_turma'])
            new_atividade_gerada_id = atividade_map.get(old_plano['id_atividade_gerada'])

            if new_turma_id and data_prevista_obj: # Campos obrigatórios
                new_plano = PlanoDeAula(
                    id_turma=new_turma_id,
                    data_prevista=data_prevista_obj,
                    titulo=old_plano['titulo'],
                    conteudo=old_plano['conteudo'],
                    habilidades_bncc=old_plano['habilidades_bncc'],
                    objetivos=old_plano['objetivos'],
                    duracao=old_plano['duracao'],
                    recursos=old_plano['recursos'],
                    metodologia=old_plano['metodologia'],
                    avaliacao=old_plano['avaliacao'],
                    referencias=old_plano['referencias'],
                    status=old_plano['status'],
                    id_atividade_gerada=new_atividade_gerada_id
                )
                db.session.add(new_plano)
        db.session.commit()
        print(f"  > {len(old_planos)} planos de aula migrados.")

        # --- ETAPA 6: Migrar Lembretes ---
        print("Migrando Lembretes...")
        source_cursor.execute("SELECT * FROM lembretes")
        old_lembretes = source_cursor.fetchall()
        
        for old_lembrete in old_lembretes:
            new_user_id = user_map.get(old_lembrete['id_user'])
            if new_user_id: # Só migra se o utilizador existir
                
                # Tenta converter data_criacao para datetime se for string (SQLite padrão)
                data_criacao_obj = old_lembrete['data_criacao']
                if isinstance(data_criacao_obj, str):
                    try:
                        data_criacao_obj = datetime.fromisoformat(data_criacao_obj)
                    except:
                        data_criacao_obj = datetime.utcnow() # Usa a data atual como fallback
                        
                new_lembrete = Lembrete(
                    texto=old_lembrete['texto'],
                    data_criacao=data_criacao_obj,
                    status=old_lembrete['status'],
                    id_user=new_user_id
                )
                db.session.add(new_lembrete)
        db.session.commit()
        print(f"  > {len(old_lembretes)} lembretes migrados.")

        # --- ETAPA 7: Migrar Presenças (Notas/Faltas) ---
        print("Migrando Presenças/Notas...")
        source_cursor.execute("SELECT * FROM presencas")
        old_presencas = source_cursor.fetchall()

        for old_presenca in old_presencas:
            new_aluno_id = aluno_map.get(old_presenca['id_aluno'])
            new_atividade_id = atividade_map.get(old_presenca['id_atividade'])

            # Só migra se o aluno e a atividade ainda existirem
            if new_aluno_id and new_atividade_id:
                new_presenca = Presenca(
                    id_aluno=new_aluno_id,
                    id_atividade=new_atividade_id,
                    status=old_presenca['status'],
                    participacao=old_presenca['participacao'],
                    nota=old_presenca['nota'],
                    
                    # CORREÇÃO: Adiciona a coluna 'acertos', inicializada como None
                    acertos=old_presenca.get('acertos'),
                    
                    desempenho=old_presenca['desempenho'],
                    situacao=old_presenca['situacao'],
                    observacoes=old_presenca['observacoes']
                )
                db.session.add(new_presenca)
        db.session.commit()
        print(f"  > {len(old_presencas)} registos de presença/nota migrados.")


        print("\n✅ MIGRAÇÃO CONCLUÍDA COM SUCESSO!")
        print("O novo banco de dados (gestao_alunos.db) está criado com o esquema mais recente e os dados antigos.")
        print("Pode agora executar a aplicação principal com 'python run.py'")

    # Fecha a conexão com o backup
    source_conn.close()

# Executa a função
if __name__ == "__main__":
    run_migration()