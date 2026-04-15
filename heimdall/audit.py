from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from .sanitization import redact


@dataclass(slots=True)
class SecurityEvent:
    event_type: str
    actor_id: str | None
    source_ip: str
    outcome: str
    details: dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class AuditLogger:
    def __init__(self, sensitive_fields: set[str]):
        self.sensitive_fields = {field.lower() for field in sensitive_fields}
        self._events: list[SecurityEvent] = []

    def log(self, event: SecurityEvent) -> None:
        safe_event = SecurityEvent(
            event_type=event.event_type,
            actor_id=event.actor_id,
            source_ip=event.source_ip,
            outcome=event.outcome,
            details=redact(event.details, self.sensitive_fields),
            timestamp=event.timestamp,
        )
        self._events.append(safe_event)

    def recent(self, limit: int = 50) -> list[SecurityEvent]:
        return self._events[-limit:]
