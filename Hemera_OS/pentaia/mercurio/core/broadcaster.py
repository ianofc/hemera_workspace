import logging

logger = logging.getLogger("mercurio")

class Broadcaster:
    def distribute(self, data):
        if not data:
            return
        
        # Aqui entra a lógica de Twilio / SendGrid / Telegram
        trends = data.get('google_trends', [])
        matches = data.get('matches', [])
        
        print("="*40)
        print("📢 MERCURIO BROADCAST REPORT")
        print(f"🔥 Top Trend Atual: {trends[0] if trends else 'Nenhum'}")
        print(f"🔗 Matches (News+Trends): {len(matches)}")
        print("="*40)
        
        if matches:
            logger.info(f"Enviando alerta de oportunidade: {matches[0]['trend']}")