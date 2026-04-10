from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass(slots=True)
class ServiceStatus:
    component: str
    healthy: bool
    detail: str


def build_security_health(statuses: list[ServiceStatus]) -> dict:
    healthy = all(item.healthy for item in statuses)
    return {
        "service": "heimdall",
        "healthy": healthy,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "checks": [item.__dict__ for item in statuses],
    }
