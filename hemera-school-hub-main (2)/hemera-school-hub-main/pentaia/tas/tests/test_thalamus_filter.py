import asyncio
from pathlib import Path
from types import SimpleNamespace
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.engines.thalamus.filters import ThalamusFilter


def test_study_context_is_case_insensitive_for_safety_filter():
    filter_engine = ThalamusFilter()
    req = SimpleNamespace(context="study")
    candidates = [
        {"id": "unsafe_1", "tags": ["science"], "safety": "unsafe"},
        {"id": "safe_1", "tags": ["science"], "safety": "safe"},
    ]

    result = asyncio.run(filter_engine.apply(req, candidates))

    assert [item["id"] for item in result] == ["safe_1"]
