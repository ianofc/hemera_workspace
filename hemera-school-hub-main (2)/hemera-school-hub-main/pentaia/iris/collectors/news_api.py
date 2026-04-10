import feedparser
import logging

logger = logging.getLogger(__name__)

# Lista de fontes relevantes BR
SOURCES = {
    "g1": "https://g1.globo.com/rss/index/feed/pagina/0.xml",
    "uol": "http://rss.uol.com.br/feed/noticias.xml",
    "cnn_br": "https://www.cnnbrasil.com.br/feed/",
    "folha": "https://feeds.folha.uol.com.br/emcimadahora/rss091.xml"
}

class NewsCollector:
    def get_latest_news(self):
        all_news = []
        
        for source, url in SOURCES.items():
            try:
                logger.info(f"Lendo feed: {source}")
                feed = feedparser.parse(url)
                
                for entry in feed.entries[:5]: # Pega as 5 mais recentes de cada
                    all_news.append({
                        "source": source,
                        "title": entry.title,
                        "link": entry.link,
                        "published": getattr(entry, 'published', 'N/A')
                    })
            except Exception as e:
                logger.error(f"Erro lendo {source}: {e}")
                
        return all_news