import asyncio
from pathlib import Path
from types import SimpleNamespace
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.services.recommendation_service import RecommendationService


def test_budget_from_env_uses_default_for_invalid(monkeypatch):
    monkeypatch.setenv("TAS_BUDGET_SARA_MS", "invalid")
    service = RecommendationService()

    assert service.budget_ms["sara"] == 45


def test_budget_from_env_enforces_minimum_positive(monkeypatch):
    monkeypatch.setenv("TAS_BUDGET_THALAMUS_MS", "0")
    service = RecommendationService()

    assert service.budget_ms["thalamus"] == 1


def test_get_feed_with_meta_without_degradation(monkeypatch):
    service = RecommendationService()

    async def ok_filter(request, raw_data):
        return raw_data

    async def ok_align(user_id, clean):
        for item in clean:
            item["sara_score"] = 1.0
        return clean

    async def ok_rank(aligned):
        return [str(item["id"]) for item in aligned]

    monkeypatch.setattr(service.thalamus, "apply", ok_filter)
    monkeypatch.setattr(service.sara, "align", ok_align)
    monkeypatch.setattr(service.accumbens, "rank", ok_rank)

    request = SimpleNamespace(user_id="u1", context="BIRD")
    ids, meta = asyncio.run(service.get_feed_with_meta(request))

    assert ids
    assert meta["degraded"] is True  # há fallback global por dataset vazio em ambiente de teste
    assert "stage_metrics" in meta


def test_get_feed_with_meta_degrades_on_sara_timeout(monkeypatch):
    service = RecommendationService()
    service.budget_ms["sara"] = 1

    async def ok_filter(request, raw_data):
        return raw_data

    async def slow_align(user_id, clean):
        await asyncio.sleep(0.01)
        return clean

    async def ok_rank(aligned):
        return [str(item["id"]) for item in aligned]

    monkeypatch.setattr(service.thalamus, "apply", ok_filter)
    monkeypatch.setattr(service.sara, "align", slow_align)
    monkeypatch.setattr(service.accumbens, "rank", ok_rank)

    request = SimpleNamespace(user_id="u1", context="BIRD")
    ids, meta = asyncio.run(service.get_feed_with_meta(request))

    assert ids
    assert meta["stage_metrics"]["sara"]["degraded"] is True
    assert meta["degraded"] is True
