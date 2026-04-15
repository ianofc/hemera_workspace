from heimdall.audit import AuditLogger, SecurityEvent
from heimdall.auth import PasswordGuard, hash_token, verify_token
from heimdall.config import HeimdallSettings
from heimdall.integrity import EndpointGuard, EndpointPolicy
from heimdall.rate_limit import SlidingWindowRateLimiter
from heimdall.threats import ThreatDetector


def test_password_policy_and_token_hashing():
    guard = PasswordGuard(HeimdallSettings().password)
    ok, errors = guard.validate("Fraca123")
    assert not ok
    assert errors

    ok2, errors2 = guard.validate("SenhaForte@2026")
    assert ok2
    assert not errors2

    digest = hash_token("token-abc", "salt")
    assert verify_token("token-abc", digest, "salt")
    assert not verify_token("token-diff", digest, "salt")


def test_threat_detector_blocks_cidr():
    detector = ThreatDetector.from_cidrs({"10.0.0.0/8"})
    blocked = detector.evaluate_ip("10.2.3.4")
    allowed = detector.evaluate_ip("8.8.8.8")

    assert blocked.allowed is False
    assert allowed.allowed is True


def test_rate_limiter_window():
    limiter = SlidingWindowRateLimiter(requests=2, window_seconds=60)
    first = limiter.check("ip:/path")
    second = limiter.check("ip:/path")
    third = limiter.check("ip:/path")

    assert first.allowed is True
    assert second.allowed is True
    assert third.allowed is False


def test_audit_logger_redacts_sensitive_fields():
    logger = AuditLogger({"password", "token"})
    logger.log(
        SecurityEvent(
            event_type="login",
            actor_id="u1",
            source_ip="1.1.1.1",
            outcome="failed",
            details={"password": "123", "meta": {"token": "abc"}},
        )
    )

    event = logger.recent(1)[0]
    assert event.details["password"] == "***"
    assert event.details["meta"]["token"] == "***"


def test_endpoint_guard_policy():
    guard = EndpointGuard([
        EndpointPolicy(path="/public", requires_auth=False, allows_public_get=True),
        EndpointPolicy(path="/private", requires_auth=True),
    ])

    ok_public, _ = guard.verify("/public", "GET", has_auth=False)
    blocked_private, reason = guard.verify("/private", "POST", has_auth=False)

    assert ok_public is True
    assert blocked_private is False
    assert reason == "Autenticação obrigatória"
