from core.safety import evaluate_safety
from core.models import UserAction

def test_safety_child_protection():
    action = UserAction(
        action_type="SEARCH",
        context_environment="IO_LIFE_MAIN",
        content_tags=["criança", "nsfw"]
    )
    verdict = evaluate_safety(action, user_age=30, user_id="test")
    assert verdict.allowed == False
    assert verdict.risk_level == "CRITICAL"

def test_dex_access():
    action = UserAction(
        action_type="VIEW",
        context_environment="DEX_FEED",
        content_tags=["NSFW"]
    )
    verdict = evaluate_safety(action, user_age=30, user_id="test")
    assert verdict.allowed == True