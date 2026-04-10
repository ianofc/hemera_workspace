from __future__ import annotations

import logging
import os

from fastapi import FastAPI

from .config import HeimdallSettings
from .middleware import HeimdallMiddleware


logger = logging.getLogger("heimdall.integration")


def _read_csv_set(raw: str | None) -> set[str]:
    if not raw:
        return set()
    return {item.strip() for item in raw.split(",") if item.strip()}


def heimdall_enabled(default: bool = True) -> bool:
    raw = os.getenv("HEIMDALL_ENABLED")
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


def settings_from_env() -> HeimdallSettings:
    settings = HeimdallSettings()

    blocked = _read_csv_set(os.getenv("HEIMDALL_BLOCKED_NETWORKS"))
    if blocked:
        settings.blocked_networks = blocked

    proxies = _read_csv_set(os.getenv("HEIMDALL_TRUSTED_PROXIES"))
    if proxies:
        settings.trusted_proxies = proxies

    sensitive = _read_csv_set(os.getenv("HEIMDALL_SENSITIVE_FIELDS"))
    if sensitive:
        settings.sensitive_fields = {field.lower() for field in sensitive}

    requests = os.getenv("HEIMDALL_RATE_LIMIT_REQUESTS")
    window = os.getenv("HEIMDALL_RATE_LIMIT_WINDOW_SECONDS")
    if requests:
        settings.rate_limit.requests = int(requests)
    if window:
        settings.rate_limit.window_seconds = int(window)

    return settings


def attach_heimdall(app: FastAPI, service_name: str, default_enabled: bool = True) -> bool:
    if not heimdall_enabled(default=default_enabled):
        logger.info("Heimdall desativado em %s", service_name)
        return False

    try:
        settings = settings_from_env()
        app.add_middleware(HeimdallMiddleware, settings=settings)
        logger.info("Heimdall ativo em %s", service_name)
        return True
    except Exception as exc:
        logger.exception("Falha ao ativar Heimdall em %s: %s", service_name, exc)
        return False
