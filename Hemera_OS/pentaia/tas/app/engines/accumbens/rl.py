import logging
from typing import Dict, List, Any
from sqlalchemy.future import select
from app.db.session import async_session
from app.db.base_user import UserProfileModel

logger = logging.getLogger("ACCUMBENS_RL")


class AccumbensRL:
    def __init__(self, learning_rate: float = 0.15):
        self.learning_rate = learning_rate
        # Escalonamento de recompensas (Dopamine Weights)
        self.rewards = {
            "click": 1.0,
            "like": 3.0,
            "comment": 6.0,
            "share": 12.0,
            "boredom": -5.0,  # Penalidade de tédio
            "skip": -3.0
        }
        # Fallback local na RAM caso o banco esteja inacessível
        self.memory_fallback_profiles: Dict[str, Dict[str, float]] = {}

    def get_fallback_interests(self, user_id: str) -> Dict[str, float]:
        return self.memory_fallback_profiles.get(user_id, {})

    async def update_user_preferences(self, user_id: str, tags: List[str], action: str):
        """
        Recebe a ação de interação do usuário, calcula a recompensa (dopamine weight) 
        e atualiza os pesos das tags no perfil de prioridades do usuário.
        """
        reward = self.rewards.get(action.lower(), 0.0)
        if reward == 0.0 or not tags:
            return

        # 1. Tenta atualizar via PostgreSQL
        try:
            async with async_session() as session:
                result = await session.execute(select(UserProfileModel).filter_by(user_id=user_id))
                profile = result.scalars().first()

                if not profile:
                    profile = UserProfileModel(
                        user_id=user_id,
                        blacklisted_tags=[],
                        blacklisted_authors=[],
                        priority_interests={}
                    )
                    session.add(profile)

                interests = profile.priority_interests or {}
                if not isinstance(interests, dict):
                    interests = {}

                # Atualiza pesos para as tags informadas
                for tag in tags:
                    tag_clean = tag.strip().lower()
                    current_weight = float(interests.get(tag_clean, 0.0))
                    new_weight = current_weight + self.learning_rate * reward
                    interests[tag_clean] = round(max(-10.0, min(20.0, new_weight)), 3)

                profile.priority_interests = interests
                session.add(profile)
                await session.commit()
                logger.info(f"🧠 [ACCUMBENS RL] DB atualizado. Usuário {user_id} -> {action} em tags {tags}. Recompensa: {reward}")
                return
        except Exception as e:
            logger.warning(f"⚠️ [ACCUMBENS RL] Falha ao gravar no DB ({e}). Salvando em cache de fallback na memória.")

        # 2. Fallback: Grava em RAM local
        interests = self.memory_fallback_profiles.setdefault(user_id, {})
        for tag in tags:
            tag_clean = tag.strip().lower()
            current_weight = interests.get(tag_clean, 0.0)
            new_weight = current_weight + self.learning_rate * reward
            interests[tag_clean] = round(max(-10.0, min(20.0, new_weight)), 3)
            
        logger.info(f"🧠 [ACCUMBENS RL MEMORY] RAM atualizada. Usuário {user_id} -> {action} em tags {tags}.")


accumbens_rl = AccumbensRL()


# Handler de evento na fila assíncrona do Talamus
async def process_feedback_event(event: Dict[str, Any]):
    """
    Consome eventos da fila de entrada do Talamus. Se for um evento de interação 
    (ex: clique, like, share), atualiza o aprendizado por reforço do Accumbens.
    """
    event_type = event.get("event_type") or event.get("action")
    user_id = event.get("user_id")
    tags = event.get("tags") or []
    
    if event_type and user_id and tags:
        # Se for uma ação válida, repassa para o aprendizado por reforço do Accumbens
        if event_type.lower() in accumbens_rl.rewards:
            await accumbens_rl.update_user_preferences(user_id, tags, event_type)
