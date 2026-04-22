import numpy as np
class SaraEngine:
    async def align(self, user_id, candidates, user_vector=None):
        """
        Alinha candidatos usando o vetor de interesse real do utilizador.
        Se o utilizador não tem vetor, usamos um neutro.
        """
        # Se não houver vetor de interesse, geramos um neutro
        u_vec = np.array(user_vector) if user_vector else np.random.rand(384)
        
        for c in candidates:
            # Recupera o embedding que salvamos no Supabase durante a ingestão
            c_vec = np.array(c.get("embedding", np.random.rand(384)))
            
            # Cálculo de Similaridade de Cosseno (Afinidade Pura)
            norm_u = np.linalg.norm(u_vec)
            norm_c = np.linalg.norm(c_vec)
            
            if norm_u > 0 and norm_c > 0:
                c["sara_score"] = float(np.dot(u_vec, c_vec) / (norm_u * norm_c))
            else:
                c["sara_score"] = 0.5
                
        return sorted(candidates, key=lambda x: x["sara_score"], reverse=True)

sara_engine = SaraEngine()