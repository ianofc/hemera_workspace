from sqlalchemy import text
from app.db.base import ContentModel
import json

class SearchRepository:
    def __init__(self, db_session):
        self.db = db_session

    async def semantic_search(self, query_vector, limit=10):
        """
        Executa busca por similaridade de cosseno diretamente no SQL.
        Nota: O pgvector no Supabase usa o operador <=> para distância de cosseno.
        """
        # Transformamos o vetor em string para o SQL
        vector_str = str(query_vector)
        
        # Query otimizada para buscar os mais próximos
        query = text(f"""
            SELECT id, title, tags, safety_label, author_id, embedding
            FROM contents
            ORDER BY embedding::jsonb <=> :vector::jsonb
            LIMIT :limit
        """)
        
        result = await self.db.execute(query, {"vector": vector_str, "limit": limit})
        return result.fetchall()