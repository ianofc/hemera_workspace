from typing import Any, Dict, List, Optional

import numpy as np

from app.engines.sara.encoders import sara_encoder


class SaraEngine:
    async def align(
        self,
        user_id: str,
        candidates: List[Dict[str, Any]],
        user_vector: Optional[List[float]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Alinha candidatos pela similaridade de cosseno entre o vetor do usuário
        e o vetor de cada conteúdo. Sem aleatoriedade para manter consistência.
        """
        if user_vector:
            u_vec = np.array(user_vector, dtype=float)
        else:
            u_vec = np.array(sara_encoder.encode(user_id or "anonymous_user"), dtype=float)

        norm_u = np.linalg.norm(u_vec)

        for c in candidates:
            embedding = c.get("embedding")
            if embedding:
                c_vec = np.array(embedding, dtype=float)
            else:
                text_basis = " ".join(
                    [
                        str(c.get("title", "")),
                        " ".join(c.get("tags", []) or []),
                        str(c.get("id", "")),
                    ]
                ).strip()
                c_vec = np.array(sara_encoder.encode(text_basis or "content_fallback"), dtype=float)

            norm_c = np.linalg.norm(c_vec)

            if norm_u > 0 and norm_c > 0:
                c["sara_score"] = float(np.dot(u_vec, c_vec) / (norm_u * norm_c))
            else:
                c["sara_score"] = 0.0

        return sorted(candidates, key=lambda x: x["sara_score"], reverse=True)


sara_engine = SaraEngine()
