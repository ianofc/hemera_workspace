from __future__ import annotations

from ipaddress import ip_address


PRIVATE_RANGES = (
    ("10.0.0.0", "10.255.255.255"),
    ("172.16.0.0", "172.31.255.255"),
    ("192.168.0.0", "192.168.255.255"),
)


def is_private_ip(address: str) -> bool:
    return ip_address(address).is_private


def extract_client_ip(headers: dict[str, str], remote_addr: str, trusted_proxies: set[str]) -> str:
    forward = headers.get("x-forwarded-for")
    if not forward or remote_addr not in trusted_proxies:
        return remote_addr
    first_ip = forward.split(",")[0].strip()
    return first_ip
