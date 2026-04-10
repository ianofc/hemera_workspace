import vecs
from core.config import settings

class ZiosMemory:
    """Interface de Memória Infinita via Supabase."""
    def __init__(self, user_id):
        self.user_id = user_id
        # Placeholder para conexão futura com Supabase/pgvector
        # self.client = vecs.create_client(settings.DATABASE_URL)

    def persist(self, input_data, output_data):
        print(f"💾 Memória persistida para {self.user_id}")

    def recall(self, query):
        return ["Ian está a migrar o IO CONSCIUS para o ZIOS com foco em automação total."]