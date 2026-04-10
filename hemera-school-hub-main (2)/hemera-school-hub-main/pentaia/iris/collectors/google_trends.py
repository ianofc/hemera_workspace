from pytrends.request import TrendReq
import logging

logger = logging.getLogger(__name__)

class TrendsCollector:
    def __init__(self):
        # hl='pt-BR', tz=180 define Brasil
        self.pytrends = TrendReq(hl='pt-BR', tz=180)

    def get_realtime_trends(self, country='BR'):
        """
        Pega os assuntos que estão explodindo AGORA (Realtime Search Trends)
        """
        try:
            logger.info(f"Buscando Trends em tempo real para: {country}")
            # Pega trends de tempo real
            df = self.pytrends.realtime_trending_searches(pn=country)
            
            # Converte para uma lista simples de títulos
            if not df.empty:
                return df['title'].tolist()
            return []
        except Exception as e:
            logger.error(f"Erro ao buscar trends: {e}")
            return []

    def get_daily_trends(self, country='brazil'):
        """Trends diários consolidados"""
        try:
            df = self.pytrends.trending_searches(pn=country)
            return df[0].tolist()
        except Exception as e:
            logger.error(f"Erro no daily trends: {e}")
            return []