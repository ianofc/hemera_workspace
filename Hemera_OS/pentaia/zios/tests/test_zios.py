import os
import shutil
import pytest
import sqlite3
import json
from datetime import datetime, timezone, timedelta
from fastapi.testclient import TestClient

from core.memory import ZiosMemory
from core.resonance import ResonanceEngine
from core.coding import ZiosSelfCoder
from core.zios import ZiosOrchestrator
from main import app

# --- TESTES DA INGESTÃO EPISÓDICA ---

def test_memory_sqlite_fallback(tmp_path):
    # Força uso de SQLite criando um DB temporário
    db_file = tmp_path / "test_zios_memory.db"
    
    # Instancia a memória
    memory = ZiosMemory(user_id="test_user", db_url=None, google_api_key=None)
    memory.sqlite_db_path = str(db_file)
    memory._init_sqlite()
    
    # 1. Verifica se a tabela foi inicializada
    assert os.path.exists(db_file)
    
    # 2. Persiste um episódio
    input_text = "testar conexao de rede"
    output_text = "porta 8080 liberada com sucesso"
    context = {"urgency": 0.5, "tags": ["rede"]}
    
    episode_id = memory.persist(input_text, output_text, context)
    assert episode_id is not None
    
    # Valida persistência direta no SQLite
    conn = sqlite3.connect(str(db_file))
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM zios_episodic_memory WHERE id = ?", (episode_id,))
    row = cursor.fetchone()
    conn.close()
    
    assert row is not None
    assert row["user_id"] == "test_user"
    assert row["input_data"] == input_text
    assert row["output_data"] == output_text
    assert "rede" in row["context"]
    
    # 3. Testa o recall semântico/temporal
    recalled = memory.recall(query="testar conexao", limit=1)
    assert len(recalled) > 0
    assert "testar conexao" in recalled[0] or "porta 8080" in recalled[0]
    
    # Limpa
    memory.clear()
    
    conn = sqlite3.connect(str(db_file))
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM zios_episodic_memory")
    count = cursor.fetchone()[0]
    conn.close()
    assert count == 0


# --- TESTES DA FILTRAGEM POR RESSONÂNCIA ---

def test_resonance_engine():
    engine = ResonanceEngine()
    
    # 1. Caso com baixa ressonância (não deve intervir)
    low_context = {
        "urgency": 0.2,
        "user_relevance": 0.1,
        "impact": 0.1,
        "security_risk": 0.1
    }
    score_low = engine.calculate_resonance(low_context)
    assert score_low < 0.5
    assert not engine.should_intervene(low_context, threshold=0.7)
    
    # 2. Caso com alta urgência e relevância de usuário master (deve intervir)
    high_context = {
        "urgency": 0.9,
        "user_id": "ian_master",
        "impact": 0.5,
        "security_risk": 0.2
    }
    score_high = engine.calculate_resonance(high_context)
    assert score_high >= 0.7
    assert engine.should_intervene(high_context, threshold=0.7)
    
    # 3. Caso com ameaça de segurança (Heimdall alert)
    security_context = {
        "urgency": 0.4,
        "threat_detected": True,
        "shield_level": "ELEVATED",
        "impact": 0.3
    }
    score_security = engine.calculate_resonance(security_context)
    assert score_security > 0.5
    
    # 4. Priorização de lista de contextos
    contexts = [
        {"urgency": 0.1, "user_relevance": 0.1},
        {"urgency": 0.9, "user_id": "ian_master"},
        {"urgency": 0.5, "impact": 0.5}
    ]
    prioritized = engine.prioritize_contexts(contexts, threshold=0.3)
    assert len(prioritized) >= 2
    assert prioritized[0]["urgency"] == 0.9


# --- TESTES DA AUTO-CODIFICAÇÃO (SANDBOX) ---

def test_self_coder_pipeline(tmp_path):
    sandbox_path = tmp_path / "sandbox_test_run"
    coder = ZiosSelfCoder(sandbox_base_path=str(sandbox_path))
    
    # 1. Testa geração de código e teste (estático/fallback do soma)
    script_code, test_code = coder.generate_code_and_tests("Preciso de uma calculadora de soma")
    assert "def soma" in script_code
    assert "test_soma" in test_code
    
    # 2. Testa execução do pytest na sandbox com sucesso
    test_result = coder.sandbox_test(script_code, test_code)
    assert test_result["success"] is True
    assert test_result["returncode"] == 0
    assert "test_soma" in test_result["stdout"]
    
    # 3. Testa aplicação final do código (apply)
    destination = tmp_path / "applied_tools" / "math_tool.py"
    apply_result = coder.apply_code(script_code, str(destination), test_code)
    assert apply_result["applied"] is True
    assert os.path.exists(destination)
    
    with open(destination, "r", encoding="utf-8") as f:
        content = f.read()
    assert "def soma" in content

def test_self_coder_safety_rejection(tmp_path):
    coder = ZiosSelfCoder(sandbox_base_path=str(tmp_path))
    
    # Código malicioso violando segurança
    malicious_code = """
import os
def delete_all():
    os.system("rm -rf /")
"""
    test_code = "def test_ok(): assert True"
    
    result = coder.sandbox_test(malicious_code, test_code)
    assert result["success"] is False
    assert "SecurityViolation" in result["error"]


# --- TESTES DA API E INTEGRADOS ---

def test_api_endpoints():
    with TestClient(app) as client:
        # 1. Root e health
        response = client.get("/")
        assert response.status_code == 200
        assert response.json()["status"] == "OPERATIONAL"
        
        response = client.get("/health")
        assert response.status_code == 200
        assert "brain" in response.json()["components"]
        
        # 2. Persistir memória episódica via API
        persist_req = {
            "input_data": "auditoria de rede",
            "output_data": "sistema estavel",
            "context": {"urgency": 0.3}
        }
        response = client.post("/api/v1/zios/memory/persist", json=persist_req)
        assert response.status_code == 200
        assert response.json()["status"] == "success"
        episode_id = response.json()["episode_id"]
        assert episode_id is not None
        
        # 3. Recall de memória via API
        recall_req = {
            "query": "auditoria",
            "limit": 5,
            "threshold": 0.0
        }
        response = client.post("/api/v1/zios/memory/recall", json=recall_req)
        assert response.status_code == 200
        assert response.json()["status"] == "success"
        assert len(response.json()["episodes"]) > 0
        
        # 4. Proactive Status e trigger
        response = client.get("/api/v1/proactive/status")
        assert response.status_code == 200
        assert response.json()["active"] is True
        
        # Testa desativar/ativar loop
        response = client.post("/api/v1/proactive/toggle?active=false")
        assert response.status_code == 200
        assert response.json()["active"] is False
        
        response = client.post("/api/v1/proactive/toggle?active=true")
        assert response.status_code == 200
        assert response.json()["active"] is True
        
        # Força trigger proativo
        response = client.post("/api/v1/proactive/trigger")
        assert response.status_code == 200
        assert response.json()["status"] == "triggered"
        
        # 5. Pipeline de Auto-Codificação via API
        self_coding_req = {
            "task_description": "Preciso de um formatador slug para logs",
            "destination_path": "sandbox/applied/slug_tool.py"
        }
        response = client.post("/api/v1/proactive/self-coding/test", json=self_coding_req)
        assert response.status_code == 200
        assert response.json()["status"] == "success"
        assert response.json()["result"]["applied"] is True
        assert os.path.exists("sandbox/applied/slug_tool.py")
        
        # Limpeza pós-teste
        if os.path.exists("sandbox/applied/slug_tool.py"):
            os.remove("sandbox/applied/slug_tool.py")
