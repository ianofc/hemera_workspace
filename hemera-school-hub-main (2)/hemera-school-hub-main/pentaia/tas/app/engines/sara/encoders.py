import hashlib
from typing import List

import numpy as np

VECTOR_SIZE = 384

try:
    from sentence_transformers import SentenceTransformer

    MODEL = SentenceTransformer("all-MiniLM-L6-v2")
    print("✅ [SARA] Modelo de IA carregado.")
except Exception as e:
    print(f"⚠️ [SARA] Aviso: Falha ao carregar IA ({e}). Usando modo Fallback determinístico.")
    MODEL = None


class SaraEncoder:
    def _deterministic_vector(self, text: str) -> List[float]:
        seed = int(hashlib.sha256(text.encode("utf-8")).hexdigest(), 16) % (2**32)
        rng = np.random.default_rng(seed)
        return rng.random(VECTOR_SIZE).astype(float).tolist()

    def encode(self, text: str) -> List[float]:
        payload = (text or "").strip()
        if MODEL and payload:
            try:
                return MODEL.encode(payload).tolist()
            except Exception:
                pass
        return self._deterministic_vector(payload or "SARA_FALLBACK")


sara_encoder = SaraEncoder()
