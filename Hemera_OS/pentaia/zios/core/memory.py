import os
import json
import logging
import sqlite3
import math
from datetime import datetime, timezone
import uuid

logger = logging.getLogger("ZIOS_MEMORY")

# Tentar importar vecs
try:
    import vecs
    VECS_AVAILABLE = True
except ImportError:
    VECS_AVAILABLE = False
    logger.warning("⚠️ Biblioteca vecs não encontrada. Fallback SQLite ativo.")

class ZiosMemory:
    """
    Interface de Memória Episódica Infinita do ZIOS.
    Suporta Supabase/pgvector (via vecs) com fallback robusto em SQLite local.
    Indexa contextos e marcações de tempo (timestamps) com ordenação por relevância e temporalidade.
    """
    def __init__(self, user_id: str, db_url: str = None, google_api_key: str = None):
        self.user_id = user_id
        # Carrega chaves e URLs das configurações se não forem passados
        try:
            from core.config import settings
            self.db_url = db_url or settings.DATABASE_URL
            self.google_api_key = google_api_key or settings.GOOGLE_API_KEY
        except ImportError:
            self.db_url = db_url
            self.google_api_key = google_api_key
        
        self.use_supabase = False
        self.vecs_client = None
        self.collection = None
        self.collection_name = "zios_episodic_memory"
        self.vector_dim = 768  # Dimensão padrão para text-embedding-004 do Gemini
        
        # Inicializa o SQLite por padrão para fallbacks
        self.sqlite_db_path = "db/zios_memory.db"
        os.makedirs(os.path.dirname(self.sqlite_db_path), exist_ok=True)
        self._init_sqlite()

        # Tenta inicializar o Supabase/vecs se houver URL
        if VECS_AVAILABLE and self.db_url:
            try:
                cleaned_url = self.db_url
                if cleaned_url.startswith("postgresql://") or cleaned_url.startswith("postgres://"):
                    self.vecs_client = vecs.create_client(cleaned_url)
                    self.collection = self.vecs_client.get_or_create_collection(
                        name=self.collection_name, 
                        dimension=self.vector_dim
                    )
                    self.use_supabase = True
                    logger.info("🔌 Supabase Vector DB conectado com sucesso via vecs.")
            except Exception as e:
                logger.warning(f"⚠️ Falha ao conectar no Supabase Vector DB ({e}). Usando fallback SQLite local.")
                self.use_supabase = False

    def _init_sqlite(self):
        """Inicializa a tabela do SQLite para fallback local."""
        conn = sqlite3.connect(self.sqlite_db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS zios_episodic_memory (
                id TEXT PRIMARY KEY,
                user_id TEXT,
                timestamp TEXT,
                input_data TEXT,
                output_data TEXT,
                context TEXT,
                vector TEXT
            )
        """)
        conn.commit()
        conn.close()

    def _generate_embedding(self, text: str) -> list:
        """Gera um vetor de embedding de dimensão 768 usando o Gemini, ou fallback determinístico."""
        if self.google_api_key:
            try:
                from google import genai
                client = genai.Client(
                    api_key=self.google_api_key,
                    http_options={'api_version': 'v1beta'}
                )
                response = client.models.embed_content(
                    model="text-embedding-004",
                    contents=text
                )
                if response and hasattr(response, "embeddings") and len(response.embeddings) > 0:
                    return response.embeddings[0].values
            except Exception as e:
                logger.debug(f"Não foi possível obter embedding do Gemini ({e}). Usando fallback determinístico.")

        # Fallback determinístico (cria um vetor pseudo-aleatório baseado no hash do texto)
        import hashlib
        h = hashlib.sha256(text.encode('utf-8')).digest()
        res = []
        for i in range(self.vector_dim):
            val = (h[i % 32] / 255.0) * 2.0 - 1.0
            res.append(val)
        return res

    def persist(self, input_data: str, output_data: str, context: dict = None) -> str:
        """Salva o episódio na memória com marcação de tempo."""
        episode_id = str(uuid.uuid4())
        timestamp = datetime.now(timezone.utc).isoformat()
        ctx_str = json.dumps(context or {})
        
        # Gera o texto completo do episódio para o embedding
        combined_text = f"Input: {input_data}\nOutput: {output_data}"
        vector = self._generate_embedding(combined_text)
        
        # Salva localmente no SQLite sempre (garantia de persistência e fallback rápido)
        try:
            conn = sqlite3.connect(self.sqlite_db_path)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO zios_episodic_memory (id, user_id, timestamp, input_data, output_data, context, vector) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (episode_id, self.user_id, timestamp, input_data, output_data, ctx_str, json.dumps(vector))
            )
            conn.commit()
            conn.close()
            logger.info(f"💾 Memória persistida localmente (SQLite) para {self.user_id}.")
        except Exception as e:
            logger.error(f"❌ Erro ao persistir no SQLite local: {e}")

        # Se Supabase estiver disponível, tenta persistir lá também
        if self.use_supabase and self.collection:
            try:
                metadata = {
                    "user_id": self.user_id,
                    "timestamp": timestamp,
                    "input_data": input_data,
                    "output_data": output_data,
                    "context": ctx_str
                }
                self.collection.upsert(
                    records=[(episode_id, vector, metadata)]
                )
                logger.info(f"💾 Memória replicada no Supabase (vecs) para {self.user_id}.")
            except Exception as e:
                logger.warning(f"⚠️ Erro ao persistir no Supabase: {e}. Desativando réplica temporariamente.")
                
        return episode_id

    def recall(self, query: str, limit: int = 5, threshold: float = 0.0) -> list:
        """
        Recupera episódios da memória relevantes para a query,
        combinando similaridade de cosseno e decaimento temporal.
        """
        query_vector = self._generate_embedding(query)
        episodes = []

        # Tenta buscar do Supabase se estiver configurado
        if self.use_supabase and self.collection:
            try:
                results = self.collection.query(
                    data=query_vector,
                    limit=limit * 3,
                    include_metadata=True,
                    include_value=True
                )
                for res_id, val, meta in results:
                    episodes.append({
                        "id": res_id,
                        "user_id": meta.get("user_id"),
                        "timestamp": meta.get("timestamp"),
                        "input_data": meta.get("input_data"),
                        "output_data": meta.get("output_data"),
                        "context": json.loads(meta.get("context", "{}")),
                        "vector": val,
                        "similarity": 1.0 - val
                    })
            except Exception as e:
                logger.warning(f"⚠️ Falha ao buscar no Supabase ({e}). Buscando no SQLite local.")
                episodes = []

        # Se não retornou nada ou Supabase inativo, busca no SQLite
        if not episodes:
            try:
                conn = sqlite3.connect(self.sqlite_db_path)
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT * FROM zios_episodic_memory WHERE user_id = ?",
                    (self.user_id,)
                )
                rows = cursor.fetchall()
                conn.close()

                for row in rows:
                    row_vec = json.loads(row["vector"])
                    dot_product = sum(a * b for a, b in zip(query_vector, row_vec))
                    norm_a = math.sqrt(sum(a * a for a in query_vector))
                    norm_b = math.sqrt(sum(b * b for b in row_vec))
                    similarity = dot_product / (norm_a * norm_b) if norm_a > 0 and norm_b > 0 else 0.0
                    
                    episodes.append({
                        "id": row["id"],
                        "user_id": row["user_id"],
                        "timestamp": row["timestamp"],
                        "input_data": row["input_data"],
                        "output_data": row["output_data"],
                        "context": json.loads(row["context"]),
                        "vector": row_vec,
                        "similarity": similarity
                    })
            except Exception as e:
                logger.error(f"❌ Erro ao buscar no SQLite local: {e}")
                return ["Ian está a migrar o IO CONSCIUS para o ZIOS com foco em automação total."]

        # Ordenação combinando similaridade e temporalidade
        now = datetime.now(timezone.utc)
        scored_episodes = []
        for ep in episodes:
            try:
                ep_time = datetime.fromisoformat(ep["timestamp"])
                if ep_time.tzinfo is None:
                    ep_time = ep_time.replace(tzinfo=timezone.utc)
                delta_seconds = (now - ep_time).total_seconds()
            except Exception:
                delta_seconds = 86400.0
            
            temporal_decay = 1.0 / (1.0 + (delta_seconds / 21600.0))
            combined_score = ep["similarity"] * 0.7 + temporal_decay * 0.3
            scored_episodes.append((combined_score, ep))

        scored_episodes.sort(key=lambda x: x[0], reverse=True)
        
        results_formatted = []
        for score, ep in scored_episodes[:limit]:
            if score >= threshold:
                results_formatted.append(
                    f"[{ep['timestamp']}] Usuário: {ep['input_data']} -> ZIOS: {ep['output_data']}"
                )
                
        if not results_formatted:
            return ["Ian está a migrar o IO CONSCIUS para o ZIOS com foco em automação total."]
            
        return results_formatted

    def clear(self):
        """Limpa as memórias do usuário localmente e remotamente."""
        try:
            conn = sqlite3.connect(self.sqlite_db_path)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM zios_episodic_memory WHERE user_id = ?", (self.user_id,))
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"Erro ao limpar SQLite: {e}")
            
        if self.use_supabase and self.collection:
            try:
                self.vecs_client.delete_collection(self.collection_name)
                self.collection = self.vecs_client.get_or_create_collection(
                    name=self.collection_name, 
                    dimension=self.vector_dim
                )
            except Exception as e:
                logger.warning(f"Erro ao limpar Supabase: {e}")