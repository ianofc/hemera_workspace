from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class EndpointPolicy:
    path: str
    requires_auth: bool = True
    allows_public_get: bool = False


class EndpointGuard:
    def __init__(self, policies: list[EndpointPolicy]):
        self._map = {policy.path: policy for policy in policies}

    def verify(self, path: str, method: str, has_auth: bool) -> tuple[bool, str]:
        policy = self._map.get(path)
        if policy is None:
            return False, "Endpoint sem política registrada"
        if method.upper() == "GET" and policy.allows_public_get:
            return True, "Permitido"
        if policy.requires_auth and not has_auth:
            return False, "Autenticação obrigatória"
        return True, "Permitido"
