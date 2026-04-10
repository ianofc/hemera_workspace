from zios.core.brain import ZiosBrain
import logging

logger = logging.getLogger(__name__)

def chat_com_zios(user_data, context='ONBOARDING'):
    """
    ZIOS: O sucessor soberano do Zios.
    Atua como GPS Cognitivo, Amigo e Mentor.
    Responsável pelo batismo de identidade (IO ID) no MultiVerso.
    """
    try:
        brain = ZiosBrain()
        username = user_data.get('username', 'Viajante')
        
        # O Zios não apenas registra, ele inicia a Memória Episódica
        prompt = (
            f"O usuário {username} acaba de despertar no MultiVerso. "
            "Atue como seu Mentor Proativo. Dê as boas-vindas ao Life OS. "
            "Explique que você cuidará da burocracia no background enquanto ele foca no YourLife e Lumenios."
        )
        
        return brain.process(prompt, context=context)
    except Exception as e:
        logger.error(f"Zios Guardian offline: {e}")
        return "Zios está monitorando seu progresso. Bem-vindo ao ecossistema de elite."