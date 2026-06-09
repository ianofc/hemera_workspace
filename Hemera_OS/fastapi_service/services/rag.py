# fastapi_service/services/rag.py
import os
import re
import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger("hemera.rag")

STOPWORDS = {
    "de", "do", "da", "em", "um", "uma", "o", "a", "os", "as", "e", "ou",
    "para", "com", "por", "que", "na", "no", "nas", "nos", "se", "como",
    "dos", "das", "sobre", "entre", "sob", "para", "atras", "com", "contra"
}

class Chunk:
    def __init__(self, source: str, page: int, content: str):
        self.source = source
        self.page = page
        self.content = content

    def to_dict(self) -> Dict[str, Any]:
        return {
            "documento": self.source,
            "pagina": self.page,
            "trecho": self.content.strip()
        }

class RAGEngine:
    def __init__(self, data_dir: Optional[str] = None):
        if data_dir is None:
            # Caminho padrão relativo ao arquivo hemeralm_service ou fastapi_service
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            data_dir = os.path.join(base_dir, "data")
        
        self.data_dir = data_dir
        self.chunks: List[Chunk] = []
        self.load_documents()

    def load_documents(self):
        self.chunks = []
        if not os.path.exists(self.data_dir):
            logger.warning(f"Diretório de dados RAG não encontrado em: {self.data_dir}")
            return

        for filename in os.listdir(self.data_dir):
            if filename.endswith(".txt"):
                filepath = os.path.join(self.data_dir, filename)
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        content = f.read()
                        self._parse_and_add_chunks(content)
                except Exception as e:
                    logger.error(f"Erro ao ler arquivo {filepath}: {str(e)}")
        
        logger.info(f"RAG carregado com {len(self.chunks)} chunks de conhecimento.")

    def _parse_and_add_chunks(self, text: str):
        # Expressão regular para capturar o cabeçalho [SOURCE: ..., PAGE: ...]
        pattern = r"\[SOURCE:\s*(.*?),\s*PAGE:\s*(\d+)\]"
        matches = list(re.finditer(pattern, text))
        
        for i, match in enumerate(matches):
            source = match.group(1).strip()
            page = int(match.group(2).strip())
            
            # O conteúdo vai do fim deste match até o início do próximo match (ou até o fim do texto)
            start_pos = match.end()
            end_pos = matches[i + 1].start() if i + 1 < len(matches) else len(text)
            
            content = text[start_pos:end_pos].strip()
            if content:
                self.chunks.append(Chunk(source=source, page=page, content=content))

    def _tokenize(self, text: str) -> List[str]:
        # Limpa pontuações simples e separa em minúsculas
        text_clean = re.sub(r"[^\w\s-]", "", text.lower())
        tokens = text_clean.split()
        return [t for t in tokens if t not in STOPWORDS and len(t) > 1]

    def retrieve(self, query: str, limit: int = 3) -> List[Chunk]:
        """
        Retorna os trechos mais relevantes com base em busca textual ponderada.
        """
        query_tokens = self._tokenize(query)
        if not query_tokens:
            # Se não houver palavras-chave válidas na busca, retorna os primeiros chunks
            return self.chunks[:limit]

        scored_chunks = []
        for chunk in self.chunks:
            score = 0.0
            content_lower = chunk.content.lower()
            source_lower = chunk.source.lower()
            
            chunk_tokens = self._tokenize(chunk.content)
            
            for token in query_tokens:
                # Palavra exata no conteúdo
                if token in chunk_tokens:
                    # Frequência simples
                    count = content_lower.count(token)
                    score += 1.0 + (0.2 * count)
                # Palavra-chave no título da fonte (dar mais relevância)
                if token in source_lower:
                    score += 2.0
            
            if score > 0:
                scored_chunks.append((score, chunk))

        # Ordenar por pontuação decrescente
        scored_chunks.sort(key=lambda x: x[0], reverse=True)
        
        results = [chunk for score, chunk in scored_chunks[:limit]]
        
        # Se não houver nenhum match de palavra-chave, retorna uma lista padrão (opcional) ou vazia
        if not results:
            # Retorna alguns chunks de fallback ou lista vazia para indicar 'sem correspondência'
            # Vamos preferir retornar vazio para que o modelo informe que a informação não foi encontrada nas fontes
            return []
            
        return results

# Instância Singleton do mecanismo RAG
rag_engine = RAGEngine()
