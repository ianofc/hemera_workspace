import asyncio
import sys
from pathlib import Path
from types import SimpleNamespace
import pytest

# Adiciona o diretório pai (raiz do TAS) ao sys.path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.engines.thalamus.ingress import thalamus_ingress
from app.engines.thalamus.queue import talamus_queue
from app.engines.accumbens.rl import accumbens_rl, process_feedback_event
from app.engines.accumbens.ranker import AccumbensRanker
from app.engines.sara.vigilance import sara_vigilance


# =====================================================================
# 1. TESTES DO TALAMUS (Sanitização, Vetos e Ingress)
# =====================================================================

def test_thalamus_sanitization_removes_html_and_bad_chars():
    dirty_string = "<script>alert('xss')</script> Safe Content \x00"
    sanitized = thalamus_ingress.sanitize_string(dirty_string)
    assert "script" not in sanitized
    assert "alert" in sanitized
    assert "Safe Content" in sanitized
    # SQL characters check
    assert ";" not in sanitized


def test_thalamus_vetos_illegal_tags():
    tags = ["politics", "cp", "sports", "terrorism_action"]
    clean_tags = thalamus_ingress.sanitize_tags(tags)
    assert "politics" in clean_tags
    assert "sports" in clean_tags
    assert "cp" not in clean_tags
    assert "terrorism_action" not in clean_tags


def test_thalamus_event_payload_sanitation():
    payload = {
        "title": "<h1>Super Title</h1>",
        "tags": ["tech", "cp"],
        "nested": {
            "comment": "Bad script <iframe src='...'></iframe>"
        }
    }
    sanitized = thalamus_ingress.sanitize_event_payload(payload)
    assert sanitized["title"] == "Super Title"
    assert "tech" in sanitized["tags"]
    assert "cp" not in sanitized["tags"]
    assert "iframe" not in sanitized["nested"]["comment"]


@pytest.mark.asyncio
async def test_talamus_queue_async_dispatch():
    # Cria um handler mock
    events_received = []
    
    def mock_handler(event):
        events_received.append(event)

    talamus_queue.register_handler(mock_handler)
    
    # Inicia a fila
    await talamus_queue.start()
    
    # Publica evento
    event = {"user_id": "user_test", "action": "click", "tags": ["sports"]}
    await talamus_queue.publish(event)
    
    # Espera o processamento assíncrono
    await asyncio.sleep(0.1)
    
    assert len(events_received) == 1
    assert events_received[0]["user_id"] == "user_test"
    assert events_received[0]["action"] == "click"
    
    await talamus_queue.stop()


# =====================================================================
# 2. TESTES DO ACCUMBENS (Reinforcement Learning e Scoring)
# =====================================================================

@pytest.mark.asyncio
async def test_accumbens_rl_updates_memory_fallback():
    user_id = "user_rl_1"
    tags = ["gaming", "science"]
    
    # Simula ação de like (recompensa +3.0)
    # Como não temos conexão de banco ativa no pytest (ou se falhar),
    # ele deve cair de volta na memória local.
    await accumbens_rl.update_user_preferences(user_id, tags, "like")
    
    interests = accumbens_rl.get_fallback_interests(user_id)
    assert interests["gaming"] > 0
    assert interests["science"] > 0
    
    # Simula ação de boredom (recompensa -5.0)
    await accumbens_rl.update_user_preferences(user_id, ["gaming"], "boredom")
    interests_after = accumbens_rl.get_fallback_interests(user_id)
    assert interests_after["gaming"] < interests["gaming"]


@pytest.mark.asyncio
async def test_accumbens_ranker_incorporates_rl_boost():
    ranker = AccumbensRanker()
    user_id = "user_rank_test"
    
    # Dá preferência do usuário via RL fallback para tag 'music'
    accumbens_rl.memory_fallback_profiles[user_id] = {"music": 15.0, "sports": -5.0}
    
    candidates = [
        {"id": "cand_1", "tags": ["sports"], "predicted_likes": 0, "sara_score": 0.5},
        {"id": "cand_2", "tags": ["music"], "predicted_likes": 0, "sara_score": 0.5},
    ]
    
    # Sem o perfil do usuário, ambos deveriam pontuar de forma parecida
    ranked_no_profile = await ranker.rank(candidates)
    
    # Com o perfil de preferência do usuário e o RL boost
    ranked_with_profile = await ranker.rank(candidates, user_id=user_id)
    
    # cand_2 deve vir em primeiro devido ao boost de +15.0 na tag 'music'
    assert ranked_with_profile[0] == "cand_2"


# =====================================================================
# 3. TESTES DA SARA (Vigília, HPA e Dynamic Budgets)
# =====================================================================

def test_sara_vigilance_state_transitions():
    daemon = sara_vigilance
    
    # Estado inicial
    assert daemon.state in ["SLEEP", "NORMAL", "WAKE"]
    
    # Simula carga baixa e sem requisições -> SLEEP
    daemon.request_count = 0
    daemon.evaluate_system_state()
    assert daemon.state == "SLEEP"
    assert daemon.scale_up_needed is False
    assert daemon.hpa_replicas == 1
    
    # Simula pico de carga (RPS alto e latência alta) -> WAKE
    daemon.request_count = 100 # Em 5 segundos dá 20 RPS
    daemon.total_latency = 5000.0 # 50ms de média
    daemon.evaluate_system_state()
    
    assert daemon.state == "WAKE"
    assert daemon.scale_up_needed is True
    assert daemon.hpa_replicas >= 3
    # Os budgets em estado WAKE devem ser menores (corte rápido)
    assert daemon.current_budgets["sara"] < daemon.budgets["NORMAL"]["sara"]


def test_sara_vigilance_status_reporting():
    status = sara_vigilance.get_status()
    assert "state" in status
    assert "rps" in status
    assert "eps" in status
    assert "cpu_percent" in status
    assert "hpa" in status
    assert "active_budgets_ms" in status
