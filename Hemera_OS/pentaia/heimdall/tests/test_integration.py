from fastapi import FastAPI

from heimdall.integration import attach_heimdall, heimdall_enabled, settings_from_env


def test_heimdall_enabled_by_default_and_override(monkeypatch):
    monkeypatch.delenv("HEIMDALL_ENABLED", raising=False)
    assert heimdall_enabled(default=True) is True

    monkeypatch.setenv("HEIMDALL_ENABLED", "false")
    assert heimdall_enabled(default=True) is False


def test_settings_from_env(monkeypatch):
    monkeypatch.setenv("HEIMDALL_BLOCKED_NETWORKS", "203.0.113.0/24,198.51.100.0/24")
    monkeypatch.setenv("HEIMDALL_TRUSTED_PROXIES", "127.0.0.1")
    monkeypatch.setenv("HEIMDALL_SENSITIVE_FIELDS", "password,token,cpf")
    monkeypatch.setenv("HEIMDALL_RATE_LIMIT_REQUESTS", "40")
    monkeypatch.setenv("HEIMDALL_RATE_LIMIT_WINDOW_SECONDS", "120")

    settings = settings_from_env()

    assert settings.blocked_networks == {"203.0.113.0/24", "198.51.100.0/24"}
    assert settings.trusted_proxies == {"127.0.0.1"}
    assert "cpf" in settings.sensitive_fields
    assert settings.rate_limit.requests == 40
    assert settings.rate_limit.window_seconds == 120


def test_attach_heimdall_registers_middleware(monkeypatch):
    monkeypatch.setenv("HEIMDALL_ENABLED", "true")

    app = FastAPI()
    attached = attach_heimdall(app, service_name="test-service")

    assert attached is True
    assert any(item.cls.__name__ == "HeimdallMiddleware" for item in app.user_middleware)
