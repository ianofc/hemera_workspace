from __future__ import annotations

from dataclasses import dataclass, field
from ipaddress import ip_network
from typing import Iterable


@dataclass(slots=True)
class RateLimitPolicy:
    requests: int = 100
    window_seconds: int = 60
    burst: int = 25


@dataclass(slots=True)
class PasswordPolicy:
    min_length: int = 12
    require_upper: bool = True
    require_lower: bool = True
    require_digit: bool = True
    require_symbol: bool = True


@dataclass(slots=True)
class HeimdallSettings:
    trusted_proxies: set[str] = field(default_factory=set)
    blocked_networks: set[str] = field(default_factory=lambda: {"10.0.0.0/8", "192.168.0.0/16"})
    sensitive_fields: set[str] = field(
        default_factory=lambda: {"password", "token", "authorization", "secret", "api_key"}
    )
    rate_limit: RateLimitPolicy = field(default_factory=RateLimitPolicy)
    password: PasswordPolicy = field(default_factory=PasswordPolicy)

    def normalized_blocked_networks(self) -> tuple:
        return tuple(ip_network(network) for network in sorted(self.blocked_networks))

    def with_blocked_networks(self, networks: Iterable[str]) -> "HeimdallSettings":
        clone = HeimdallSettings(
            trusted_proxies=set(self.trusted_proxies),
            blocked_networks=set(networks),
            sensitive_fields=set(self.sensitive_fields),
            rate_limit=self.rate_limit,
            password=self.password,
        )
        return clone
