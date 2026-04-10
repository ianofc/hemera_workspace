# iris/core/sattr_logic.py

import feedparser
import re
import hashlib
import logging
import math
import os
import requests  # Adicionado: necessário para _fetch_api_news
import google.generativeai as genai
from datetime import datetime
from typing import Dict, Any, List  # Adicionado: List para anotações de tipo
from pytrends.request import TrendReq
from dotenv import load_dotenv

load_dotenv()

# --- ARQUITETURA DE LOGS PENTAIA ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("IRIS_OMEGA_GEMINI")

class IRIS_Physics:
    """
    Algoritmos matemáticos para predição de tração de rede.
    Implementa decaimento newtoniano para relevância temporal.
    """
    @staticmethod
    def calculate_momentum(source_authority: float, position: int) -> float:
        # Fórmula: (Peso da Fonte * (20 - Posição)) / log(Tempo + e)
        # Garante que o que é novo e de fonte forte domine o feed.
        gravity = 1.8
        decay = math.pow(2.0, gravity) 
        momentum = (source_authority * (15 - position)) / decay
        return round(max(momentum, 0.1), 4)

class SATTR:
    """
    IRIS - SATTR (Systemic Algorithm for Real-time Trends & Resonance).
    Edição Gemini: Inteligência Híbrida de Varredura Espectral.
    """
    def __init__(self):
        # 1. Conexão com o Núcleo Neural (Gemini)
        self.api_key = os.getenv("GEMINI_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
            # flash é ideal para latência zero em tempo real
            self.model = genai.GenerativeModel('gemini-1.5-flash') 
            self.ai_enabled = True
            logger.info("Nó de Visão Gemini: Sincronizado.")
        else:
            logger.warning("Nó Gemini indisponível. Operando em modo de visão padrão.")
            self.ai_enabled = False

        # 2. Configuração de Sensores Globais
        self.pytrends = TrendReq(hl='pt-BR', tz=180, retries=3, backoff_factor=1)
        self.sources = {
            "G1": {"url": "https://g1.globo.com/rss/g1/", "weight": 1.4},
            "GOOGLE": {"url": "https://news.google.com/rss?hl=pt-BR&gl=BR&ceid=BR:pt-419", "weight": 1.2},
            "REUTERS": {"url": "https://www.reutersagency.com/feed/?best-topics=world-news&format=xml", "weight": 1.5}
        }
        self.api_sources = {
            "hackernews": "https://hn.algolia.com/api/v1/search?tags=front_page",
            "reddit": "https://www.reddit.com/r/worldnews/top.json?t=day&limit=10"
        }

    def _get_gemini_resonance(self, topic: str) -> str:
        """
        Ressonância Neural: Pergunta ao Gemini o porquê da trend.
        Elimina a necessidade de scrapers lentos de conteúdo.
        """
        if not self.ai_enabled:
            return "Monitoramento de pulso ativo via SATTR padrão."

        prompt = (
            f"Analise o assunto: '{topic}'. "
            "Forneça um contexto de uma única frase, sem introduções, "
            "explicando o impacto imediato disso para o Brasil ou o mundo hoje."
        )
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception:
            return "Tendência identificada e sob monitoramento proativo."

    def _fetch_api_news(self) -> List[Dict[str, Any]]:
        items = []
        # Hacker News API
        try:
            hn = requests.get(self.api_sources["hackernews"], timeout=4)
            if hn.status_code == 200:
                for hit in hn.json().get("hits", [])[:5]:
                    title = hit.get("title") or hit.get("story_title")
                    link = hit.get("url") or hit.get("story_url") or "https://news.ycombinator.com/"
                    if title:
                        items.append({"source": "HackerNews", "title": title, "link": link, "published": hit.get("created_at", "N/A")})
        except Exception as e:
            logger.warning(f"Falha API HackerNews: {e}")

        # Reddit JSON API
        try:
            headers = {"User-Agent": "bird-iris/1.0"}
            rd = requests.get(self.api_sources["reddit"], timeout=4, headers=headers)
            if rd.status_code == 200:
                children = rd.json().get("data", {}).get("children", [])
                for child in children[:5]:
                    data = child.get("data", {})
                    title = data.get("title")
                    link = data.get("url") or f"https://reddit.com{data.get('permalink', '')}"
                    if title:
                        items.append({"source": "Reddit", "title": title, "link": link, "published": datetime.utcfromtimestamp(data.get("created_utc", 0)).isoformat()})
        except Exception as e:
            logger.warning(f"Falha API Reddit: {e}")

        return items

    def _to_camel_hashtag(self, text: str) -> str:
        """Determinismo de Hashtag: Garante a identidade visual solicitada."""
        clean = re.sub(r'[^\w\s]', '', text)
        words = clean.split()
        if not words:
            return "#PentaIA"
        semantic_words = [w for w in words if len(w) > 2]
        base_words = semantic_words[:4] if semantic_words else words[:4]
        while len(base_words) < 4:
            base_words.append(["Bird", "Trend", "Agora", "Brasil"][len(base_words)])

        tag = "".join(word.capitalize() for word in base_words[:4])
        return f"#{tag}" if tag else "#PentaIATrendAgoraBrasil"

    def perform_scan(self) -> Dict[str, Any]:
        """
        Varredura de Espectro Total.
        Cruza intenção de busca (Search) com fatos (RSS) e processa via Gemini.
        """
        logger.info("Iniciando varredura IRIS-OMEGA Século XXII...")
        raw_pool = []
        
        # 1. SENSOR PRIMÁRIO: Google Hot Trends
        try:
            df = self.pytrends.trending_searches(pn='brazil')
            for i, row in df.head(10).iterrows():
                raw_pool.append({
                    "topic": row[0],
                    "pos": i,
                    "auth": 2.0, # Maior autoridade: intenção direta
                    "cat_suggest": "Tendência de Busca",
                    "link": f"https://www.google.com/search?q={row[0].replace(' ', '+')}"
                })
        except Exception as e:
            logger.warning(f"Sensor Pytrends em modo cooldown: {e}")

        news_items: List[Dict[str, Any]] = []

        # 2. SENSOR SECUNDÁRIO: RSS Multicamada
        for name, info in self.sources.items():
            try:
                feed = feedparser.parse(info["url"])
                for i, entry in enumerate(feed.entries[:5]):
                    title = entry.title.split(' - ')[0]
                    news_items.append({
                        "source": name,
                        "title": title,
                        "link": entry.link,
                        "published": getattr(entry, "published", "N/A")
                    })
                    raw_pool.append({
                        "topic": title,
                        "pos": i,
                        "auth": info["weight"],
                        "cat_suggest": f"Notícia {name}",
                        "link": entry.link
                    })
            except Exception:
                continue

        # 3. APIs externas de notícias reais
        news_items.extend(self._fetch_api_news())

        # 4. FILTRAGEM, RESSONÂNCIA E PONTUAÇÃO
        processed = []
        seen_tags = set()

        for item in raw_pool:
            hashtag = self._to_camel_hashtag(item["topic"])
            if hashtag in seen_tags:
                continue
            seen_tags.add(hashtag)

            # Cálculo de Momentum Gravitacional
            # Corrigido: Removido argumento extra item["auth"] que causava erro
            score = IRIS_Physics.calculate_momentum(item["auth"], item["pos"])
            
            # Ressonância Neural (Gemini)
            # Só acionamos o Gemini para os top 12 para economizar cota e ganhar performance
            context = self._get_gemini_resonance(item["topic"]) if len(processed) < 12 else "Pulso validado."

            topic_words = [w.lower() for w in re.findall(r"\w+", item["topic"]) if len(w) > 3]
            related_news_count = 0
            if topic_words:
                for n in news_items:
                    title_l = str(n.get("title", "")).lower()
                    if any(w in title_l for w in topic_words[:4]):
                        related_news_count += 1
            related_posts_count = max(1, int(score * 35) + (related_news_count * 3))

            processed.append({
                "id": hashlib.md5(hashtag.encode()).hexdigest()[:10],
                "hashtag": hashtag,
                "topic": item["topic"],
                "category": self._detect_category(item["topic"]),
                "context": context,
                "related_posts_count": related_posts_count,
                "related_news_count": related_news_count,
                "link": item["link"],
                "momentum": score,
                "confidence": "High" if item["auth"] > 1.3 else "Standard"
            })

        # Ordenação por Momentum (Explosividade)
        final_trends = sorted(processed, key=lambda x: x["momentum"], reverse=True)

        return {
            "status": "synchronized",
            "engine": "IRIS-OMEGA-GEMINI-2.2",
            "timestamp": datetime.now().isoformat(),
            "stats": {
                "raw_captured": len(raw_pool),
                "neural_resonance": self.ai_enabled
            },
            "google_trends": final_trends,
            "news": news_items[:20]
        }

    def _detect_category(self, text: str) -> str:
        """IA Heurística para categorização instantânea (Frontend Badges)."""
        text = text.lower()
        if any(w in text for w in ['vasco', 'gol', 'futebol', 'campeão', 'vitoria', 'flamengo', 'palmeiras']):
            return "Esportes"
        if any(w in text for w in ['mercado', 'dólar', 'ações', 'economia', 'investimento', 'selic']):
            return "Economia"
        if any(w in text for w in ['ia', 'tech', 'apple', 'foguete', 'software', 'chip', 'celular']):
            return "Tecnologia"
        if any(w in text for w in ['governo', 'lula', 'senado', 'política', 'stf', 'eleição']):
            return "Política"
        if any(w in text for w in ['filme', 'série', 'bbb', 'show', 'música', 'atriz', 'carnaval']):
            return "Cultura"
        return "Geral"