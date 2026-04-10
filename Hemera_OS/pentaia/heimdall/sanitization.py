from __future__ import annotations

from collections.abc import Mapping, Sequence

MASK = "***"


def redact(value: object, sensitive_fields: set[str]) -> object:
    if isinstance(value, Mapping):
        return {
            key: MASK if key.lower() in sensitive_fields else redact(item, sensitive_fields)
            for key, item in value.items()
        }
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return [redact(item, sensitive_fields) for item in value]
    return value
