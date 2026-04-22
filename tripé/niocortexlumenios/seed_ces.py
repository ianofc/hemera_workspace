import os
import sys
import django
import uuid
import unicodedata
import random
import time
from datetime import date

# 1. Configurar Ambiente
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'niocortex.settings')
django.setup()

from django.db import close_old_connections, connection
from core.models import CustomUser, School
from lumenios.pedagogico.models import Turma, Aluno
from yourlife.social.models import Album, Friendship

# ==============================================================================
# DADOS MACIÇOS (CES)
# ==============================================================================
DATA_CES = {
    '1ª A ADM': ['ALISSON FEITOSA FARIAS', 'ANA CLAUDIA DE SOUZA ARAUJO', 'ANA VITORIA ROCHA TELES', 'CRISTAL', 'DAVID RAMOS DE SOUZSA', 'ELOÁ BARRETO FRAGA', 'ELOÁ SANTOS RIVAS', 'EMILLY VICTORIA SANTANA R. DOS SANTOS', 'FABRICIA', 'GABRIEL SEBASTIAN', 'GABRIELA TELES CIDREIRA', 'ISABEL', 'ISADORA', 'JHULLIE BRANDÃO TEIXEIRA', 'JOÃO MATEUS LIMA ALVES', 'JOÃO VITOR', 'KAROLAYNE VITORIA SOUZA NOVAES', 'KATHARINE LIMA FREITAS', 'LAISANI', 'LARA VICTORIA', 'LAURA', 'LINCESY ALVES DOS SANTOS', 'LUIZ HENRIQUE MIRANDA SENA', 'LUNA KELLY MEDEIROS QUEIROZ', 'MARIA EDUARDA BASTOS SOUZA', 'MARLEY', 'PAMELA DA SILVA MACEDO', 'PEDRO ARIEL DE SOUZA SANTOS', 'PEDRO GABRIEL DOS SANTOS', 'PEDRO HENRIQUE SOUZA MARTINS', 'PEDRO LUCAS MENDES SANTANA', 'RAFAELA', 'REBECA', 'REINALDO', 'VIVIAN ARAUJO ALVES', 'WENDEL ALCANTARA DE SOUZA'],
    '1ª A INTEGRAL': ['ELOISA NICOLE', 'ERIC JOSÉ LIMA MORAIS', 'GABRIEL GOMES ALMEIDA', 'GUSTAVO DE OLIVEIRA MATOS', 'ISABELA GOMES ARAUJO', 'ISABELA NASCIMENTO DOS SANTOS', 'KAIKE FABIO NEVES DE SOUSA', 'LETICIA SANTOS DE JESUS', 'LUIS FELIPE BENÍCIO', 'MANUEL SILVA MELO FILHO', 'MARIA ESTEFANE MORAES DA SILVA', 'THIAGO ALCANTARA VIEIRA'],
    '1ª B ADM': ['ALEX VITORIO BARROS DO NASCIMENTO', 'ANA CLARA BISPO SILVA', 'ANA CLARA DE SOUZA ANJOS', 'ANA JULIA DALTRON AMARAL', 'CAUÁ SOUZA SILVA', 'CLARA LUISA MIRANDA TEIXEIRA', 'GEOVANNA RIBEIRO MARTINS', 'IAN SANTOS SILVA', 'ISABELA GOMES DE SOUZA', 'ISABELLA XAVIER AMARAL', 'JOSYLEIA NASCIMENTO MENEZES', 'JULIA CATHARINE SOUZA TELES', 'JULIA SANTOS ARAÚJO', 'JULIA TELES RIBEIRO', 'KAROLAINE SILVA SOUZA', 'LARA VITORIA OLIVEIRA MENDES', 'LUKA THIERRY SÁ TELES DE ARAÚJO', 'MARIA CLARA ALVES FERREIRA', 'MARIA EDUARDA BISPO DOS SANTOS', 'MARIANA TEIXEIRA DE SOUZA', 'MARIANE DOS ANJOS RIBEIRO', 'NICOLLY BRITO DE SOUZA', 'PEDRO CORDEIRO SANTOS', 'PEDRO HENRIQUE SOUZA', 'PEDRO KAUAN SOUZA OLIVEIRA', 'THAUANY RODRIGUES DE SOUZA', 'TULIO RIBEIRO DE AZEVEDO ROCHA', 'VIVIANNY MORAES PACHECO'],
    '1ª B INTEGRAL': ['DHEIVERSON JESUS DOS ANJOS', 'FRANCISCA STEFANY SANTOS ARAUJO', 'GABRIEL ATHAYDE ARAUJO SILVA', 'GABRIEL VINICIUS MARIANO SANTIAGO', 'GABRIELLY SOUZA SANTOS', 'INÁCIO SILVA OLIVEIRA', 'JHONATA FRANÇA DA SILVA PONTES', 'LETICIA SANTOS DE JESUS', 'MARIA CLARA DE OLIVEIRA', 'MARIA EDUARDA PONTES MUNIZ DA SILVA', 'MARIANE SILVA SOUZA', 'PEDRO CAUAN ALVES LIMA', 'PEDRO HENRIQUE SANTOS MACHADO'],
    '1ª D ADM': ['ADSON ARAUJO ALVES', 'ANA CLARA ARAUJO BARROS', 'ANNA VITORIA FIDELES DE SOUZA', 'ARYEL MATHEUS OLIVEIRA LOPES', 'BISMARK ANJOS DOS SANTOS', 'CARLOS EDUARDO JESUS DA SILVA', 'DAFINE SOFIA RODRIGUES DE SOUZA', 'DEIVISON RUFINO DE SOUZA', 'ELLEN KAILANE ARAUJO DOS SANTOS', 'EMILLY OLIVEIRA BRANDÃO', 'ENZO GABRIEL MENDES SANTANA', 'ERIC OLIVEIRA GUIMARÃES', 'ERICK RIAN DE OLIVEIRA FERREIRA', 'FRANCINY ANJOS VIEIRA', 'IAGO MATHEUS BARBOSA SILVA', 'ISABELLA JESUS NOVAIS DA SILVA', 'JOANA RAISSA SILVA DE ARAÚJO', 'JULIA DE SOUZA SANTOS', 'KELLY NAIANE DE NOVAIS ANJOS', 'LARA LORRANE ROCHA FERREIRA', 'LUNNA RIHANNA ALVES SANTOS', 'MAINARA DE SOUZA OLIVEIRA', 'MARINA DA SILVA FERREIRA', 'MATHEUS SOUZA DOS SANTOS', 'MIRELE SILVA BRANDÃO', 'NATALIA MENDES', 'NATIELE MENDES DE JESUS', 'RAQUEL RODRIGUES ALVES', 'SAMILLY SOUZA LEITE', 'SHEILA SILVIA DE OLIVEIRA', 'VITÓRIA EDUARDA BARROS ALVES', 'WELLINGTON PAULO SANTOS BARRETO'],
    '2ª 3ª E FLUXO': ['ANGELA DE SOUZA SANTOS', 'BRENO MENDES DE SOUZA', 'CAMILA NOVAES DOS SANTOS', 'DANIELLY DOS ANJOS SOUZA', 'EDUARDO DE SOUZA SANTOS', 'ELOISA ALVES', 'EMERSON GABRIEL', 'FRANCIELE ALVES', 'FREDSON DOURADO MEDEIROS', 'GUILHERME S. PEREIRA', 'ICARO FELIPE DA SILVA SOUZA', 'ISIS CATARINE S. C.', 'JOAO PEDRO NOVAIS VENTURA', 'LAZARO SOUZA LOPES', 'MARIA LUISA SOUZA SILVA', 'MICAEL CAMBUI DE SOUZA', 'NILANE AMORIN CIRINO', 'OTAVIO DE SOUZA', 'PEDRO YAERLEM MOREIRA BRANDAO', 'RAI SANTOS', 'RICHARLES DOS SANTOS SOUZA', 'RUAN ALVES SANTANA', 'VITORIA', 'ZILMARIA DOS S. T.'],
    '2ª D': ['ACASSIO DA SILVA MARTINS', 'ANDRYA DANIELLY ARAUJO DOS SANTOS', 'CLEILSON MEDEIROS DE SOUZA', 'ELLEN ENEDINA TELES FERNANDES', 'ELVIS ALENCAR DOS SANTOS SILVA', 'EZIELTON CONCEICAO MENDES', 'GABRIELA MARTINS SOUZA', 'GEAZI TEIXEIRA GOMES', 'GUILHERME BRAGA DE SOUZA', 'GUILHERME SOUZA DA SILVA', 'IAGO OLIVEIRA MENDES', 'ISANDRA DOS SANTOS DE SOUZA', 'JESSICA AMORIM DOS SANTOS', 'JOSE NILTON NASCIMENTO PINTO', 'JOVANA ALVES DOS SANTOS', 'LEANDRO SILVA DE SOUZA', 'LEILTON DA SILVA MENDES', 'LUIZ EDUARDO SOUZA VIEIRA', 'LUNA DA SILVA ARAUJO', 'LUNA MARIA PEREIRA DE SOUZA', 'MARIA LUIZA FARIAS DE PAULA', 'NAELE DE SOUZA', 'NATIELE OLIVEIRA SOUZA', 'PEDRO HENRIQUE FERREIRA GOMES', 'RAFAELLA DE SOUZA SANTOS', 'RAILA SOUZA AMORIM', 'RAY JOSÉ DA CONCEIÇÃO SANTOS', 'RICKELME SOUZA SILVA', 'RUBENS ALVES FERREIRA', 'SOPHIA ALCANTARA DE SOUZA BRANDAO', 'TAINÁ MENDES DE SOUZA', 'TATIANE MARTINS ARAUJO', 'UALISSON RUAN ARAUJO SOUZA', 'VANESSA SOUZA MENDES'],
    '2ª INTEGRAL': ['Fabrício Reis de Oliveira', 'Gutierry Oliveira Souza', 'Igor Nunes da Silva', 'Ismael Gomes Batista', 'Joaquim Araujo de Carvalho', 'João Miguel Santos Araujo', 'Karina Almeida Carvalho', 'Lucas Manoel Nunes', 'Maria Eduarda Marques Araujo', 'Rafael Silva Teixeira', 'Raí Pereira da Rocha', 'Vitor Gabriel Santos Silva', 'Vitória Rosa de Oliveira'],
    '3ªC ELETIVA': ['ALAN NOVAES DA SILVA', 'AMANDA GREGORIO ALVES', 'ANA JULIA DORADO DE JESUS', 'ANALY JESUS DOS SANTOS', 'ARYEL CAIQUE SANTOS MENDES', 'BENJAMIM SANTANA RODRIGUES', 'BÁRBARA PEREIRA DE OLIVEIRA', 'CAIO GOIS SOUZA', 'CARLOS DANIEL DINIZ OLIVEIRA', 'DAVISON OLIVEIRA SILVA', 'EDINEI ARAUJO DE SOUZA', 'ELOISE SILVA FERREIRA', 'ELVITON JUNIOR PEREIRA DOS ANJOS', 'FLAVIO PINTO ALVES', 'GISELE SANTOS ANTUNES', 'GLEICE LIMA MENDES', 'GUILHERME ARAUJO DE NOVAES', 'GUILHERME PINA DE OLIVEIRA', 'IASMIM SILVA OLIVEIRA', 'INGRED DREGER DE JESUS', 'ITALO MENDES SANTOS', 'JAIELE MARQUES DE OLIVEIRA', 'JULIANE ANJOS MENDES', 'KEILLA OLIVIERA DE SOUZA', 'LAIANE SOUZA SANTOS', 'LEILTON ALVES DA SILVA', 'LILIAN SIMONI MORAES ALVES', 'LUCAS WENDEL MATOS DE OLIVEIRA', 'LUIS DANIEL DIAS BRANDÃO', 'MARCOS ANTONIO SOUZA DE JESUS', 'MICHEL SANTOS OLIVEIRA', 'NATALÍ BARBOSA DOS ANJOS', 'RENATO DA SILVA FRANÇA', 'STEFANE OLIVEIRA DOS ANJOS', 'THAINÁ SILVA MELO', 'THAUÃ VICTOR DE OLIVEIRA SANTOS', 'UANDERSON DOS REIS SILVA', 'WEVERTON GASPAR DE SOUZA'],
}

# ==============================================================================
# UTILITÁRIOS
# ==============================================================================
def gerar_cpf_fake():
    return f"{random.randint(100,999)}.{random.randint(100,999)}.{random.randint(100,999)}-{random.randint(10,99)}"

def gerar_nascimento(idade_min, idade_max):
    ano = date.today().year - random.randint(idade_min, idade_max)
    return date(ano, random.randint(1, 12), random.randint(1, 28))

def normalizar_nome(nome):
    return "".join(c for c in unicodedata.normalize('NFKD', nome) if not unicodedata.combining(c)).lower()

def gerar_username_unico(nome_completo):
    parts = normalizar_nome(nome_completo).split()
    base = f"{parts[0]}.{parts[-1]}" if len(parts) >= 2 else parts[0]
    username = base
    counter = 1
    # Verifica no banco se já existe para evitar colisão
    while CustomUser.objects.filter(username=username).exists():
        username = f"{base}{counter}"
        counter += 1
    return username

def gerar_matricula_oficial(escola_id, cargo_id, seq, cpf_fake):
    """AAAA + SM + MM + EE + CC + SEQ + CPF"""
    hoje = date.today()
    semestre = "01" if hoje.month <= 6 else "02"
    return f"{hoje.year}{semestre}{hoje.month:02d}{escola_id:02d}{cargo_id:02d}{seq:04d}{cpf_fake[-4:]}"

def criar_amizade(user1, user2):
    if user1 and user2 and user1 != user2:
        try:
            Friendship.objects.get_or_create(user_from=user1, user_to=user2, defaults={'status': 'ACCEPTED'})
            Friendship.objects.get_or_create(user_from=user2, user_to=user1, defaults={'status': 'ACCEPTED'})
        except Exception:
            pass # Ignora erros de duplicidade

# ==============================================================================
# ORQUESTRADOR
# ==============================================================================
def run():
    print("--- 📡 INICIANDO SCRIPT BLINDADO (CONEXÃO SEGURA) ---")

    # Garante conexão limpa no início
    close_old_connections()

    # 1. ESCOLA BASE
    escola, _ = School.objects.get_or_create(nome='Colegio Estadual de Seabra - CES', defaults={'tipo': 'SaaS_Head'})
    if not escola.tenant_id:
        escola.tenant_id = uuid.uuid4(); escola.save()
    tenant_uuid = escola.tenant_id
    ESCOLA_ID = 1

    # ------------------------------------------------------------------
    # 2. IAN SANTOS (ADMIN)
    # ------------------------------------------------------------------
    print("⚙️  Verificando Admin...")
    cpf_ian = "000.000.000-01"
    mat_ian = gerar_matricula_oficial(ESCOLA_ID, 99, 1, cpf_ian)
    
    ian, _ = CustomUser.objects.update_or_create(
        username='iansantos',
        defaults={
            'email': 'ianworktech@gmail.com', 'first_name': 'Ian', 'last_name': 'Santos',
            'role': 'ADMIN', 'is_staff': True, 'is_superuser': True, 
            'is_professor': True, 'is_gestor': True, 'is_premium': True,
            'matricula': mat_ian, 'cpf': cpf_ian,
            'data_nascimento': date(1993, 4, 29),
            'cidade_natal': 'Seabra', 'cidade_atual': 'Seabra',
            'school': escola, 'tenant_id': tenant_uuid
        }
    )
    ian.set_password('134679')
    ian.save()
    print("✅ Ian Santos ok.")

    # ------------------------------------------------------------------
    # 3. FAMÍLIA ENZO (Update Seguro)
    # ------------------------------------------------------------------
    print("\n🏠 Verificando Família...")
    test_users = [
        {'user': 'ana_uni', 'first': 'Ana', 'last': 'Universitária', 'role': 'ALUNO', 'nivel': 'superior', 'idade': 22, 'inst': 'UNEB', 'rel': 'NAMORANDO'},
        {'user': 'bebe_enzo', 'first': 'Enzo', 'last': 'Gabriel', 'role': 'ALUNO', 'nivel': 'infantil', 'idade': 2, 'inst': 'Creche', 'rel': 'SOLTEIRO', 'bio': 'Gerido por Mamãe e Papai.'},
        {'user': 'pai_enzo', 'first': 'Carlos', 'last': 'Silva', 'role': 'RESPONSAVEL', 'nivel': 'medio', 'idade': 30, 'inst': 'UFBA', 'rel': 'CASADO'},
        {'user': 'mae_enzo', 'first': 'Fernanda', 'last': 'Souza', 'role': 'RESPONSAVEL', 'nivel': 'medio', 'idade': 28, 'inst': 'UFBA', 'rel': 'CASADO'}
    ]

    seq_test = 100
    for t in test_users:
        seq_test += 1
        mat = gerar_matricula_oficial(ESCOLA_ID, 0, seq_test, gerar_cpf_fake())
        
        # Check first to avoid re-generating unnecessary updates
        u = CustomUser.objects.filter(username=t['user']).first()
        if not u:
            u = CustomUser(username=t['user'])
        
        # Update Attributes
        u.first_name = t['first']
        u.last_name = t['last']
        u.email = f"{t['user']}@niocortex.com"
        u.role = t['role']
        if not u.matricula: u.matricula = mat
        if not u.cpf: u.cpf = gerar_cpf_fake()
        u.data_nascimento = gerar_nascimento(t['idade'], t['idade'])
        u.bio = t.get('bio', '')
        u.instituicao_ensino = t['inst']
        u.status_relacionamento = t['rel']
        u.cidade_atual = 'Seabra'
        u.school = escola
        u.tenant_id = tenant_uuid
        u.is_aluno = (t['role'] == 'ALUNO')
        u.nivel_ensino = t['nivel']
        
        u.set_password('123456')
        u.save() # Signal deve criar Aluno automaticamente se for ALUNO
        
        # Garante Álbum
        if not u.albuns.exists():
            Album.objects.create(usuario=u, titulo="Fotos de Perfil", privacidade='PUBLIC')

    # Conexões
    try:
        pai = CustomUser.objects.get(username='pai_enzo')
        mae = CustomUser.objects.get(username='mae_enzo')
        enzo = CustomUser.objects.get(username='bebe_enzo')
        criar_amizade(pai, mae)
        criar_amizade(pai, enzo)
        criar_amizade(mae, enzo)
    except: pass
    print("✅ Família ok.")

    # ------------------------------------------------------------------
    # 4. ALUNOS CES (COM PROTEÇÃO DE CONEXÃO)
    # ------------------------------------------------------------------
    print("\n📚 Processando Alunos do CES...")
    
    # Fecha conexão antes do loop pesado para evitar timeout
    close_old_connections()
    
    seq_ces = 200
    total_processed = 0

    for nome_turma, alunos in DATA_CES.items():
        # Reabre conexão a cada turma para garantir estabilidade
        close_old_connections()
        
        turma, _ = Turma.objects.get_or_create(
            nome=nome_turma,
            defaults={'ano_letivo': 2026, 'periodo': 'Integral' if 'INTEGRAL' in nome_turma else 'Matutino'}
        )
        print(f"   📂 {nome_turma}...", end=" ", flush=True)
        
        for nome_completo in alunos:
            seq_ces += 1
            parts = nome_completo.strip().title().split()
            first = parts[0]
            last = " ".join(parts[1:]) if len(parts) > 1 else ""
            
            # Tenta encontrar user (Idempotência)
            user = CustomUser.objects.filter(first_name__iexact=first, last_name__iexact=last).first()
            
            if not user:
                username = gerar_username_unico(nome_completo)
                user = CustomUser(username=username)
                user.first_name = first
                user.last_name = last
            
            # Garante dados
            if not user.matricula:
                user.matricula = gerar_matricula_oficial(ESCOLA_ID, 0, seq_ces, gerar_cpf_fake())
            if not user.cpf: user.cpf = gerar_cpf_fake()
            
            user.role = 'ALUNO'
            user.is_aluno = True
            user.school = escola
            user.tenant_id = tenant_uuid
            user.turma = turma
            user.email = f"{user.username}@ces.edu.br"
            user.cidade_atual = "Seabra"
            user.set_password('123456')
            
            try:
                user.save() # Signal dispara criação do Aluno aqui
                
                # Perfil Pedagógico - Reforço/Update (Com nome de campo CORRIGIDO)
                Aluno.objects.update_or_create(
                    usuario=user,
                    defaults={
                        'turma': turma, 
                        'matricula': user.matricula  # <-- CORRIGIDO PARA 'matricula'
                    }
                )
                
                # Álbuns
                if not user.albuns.exists():
                    Album.objects.create(usuario=user, titulo="Fotos de Perfil", privacidade='PUBLIC')
                    Album.objects.create(usuario=user, titulo="Linha do Tempo", privacidade='PUBLIC')
                    
                total_processed += 1
            except Exception as e:
                # Se der erro em um aluno, loga mas continua
                print(f"[!] Erro em {first}: {e}")

        print("OK") # Fim da turma

    print(f"\n✅ PROCESSO FINALIZADO! {total_processed} alunos processados.")

if __name__ == "__main__":
    run()