import numpy as np
try:
    from sentence_transformers import SentenceTransformer
    MODEL = SentenceTransformer('all-MiniLM-L6-v2')
    print("✅ [SARA] Modelo de IA carregado.")
except Exception as e:
    print(f"⚠️ [SARA] Aviso: Falha ao carregar IA ({e}). Usando modo Fallback.")
    MODEL = None

class SaraEncoder:
    def encode(self, text: str):
        if MODEL:
            try:
                return MODEL.encode(text).tolist()
            except:
                pass
        # Fallback: Gera um vetor determinístico baseado no texto para não quebrar o banco
        return [float(ord(c)) / 1000 for c in text[:384]] + [0.0]*(384-len(text[:384]))

sara_encoder = SaraEncoder()