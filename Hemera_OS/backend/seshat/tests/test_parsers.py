import pytest
from unittest.mock import patch
from decimal import Decimal
from io import BytesIO, StringIO

from seshat.parsers.grades import GradesParser
from seshat.parsers.syllabus import SyllabusParser
from seshat.parsers.booklet import BookletParser

# Mock helper classes for pypdf
class MockPage:
    def __init__(self, text):
        self.extracted_text = text
    def extract_text(self):
        return self.extracted_text

class MockPdfReader:
    def __init__(self, pages_text):
        self.pages = [MockPage(txt) for txt in pages_text]


def test_grades_parser_success():
    # Simulated grade spreadsheet content
    pdf_text = (
        "TURMA 1ª A ADM - RELATÓRIO DE NOTAS\n"
        "3ª Unidade\n"
        "ALUNO\n"
        "PROVA 17/11\n"
        "TRAB 25/11\n"
        "TOTAL\n"
        "SITUAÇÃO\n"
        "JOÃO SILVA\n"
        "8,5\n"
        "9,0\n"
        "17,5\n"
        "APROVADO\n"
        "MARIA SANTOS\n"
        "5,0\n"
        "6,5\n"
        "11,5\n"
        "RECUPERAÇÃO\n"
    )
    
    parser = GradesParser()
    
    with patch('pypdf.PdfReader', return_value=MockPdfReader([pdf_text])):
        # Pass a dummy stream
        fake_stream = BytesIO(b"dummy pdf content")
        result = parser.parse(fake_stream)
        
    assert result["turma_nome_original"] == "1ª A ADM"
    assert result["atividades"] == ["PROVA 17/11", "TRAB 25/11"]
    assert len(result["alunos"]) == 2
    
    joao = result["alunos"][0]
    assert joao["nome"] == "JOÃO SILVA"
    assert joao["notas"] == [Decimal("8.5"), Decimal("9.0")]
    assert joao["situacao"] == "APROVADO"
    
    maria = result["alunos"][1]
    assert maria["nome"] == "MARIA SANTOS"
    assert maria["notas"] == [Decimal("5.0"), Decimal("6.5")]
    assert maria["situacao"] == "RECUPERAÇÃO"


def test_grades_parser_invalid_format():
    pdf_text = "ESTE É UM PDF SEM FORMATO VALIDO"
    parser = GradesParser()
    
    with patch('pypdf.PdfReader', return_value=MockPdfReader([pdf_text])):
        fake_stream = BytesIO(b"dummy pdf content")
        with pytest.raises(ValueError, match="Invalid PDF format"):
            parser.parse(fake_stream)


def test_syllabus_parser_text():
    syllabus_text = (
        "Disciplina: Programação Web Avançada\n"
        "Carga Horária: 80 horas\n"
        "Objetivos: Ensinar frameworks modernos como React e Django REST.\n"
        "BNCC: EM13MITE01\n"
        "Conteúdo Programático:\n"
        "1. Introdução ao Protocolo HTTP\n"
        "- Protocolos, verbos e códigos de status\n"
        "2. Django REST Framework\n"
        "- Serializers e ViewSets\n"
        "Bibliografia:\n"
        "- Silva, J. (2024). Web com Python.\n"
    )
    
    parser = SyllabusParser()
    stream = StringIO(syllabus_text)
    result = parser.parse(stream)
    
    assert result["disciplina"] == "Programação Web Avançada"
    assert result["carga_horaria"] == "80 horas"
    assert "React e Django REST" in result["objetivos"]
    assert result["habilidades"] == "EM13MITE01"
    assert "Web com Python" in result["referencias"]
    
    assert len(result["conteudo_programatico"]) == 2
    t1 = result["conteudo_programatico"][0]
    assert t1["titulo"] == "1. Introdução ao Protocolo HTTP"
    assert t1["detalhes"] == "Protocolos, verbos e códigos de status"
    
    t2 = result["conteudo_programatico"][1]
    assert t2["titulo"] == "2. Django REST Framework"
    assert t2["detalhes"] == "Serializers e ViewSets"


def test_booklet_parser():
    booklet_text = (
        "Física Mecânica - 1ª Série\n"
        "Capítulo 1: Introdução à Cinemática\n"
        "A cinemática estuda os movimentos sem se preocupar com suas causas.\n"
        "Exercícios:\n"
        "1. O que é referencial?\n"
        "2. Diferencie trajetória e deslocamento.\n"
        "Capítulo 2: Leis de Newton\n"
        "As leis de Newton explicam as forças que causam os movimentos.\n"
        "Exercícios:\n"
        "1. Enuncie a primeira lei de Newton.\n"
    )
    
    parser = BookletParser()
    stream = StringIO(booklet_text)
    result = parser.parse(stream)
    
    assert result["titulo"] == "Física Mecânica - 1ª Série"
    assert len(result["capitulos"]) == 2
    
    chap1 = result["capitulos"][0]
    assert chap1["numero"] == "1"
    assert chap1["titulo"] == "Introdução à Cinemática"
    assert "sem se preocupar" in chap1["conteudo"]
    assert len(chap1["exercicios"]) == 2
    assert chap1["exercicios"][0] == "1. O que é referencial?"
    
    chap2 = result["capitulos"][1]
    assert chap2["numero"] == "2"
    assert chap2["titulo"] == "Leis de Newton"
    assert "causam os movimentos" in chap2["conteudo"]
    assert len(chap2["exercicios"]) == 1
    assert chap2["exercicios"][0] == "1. Enuncie a primeira lei de Newton."
