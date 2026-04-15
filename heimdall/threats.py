from __future__ import annotations

from dataclasses import dataclass
from ipaddress import ip_address, ip_network


@dataclass(slots=True)
class ThreatVerdict:
    allowed: bool
    reason: str


class ThreatDetector:
    def __init__(self, blocked_networks: tuple):
        self.blocked_networks = blocked_networks

    def evaluate_ip(self, address: str) -> ThreatVerdict:
        client_ip = ip_address(address)
        for network in self.blocked_networks:
            if client_ip in network:
                return ThreatVerdict(False, f"IP bloqueado pela rede {network}")
        return ThreatVerdict(True, "IP permitido")

    @classmethod
    def from_cidrs(cls, cidrs: set[str]) -> "ThreatDetector":
        return cls(tuple(ip_network(cidr) for cidr in sorted(cidrs)))
