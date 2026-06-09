import pytest
from decimal import Decimal
from django.contrib.auth import get_user_model
from core.models import School
from lumenios.pedagogico.models import Turma, Aluno, Disciplina, Atividade, Nota, PlanoDeAula
from seshat.indexer import SeshatIndexer

CustomUser = get_user_model()

@pytest.mark.django_db
def test_index_grades_success():
    parsed_grades = {
        "turma_nome_original": "1ª A ADM",
        "atividades": ["PROVA 1", "TRABALHO 1"],
        "alunos": [
            {
                "nome": "João Silva",
                "notas": [Decimal("8.0"), Decimal("9.5")],
                "situacao": "APROVADO"
            },
            {
                "nome": "Maria Souza",
                "notas": [Decimal("5.0"), Decimal("7.0")],
                "situacao": "RECUPERAÇÃO"
            }
        ]
    }
    
    indexer = SeshatIndexer()
    
    # Run the indexer (which will apply transition 1ª -> 2ª)
    result = indexer.index_grades(parsed_grades, apply_transition=True)
    
    assert result["status"] == "indexed"
    assert result["turma"] == "2ª A ADM"
    assert result["atividades_criadas"] == 2
    assert result["alunos_indexados"] == 2
    assert result["notas_indexadas"] == 4
    
    # Verify DB persistence
    # 1. School check
    assert School.objects.filter(nome="Hemera Escola Padrão").exists()
    
    # 2. Turma check
    turma = Turma.objects.get(nome="2ª A ADM")
    assert turma.ano_letivo == 2026
    
    # 3. Disciplina check
    disciplina = Disciplina.objects.get(nome="Disciplina Base", turma=turma)
    
    # 4. Atividades check
    assert Atividade.objects.filter(turma=turma, disciplina=disciplina).count() == 2
    ativ_prova = Atividade.objects.get(turma=turma, titulo="PROVA 1")
    
    # 5. Aluno check
    aluno_joao = Aluno.objects.get(nome="João Silva", turma=turma)
    assert CustomUser.objects.filter(username="joao.silva", role="Student").exists()
    
    # 6. Notas check
    nota_prova_joao = Nota.objects.get(aluno=aluno_joao, atividade=ativ_prova)
    assert nota_prova_joao.valor == Decimal("8.0")


@pytest.mark.django_db
def test_index_grades_graduated_ignored():
    parsed_grades = {
        "turma_nome_original": "3ª C ELETIVA",
        "atividades": ["PROVA 1"],
        "alunos": [
            {
                "nome": "Alan Turing",
                "notas": [Decimal("10.0")],
                "situacao": "APROVADO"
            }
        ]
    }
    
    indexer = SeshatIndexer()
    result = indexer.index_grades(parsed_grades, apply_transition=True)
    
    assert result["status"] == "ignored"
    assert "graduated" in result["reason"]
    
    # Check that no Turma was created for 3ª C
    assert not Turma.objects.filter(nome__contains="3ª C").exists()


@pytest.mark.django_db
def test_index_grades_no_transition():
    parsed_grades = {
        "turma_nome_original": "3ª C ELETIVA",
        "atividades": ["PROVA 1"],
        "alunos": [
            {
                "nome": "Alan Turing",
                "notas": [Decimal("10.0")],
                "situacao": "APROVADO"
            }
        ]
    }
    
    indexer = SeshatIndexer()
    result = indexer.index_grades(parsed_grades, apply_transition=False)
    
    assert result["status"] == "indexed"
    assert result["turma"] == "3ª C ELETIVA"
    assert Turma.objects.filter(nome="3ª C ELETIVA").exists()


@pytest.mark.django_db
def test_index_syllabus():
    parsed_syllabus = {
        "disciplina": "História Geral",
        "carga_horaria": "60h",
        "objetivos": "Compreender a antiguidade clássica.",
        "habilidades": "BNCC: EM13CHS101",
        "conteudo_programatico": [
            {"titulo": "1. Grécia Antiga", "ordem": 1, "detalhes": "Democracia ateniense e Esparta"},
            {"titulo": "2. Império Romano", "ordem": 2, "detalhes": "Pax Romana e queda do império"}
        ],
        "referencias": "Gibbon, Edward. Queda do Império Romano."
    }
    
    indexer = SeshatIndexer()
    result = indexer.index_syllabus(parsed_syllabus)
    
    assert result["status"] == "indexed"
    assert result["disciplina"] == "História Geral"
    assert result["planos_de_aula_criados"] == 2
    
    # Verify Planos de Aula in DB
    turma = Turma.objects.get(nome="Turma Geral SESHAT")
    disciplina = Disciplina.objects.get(nome="História Geral", turma=turma)
    
    planos = PlanoDeAula.objects.filter(turma=turma).order_by('titulo')
    assert planos.count() == 2
    
    plano_romano = planos.filter(titulo__contains="Romano").first()
    assert plano_romano is not None
    assert "Pax Romana" in plano_romano.conteudo
    assert plano_romano.habilidades_bncc == "BNCC: EM13CHS101"
    assert "Gibbon" in plano_romano.referencias


@pytest.mark.django_db
def test_index_booklet():
    parsed_booklet = {
        "titulo": "Apostila de Química Orgânica",
        "capitulos": [
            {
                "numero": "1",
                "titulo": "Introdução ao Carbono",
                "conteudo": "O carbono é um elemento tetravalente.",
                "exercicios": [
                    "1. Desenhe a estrutura do metano.",
                    "2. Defina hibridização."
                ]
            },
            {
                "numero": "2",
                "titulo": "Hidrocarbonetos",
                "conteudo": "Alcanos, alcenos e alcinos.",
                "exercicios": []
            }
        ]
    }
    
    indexer = SeshatIndexer()
    result = indexer.index_booklet(parsed_booklet)
    
    assert result["status"] == "indexed"
    assert result["planos_de_aula_criados"] == 2
    assert result["atividades_de_exercicio_criadas"] == 1  # only Chapter 1 has exercises
    
    # Verify DB
    turma = Turma.objects.get(nome="Turma Geral SESHAT")
    disciplina = Disciplina.objects.get(nome="Apostila de Química Orgânica", turma=turma)
    
    # PlanoDeAula verification
    planos = PlanoDeAula.objects.filter(turma=turma)
    assert planos.count() == 2
    
    # Atividade verification
    assert Atividade.objects.filter(turma=turma, disciplina=disciplina).count() == 1
    ativ = Atividade.objects.get(turma=turma, disciplina=disciplina)
    assert "metano" in ativ.descricao
