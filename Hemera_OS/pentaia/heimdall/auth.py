from __future__ import annotations

import hashlib
import hmac
import re

from .config import PasswordPolicy


class PasswordGuard:
    SYMBOL_RE = re.compile(r"[^a-zA-Z0-9]")

    def __init__(self, policy: PasswordPolicy):
        self.policy = policy

    def validate(self, password: str) -> tuple[bool, list[str]]:
        errors: list[str] = []
        if len(password) < self.policy.min_length:
            errors.append(f"Senha deve ter pelo menos {self.policy.min_length} caracteres")
        if self.policy.require_upper and not any(char.isupper() for char in password):
            errors.append("Senha deve conter letra maiúscula")
        if self.policy.require_lower and not any(char.islower() for char in password):
            errors.append("Senha deve conter letra minúscula")
        if self.policy.require_digit and not any(char.isdigit() for char in password):
            errors.append("Senha deve conter número")
        if self.policy.require_symbol and not self.SYMBOL_RE.search(password):
            errors.append("Senha deve conter símbolo")
        return len(errors) == 0, errors


def hash_token(raw_token: str, salt: str) -> str:
    digest = hashlib.sha256(f"{salt}:{raw_token}".encode("utf-8")).hexdigest()
    return digest


def verify_token(raw_token: str, expected_digest: str, salt: str) -> bool:
    calculated = hash_token(raw_token, salt)
    return hmac.compare_digest(calculated, expected_digest)
