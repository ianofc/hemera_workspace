import os
import sys
import django
import uuid
import unicodedata
import random
from datetime import date

# 1. Configurar Ambiente
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'niocortex.settings')
django.setup()

from core.models import CustomUser, School
from lumenios.pedagogico.models import Turma, Aluno
from yourlife.social.models import Album

# ==============================================================================
# LÓGICA DE MATRÍCULA ROBUSTA
# ==============================================================================
def gerar_matricula_padrao(escola_id_seq, cargo_code, sequencial_db, cpf_final):
    """
    Gera matrícula no formato: AAAA + SM + MM + EE + CC + SEQ + CPF
    Ex: 2026 01 01 01 00 0001 4538
    """
    hoje = date.today()
    ano = hoje.year
    semestre = "01" if hoje.month <= 6 else "02"
    mes = f"{hoje.month:02d}"
    
    # EE: ID da Escola (01 a 99)
    escola_str = f"{escola_id_seq:02d}"
    
    # CC: Código do Cargo
    # 00: ALUNO, 10: PROF, 20: COORD, 30: DIR, 40: SEC, 50: RH, 60: FIN
    cargo_str = f"{cargo_code:02d}"
    
    # SEQ: Sequencial do cadastro (0001 a 9999)
    seq_str = f"{sequencial_db:04d}"
    
    # CPF: 4 últimos dígitos
    cpf_str = cpf_final[-4:] if cpf_final else f"{random.randint(1000,9999)}"
    
    return f"{ano}{semestre}{mes}{escola_str}{cargo_str}{seq_str}{cpf_str}"

# ==============================================================================
# DADOS (Mantidos da extração anterior)
# ==============================================================================
DATA_EXTRACTED = {
    '1ª A ADM': [
        'ALISSON FEITOSA FARIAS', 'ANA CLAUDIA DE SOUZA ARAUJO', 'ANA VITORIA ROCHA TELES', 'CRISTAL', 
        'DAVID RAMOS DE SOUZSA', 'ELOÁ BARRETO FRAGA', 'ELOÁ SANTOS RIVAS', 'EMILLY VICTORIA SANTANA R. DOS SANTOS', 
        'FABRICIA', 'GABRIEL SEBASTIAN', 'GABRIELA TELES CIDREIRA', 'ISABEL', 'ISADORA', 'JHULLIE BRANDÃO TEIXEIRA', 
        'JOÃO MATEUS LIMA ALVES', 'JOÃO VITOR', 'KAROLAYNE VITORIA SOUZA NOVAES', 'KATHARINE LIMA FREITAS', 
        'LAISANI', 'LARA VICTORIA', 'LAURA', 'LINCESY ALVES DOS SANTOS', 'LUIZ HENRIQUE MIRANDA SENA', 
        'LUNA KELLY MEDEIROS QUEIROZ', 'MARIA EDUARDA BASTOS SOUZA', 'MARLEY', 'PAMELA DA SILVA MACEDO', 
        'PEDRO ARIEL DE SOUZA SANTOS', 'PEDRO GABRIEL DOS SANTOS', 'PEDRO HENRIQUE SOUZA MARTINS', 
        'PEDRO LUCAS MENDES SANTANA', 'RAFAELA', 'REBECA', 'REINALDO', 'VIVIAN ARAUJO ALVES', 'WENDEL ALCANTARA DE SOUZA'
    ],
    '1ª A INTEGRAL': [
        'ELOISA NICOLE', 'ERIC JOSÉ LIMA MORAIS', 'GABRIEL GOMES ALMEIDA', 'GUSTAVO DE OLIVEIRA MATOS', 
        'ISABELA GOMES ARAUJO', 'ISABELA NASCIMENTO DOS SANTOS', 'KAIKE FABIO NEVES DE SOUSA', 'LETICIA SANTOS DE JESUS', 
        'LUIS FELIPE BENÍCIO', 'MANUEL SILVA MELO FILHO', 'MARIA ESTEFANE MORAES DA SILVA', 'THIAGO ALCANTARA VIEIRA'
    ],
    '1ª B ADM': [
        'ALEX VITORIO BARROS DO NASCIMENTO', 'ANA CLARA BISPO SILVA', 'ANA CLARA DE SOUZA ANJOS', 'ANA JULIA DALTRON AMARAL', 
        'CAUÁ SOUZA SILVA', 'CLARA LUISA MIRANDA TEIXEIRA', 'GEOVANNA RIBEIRO MARTINS', 'IAN SANTOS SILVA', 
        'ISABELA GOMES DE SOUZA', 'ISABELLA XAVIER AMARAL', 'JOSYLEIA NASCIMENTO MENEZES', 'JULIA CATHARINE SOUZA TELES', 
        'JULIA SANTOS ARAÚJO', 'JULIA TELES RIBEIRO', 'KAROLAINE SILVA SOUZA', 'LARA VITORIA OLIVEIRA MENDES', 
        'LUKA THIERRY SÁ TELES DE ARAÚJO', 'MARIA CLARA ALVES FERREIRA', 'MARIA EDUARDA BISPO DOS SANTOS', 
        'MARIANA TEIXEIRA DE SOUZA', 'MARIANE DOS ANJOS RIBEIRO', 'NICOLLY BRITO DE SOUZA', 'PEDRO CORDEIRO SANTOS', 
        'PEDRO HENRIQUE SOUZA', 'PEDRO KAUAN SOUZA OLIVEIRA', 'THAUANY RODRIGUES DE SOUZA', 'TULIO RIBEIRO DE AZEVEDO ROCHA', 
        'VIVIANNY MORAES PACHECO'
    ],
    '1ª B INTEGRAL': [
        'DHEIVERSON JESUS DOS ANJOS', 'FRANCISCA STEFANY SANTOS ARAUJO', 'GABRIEL ATHAYDE ARAUJO SILVA', 
        'GABRIEL VINICIUS MARIANO SANTIAGO', 'GABRIELLY SOUZA SANTOS', 'INÁCIO SILVA OLIVEIRA', 
        'JHONATA FRANÇA DA SILVA PONTES', 'LETICIA SANTOS DE JESUS', 'MARIA CLARA DE OLIVEIRA', 
        'MARIA EDUARDA PONTES MUNIZ DA SILVA', 'MARIANE SILVA SOUZA', 'PEDRO CAUAN ALVES LIMA', 'PEDRO HENRIQUE SANTOS MACHADO'
    ],
    '1ª D ADM': [
        'ADSON ARAUJO ALVES', 'ANA CLARA ARAUJO BARROS', 'ANNA VITORIA FIDELES DE SOUZA', 'ARYEL MATHEUS OLIVEIRA LOPES', 
        'BISMARK ANJOS DOS SANTOS', 'CARLOS EDUARDO JESUS DA SILVA', 'DAFINE SOFIA RODRIGUES DE SOUZA', 'DEIVISON RUFINO DE SOUZA', 
        'ELLEN KAILANE ARAUJO DOS SANTOS', 'EMILLY OLIVEIRA BRANDÃO', 'ENZO GABRIEL MENDES SANTANA', 'ERIC OLIVEIRA GUIMARÃES', 
        'ERICK RIAN DE OLIVEIRA FERREIRA', 'FRANCINY ANJOS VIEIRA', 'IAGO MATHEUS BARBOSA SILVA', 'ISABELLA JESUS NOVAIS DA SILVA', 
        'JOANA RAISSA SILVA DE ARAÚJO', 'JULIA DE SOUZA SANTOS', 'KELLY NAIANE DE NOVAIS ANJOS', 'LARA LORRANE ROCHA FERREIRA', 
        'LUNNA RIHANNA ALVES SANTOS', 'MAINARA DE SOUZA OLIVEIRA', 'MARINA DA SILVA FERREIRA', 'MATHEUS SOUZA DOS SANTOS', 
        'MIRELE SILVA BRANDÃO', 'NATALIA MENDES', 'NATIELE MENDES DE JESUS', 'RAQUEL RODRIGUES ALVES', 'SAMILLY SOUZA LEITE', 
        'SHEILA SILVIA DE OLIVEIRA', 'VITÓRIA EDUARDA BARROS ALVES', 'WELLINGTON PAULO SANTOS BARRETO'
    ],
    '2ª 3ª E FLUXO': [
        'ANGELA DE SOUZA SANTOS', 'BRENO MENDES DE SOUZA', 'CAMILA NOVAES DOS SANTOS', 'DANIELLY DOS ANJOS SOUZA', 
        'EDUARDO DE SOUZA SANTOS', 'ELOISA ALVES', 'EMERSON GABRIEL', 'FRANCIELE ALVES', 'FREDSON DOURADO MEDEIROS', 
        'GUILHERME S. PEREIRA', 'ICARO FELIPE DA SILVA SOUZA', 'ISIS CATARINE S. C.', 'JOAO PEDRO NOVAIS VENTURA', 
        'LAZARO SOUZA LOPES', 'MARIA LUISA SOUZA SILVA', 'MICAEL CAMBUI DE SOUZA', 'NILANE AMORIN CIRINO', 
        'OTAVIO DE SOUZA', 'PEDRO YAERLEM MOREIRA BRANDAO', 'RAI SANTOS', 'RICHARLES DOS SANTOS SOUZA', 
        'RUAN ALVES SANTANA', 'VITORIA', 'ZILMARIA DOS S. T.'
    ],
    '2ª D': [
        'ACASSIO DA SILVA MARTINS', 'ANDRYA DANIELLY ARAUJO DOS SANTOS', 'CLEILSON MEDEIROS DE SOUZA', 'ELLEN ENEDINA TELES FERNANDES', 
        'ELVIS ALENCAR DOS SANTOS SILVA', 'EZIELTON CONCEICAO MENDES', 'GABRIELA MARTINS SOUZA', 'GEAZI TEIXEIRA GOMES', 
        'GUILHERME BRAGA DE SOUZA', 'GUILHERME SOUZA DA SILVA', 'IAGO OLIVEIRA MENDES', 'ISANDRA DOS SANTOS DE SOUZA', 
        'JESSICA AMORIM DOS SANTOS', 'JOSE NILTON NASCIMENTO PINTO', 'JOVANA ALVES DOS SANTOS', 'LEANDRO SILVA DE SOUZA', 
        'LEILTON DA SILVA MENDES', 'LUIZ EDUARDO SOUZA VIEIRA', 'LUNA DA SILVA ARAUJO', 'LUNA MARIA PEREIRA DE SOUZA', 
        'MARIA LUIZA FARIAS DE PAULA', 'NAELE DE SOUZA', 'NATIELE OLIVEIRA SOUZA', 'PEDRO HENRIQUE FERREIRA GOMES', 
        'RAFAELLA DE SOUZA SANTOS', 'RAILA SOUZA AMORIM', 'RAY JOSÉ DA CONCEIÇÃO SANTOS', 'RICKELME SOUZA SILVA', 
        'RUBENS ALVES FERREIRA', 'SOPHIA ALCANTARA DE SOUZA BRANDAO', 'TAINÁ MENDES DE SOUZA', 'TATIANE MARTINS ARAUJO', 
        'UALISSON RUAN ARAUJO SOUZA', 'VANESSA SOUZA MENDES'
    ],
    '2ª INTEGRAL': [
        'Fabrício Reis de Oliveira', 'Gutierry Oliveira Souza', 'Igor Nunes da Silva', 'Ismael Gomes Batista', 
        'Joaquim Araujo de Carvalho', 'João Miguel Santos Araujo', 'Karina Almeida Carvalho', 'Lucas Manoel Nunes', 
        'Maria Eduarda Marques Araujo', 'Rafael Silva Teixeira', 'Raí Pereira da Rocha', 'Vitor Gabriel Santos Silva', 
        'Vitória Rosa de Oliveira'
    ],
    '3ªC ELETIVA': [
        'ALAN NOVAES DA SILVA', 'AMANDA GREGORIO ALVES', 'ANA JULIA DORADO DE JESUS', 'ANALY JESUS DOS SANTOS', 
        'ARYEL CAIQUE SANTOS MENDES', 'BENJAMIM SANTANA RODRIGUES', 'BÁRBARA PEREIRA DE OLIVEIRA', 'CAIO GOIS SOUZA', 
        'CARLOS DANIEL DINIZ OLIVEIRA', 'DAVISON OLIVEIRA SILVA', 'EDINEI ARAUJO DE SOUZA', 'ELOISE SILVA FERREIRA', 
        'ELVITON JUNIOR PEREIRA DOS ANJOS', 'FLAVIO PINTO ALVES', 'GISELE SANTOS ANTUNES', 'GLEICE LIMA MENDES', 
        'GUILHERME ARAUJO DE NOVAES', 'GUILHERME PINA DE OLIVEIRA', 'IASMIM SILVA OLIVEIRA', 'INGRED DREGER DE JESUS', 
        'ITALO MENDES SANTOS', 'JAIELE MARQUES DE OLIVEIRA', 'JULIANE ANJOS MENDES', 'KEILLA OLIVIERA DE SOUZA', 
        'LAIANE SOUZA SANTOS', 'LEILTON ALVES DA SILVA', 'LILIAN SIMONI MORAES ALVES', 'LUCAS WENDEL MATOS DE OLIVEIRA', 
        'LUIS DANIEL DIAS BRANDÃO', 'MARCOS ANTONIO SOUZA DE JESUS', 'MICHEL SANTOS OLIVEIRA', 'NATALÍ BARBOSA DOS ANJOS', 
        'RENATO DA SILVA FRANÇA', 'STEFANE OLIVEIRA DOS ANJOS', 'THAINÁ SILVA MELO', 'THAUÃ VICTOR DE OLIVEIRA SANTOS', 
        'UANDERSON DOS REIS SILVA', 'WEVERTON GASPAR DE SOUZA'
    ],
}

# ==============================================================================
# FUNÇÕES UTILITÁRIAS
# ==============================================================================
def normalizar_nome(nome):
    return "".join(c for c in unicodedata.normalize('NFKD', nome) if not unicodedata.combining(c)).lower()

def gerar_username(nome, sufixo_extra=""):
    parts = normalizar_nome(nome).split()
    base = f"{parts[0]}.{parts[-1]}" if len(parts) >= 2 else parts[0]
    return f"{base}{sufixo_extra}"

def gerar_nascimento_adolescente():
    ano = date.today().year - random.randint(15, 18)
    return date(ano, random.randint(1, 12), random.randint(1, 28))

def gerar_cpf_fake():
    return f"{random.randint(100,999)}.{random.randint(100,999)}.{random.randint(100,999)}-{random.randint(10,99)}"

# ==============================================================================
# SCRIPT DE POPULAÇÃO
# ==============================================================================
def run():
    print("--- 🏫 INICIANDO CADASTRO DO COLÉGIO ESTADUAL DE SEABRA ---")

    # 1. Escola e Tenant
    escola, _ = School.objects.get_or_create(
        nome='Colegio Estadual de Seabra - CES',
        defaults={'tipo': 'SaaS_Head'}
    )
    if not escola.tenant_id:
        escola.tenant_id = uuid.uuid4()
        escola.save()
    tenant_uuid = escola.tenant_id
    
    # Define ID sequencial da escola (Ex: 01)
    ESCOLA_ID = 1 

    # 2. Professor Ian (Diretor/Admin)
    cpf_ian = "000.000.000-01"
    mat_ian = gerar_matricula_padrao(ESCOLA_ID, 30, 1, cpf_ian) # 30 = DIRETOR
    
    ian, _ = CustomUser.objects.update_or_create(
        username='iansantos',
        defaults={
            'email': 'ianworktech@gmail.com',
            'first_name': 'Ian',
            'last_name': 'Santos',
            'role': 'DIRETOR',
            'matricula': mat_ian,
            'cpf': cpf_ian,
            'school': escola,
            'tenant_id': tenant_uuid,
            'is_staff': True, 'is_superuser': True, 'is_professor': True,
            'cidade_atual': 'Seabra',
            'instituicao_ensino': 'Colégio Estadual de Seabra - CES',
            'atuacao': 'Professor de Tecnologia'
        }
    )
    ian.set_password('134679')
    ian.save()
    print(f"✅ Professor: Ian Santos (Mat: {mat_ian})")

    # 3. Processar Turmas e Alunos
    sequencial_global = 2 # Começa do 2 pois o Ian é o 1
    count_alunos = 0

    for nome_turma, lista_alunos in DATA_EXTRACTED.items():
        # A. Criar Turma
        turma, created = Turma.objects.get_or_create(
            nome=nome_turma,
            defaults={
                'ano_letivo': 2026,
                'periodo': 'Integral' if 'INTEGRAL' in nome_turma else 'Matutino'
            }
        )
        print(f"\n📂 Turma: {nome_turma} ({len(lista_alunos)} alunos)")

        # B. Criar Alunos
        for nome_completo in lista_alunos:
            parts = nome_completo.strip().title().split()
            first = parts[0]
            last = " ".join(parts[1:]) if len(parts) > 1 else ""
            
            # Gera dados únicos
            sequencial_global += 1
            cpf_fake = gerar_cpf_fake()
            
            # Matrícula Padrão: 00 = Cargo Aluno
            matricula_unica = gerar_matricula_padrao(ESCOLA_ID, 0, sequencial_global, cpf_fake)
            
            # Username único (adiciona parte do seq para evitar colisão de homônimos)
            username = gerar_username(nome_completo, sufixo_extra=f"{sequencial_global}")
            email_fake = f"{username}@ces.edu.br"

            # Cria User
            try:
                user, created = CustomUser.objects.update_or_create(
                    username=username,
                    defaults={
                        'first_name': first,
                        'last_name': last,
                        'email': email_fake,
                        'matricula': matricula_unica, # CHAVE ÚNICA GARANTIDA
                        'cpf': cpf_fake,
                        'role': 'ALUNO',
                        'tenant_id': tenant_uuid,
                        'school': escola,
                        'turma': turma,
                        'is_aluno': True,
                        'data_nascimento': gerar_nascimento_adolescente(),
                        'cidade_natal': 'Seabra',
                        'cidade_atual': 'Seabra',
                        'instituicao_ensino': 'CES',
                        'status_relacionamento': 'SOLTEIRO',
                        'endereco': 'Seabra, Bahia'
                    }
                )
                
                if created:
                    user.set_password('123456')
                    user.save()
                    count_alunos += 1
                    
                    # Cria Perfil Pedagógico (agora sem erros de nome/matricula)
                    if not hasattr(user, 'perfil_escolar'):
                        Aluno.objects.create(
                            usuario=user,
                            turma=turma,
                            matricula_escolar=matricula_unica
                        )
                    
                    # Cria Álbuns
                    if not user.albuns.exists():
                        Album.objects.create(usuario=user, titulo="Fotos de Perfil", privacidade='PUBLIC')
                        Album.objects.create(usuario=user, titulo="Linha do Tempo", privacidade='PUBLIC')

            except Exception as e:
                print(f"   ❌ Erro ao criar {first} {last}: {e}")

    print(f"\n✅ IMPORTAÇÃO CONCLUÍDA!")
    print(f"   - Total Alunos Processados: {count_alunos}")
    print(f"   - Padrão de Matrícula: AAAA+SM+MM+EE+CC+SEQ+CPF")

if __name__ == "__main__":
    run()