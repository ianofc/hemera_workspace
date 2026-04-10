from fastapi import APIRouter, Depends
from app.db.session import get_db
from app.db.repositories.search_repository import SearchRepository
from app.engines.sara.encoders import sara_encoder
from app.engines.thalamus.filters import ThalamusFilter
from pydantic import BaseModel

router = APIRouter()
thalamus = ThalamusFilter()

class SearchRequest(BaseModel):
    query: str
    user_id: str
    context: str = "GLOBAL_SEARCH"
    limit: int = 10

@router.post("/")
async def search_vibe(req: SearchRequest, db=Depends(get_db)):
    repo = SearchRepository(db)
    
    # 1. Transforma a pesquisa em vetor (SARA)
    query_vector = sara_encoder.encode(req.query)
    
    # 2. Busca os conteúdos mais próximos no Supabase
    raw_results = await repo.semantic_search(query_vector, limit=req.limit * 2)
    
    # Converter para formato de dicionário para o Thalamus
    candidates = [
        {"id": r.id, "title": r.title, "tags": r.tags, "safety": r.safety_label, "author_id": r.author_id}
        for r in raw_results
    ]
    
    # 3. Thalamus aplica a soberania (remove bloqueados e ilegais)
    # Por agora usamos perfil vazio, mas o Thalamus já faz o seu trabalho
    filtered_results = await thalamus.apply(req, candidates)
    
    return {
        "query": req.query,
        "results": filtered_results[:req.limit]
    }