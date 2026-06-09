# fastapi_service/tests/test_education_rag.py
import pytest
import httpx
import os

# Configura o ambiente para forçar o mock inteligente e evitar chamadas reais à API externa nos testes
os.environ["HEMERA_FORCE_MOCK"] = "true"
os.environ["SERVICE_TOKEN_SECRET"] = "test-secret-token"

from fastapi_service.main import app

def get_headers() -> dict:
    return {
        "x-service-token": "test-secret-token"
    }

@pytest.mark.anyio
async def test_generate_exam_with_rag_grounding_history():
    payload = {
        "tema": "Era Vargas e CLT",
        "nivel": "9º Ano",
        "dificuldade": "medio",
        "qtd_questoes": 2,
        "tipo_questoes": ["multipla_escolha"],
        "contexto_bncc": True
    }

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.post(
            "/v1/education/exam", 
            json=payload, 
            headers=get_headers()
        )

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "conteudo" in data
    assert "gabarito" in data
    
    # Verificar ancoragem RAG na estrutura da prova
    prova = data["prova_estruturada"]
    assert prova["titulo_sugerido"] is not None
    assert len(prova["questoes"]) == 2
    
    # Verificar se as fontes foram mapeadas na primeira questão
    q1 = prova["questoes"][0]
    assert len(q1["fontes_ancoradas"]) > 0
    fonte = q1["fontes_ancoradas"][0]
    assert "Apostila de História" in fonte["documento"]
    assert fonte["pagina"] == 15
    assert "Getúlio Vargas" in fonte["trecho"] or "CLT" in fonte["trecho"]

    # Verificar metadados do RAG
    metadata = data["metadata"]
    assert "Apostila de História - 9º Ano" in metadata["documentos_consultados"]


@pytest.mark.anyio
async def test_generate_exam_with_rag_grounding_science():
    payload = {
        "tema": "Fontes de Energia Renováveis",
        "nivel": "8º Ano",
        "dificuldade": "facil",
        "qtd_questoes": 1,
        "tipo_questoes": ["multipla_escolha"],
        "contexto_bncc": True
    }

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.post(
            "/v1/education/exam", 
            json=payload, 
            headers=get_headers()
        )

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    
    prova = data["prova_estruturada"]
    q1 = prova["questoes"][0]
    assert len(q1["fontes_ancoradas"]) > 0
    fonte = q1["fontes_ancoradas"][0]
    assert "Apostila de Ciências" in fonte["documento"]
    assert fonte["pagina"] == 74
    assert "energia" in fonte["trecho"].lower() or "renováveis" in fonte["trecho"].lower()


@pytest.mark.anyio
async def test_generate_exam_rag_not_found():
    # Procurar por um assunto inexistente nas apostilas mockadas
    payload = {
        "tema": "Física Quântica Avançada e Computação Nuclear",
        "nivel": "9º Ano",
        "dificuldade": "dificil",
        "qtd_questoes": 1,
        "tipo_questoes": ["discursiva"],
        "contexto_bncc": True
    }

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.post(
            "/v1/education/exam", 
            json=payload, 
            headers=get_headers()
        )

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    
    prova = data["prova_estruturada"]
    assert "Geral" in prova["titulo_sugerido"]
    # A primeira questão deve avisar que o tema não foi localizado nas fontes ativas
    q1 = prova["questoes"][0]
    assert "não foi localizado" in q1["enunciado"]
    assert len(q1["fontes_ancoradas"]) == 0


@pytest.mark.anyio
async def test_generate_lesson_plan_with_rag():
    payload = {
        "tema": "Guerra Fria",
        "disciplina": "História",
        "nivel": "9º Ano",
        "duracao": "50 minutos",
        "metodologia": "Sala de Aula Invertida"
    }

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.post(
            "/v1/education/lesson_plan", 
            json=payload, 
            headers=get_headers()
        )

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "conteudo" in data
    assert "EF09HI01" in data["codigos_bncc"]
    assert len(data["fontes_ancoradas"]) > 0
    assert "Apostila de História - 9º Ano" in data["fontes_ancoradas"][0]["documento"]


@pytest.mark.anyio
async def test_generate_activity_with_rag():
    payload = {
        "tema": "Consumo Consciente de Energia",
        "nivel": "8º Ano",
        "ludico": True
    }

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.post(
            "/v1/education/activity", 
            json=payload, 
            headers=get_headers()
        )

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "conteudo" in data
    assert "instrucoes_professor" in data
    assert len(data["fontes_ancoradas"]) > 0
    assert "Apostila de Ciências - 8º Ano" in data["fontes_ancoradas"][0]["documento"]


@pytest.mark.anyio
async def test_analyze_student():
    payload = {
        "nome": "Arthur Pendragon",
        "turma": "9º A",
        "metricas": {
            "media": 5.4,
            "frequencia": 82.5,
            "notas_recentes": [5.0, 6.0, 5.2],
            "observacoes": ["Falta de foco nas aulas de história"]
        }
    }

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.post(
            "/v1/education/analyze_student", 
            json=payload, 
            headers=get_headers()
        )

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["risco_evasao"] == "Alto"
    assert "recuperação" in data["sugestao_acao"].lower()
    assert "analise_estruturada" in data
