from collections import Counter
from datetime import datetime, timezone
import os
import re
import time
from typing import Dict, Tuple
import asyncio
from sqlalchemy import text


from app.engines.thalamus.filters import ThalamusFilter
from app.engines.sara.vector_search import SaraEngine
from app.engines.accumbens.ranker import AccumbensRanker
from app.db.repositories.content_repository import ContentRepository
from app.db.session import async_session


class RecommendationService:
    def __init__(self):
        self.thalamus = ThalamusFilter()
        self.sara = SaraEngine()
        self.accumbens = AccumbensRanker()

        # Orçamentos por estágio (ms): podem ser ajustados via env sem alterar código.
        self.budget_ms = {
            "thalamus": self._budget_from_env("TAS_BUDGET_THALAMUS_MS", 15),
            "sara": self._budget_from_env("TAS_BUDGET_SARA_MS", 45),
            "accumbens": self._budget_from_env("TAS_BUDGET_ACCUMBENS_MS", 25),
        }

    @staticmethod
    def _budget_from_env(env_name: str, default: int) -> int:
        raw_value = os.getenv(env_name)
        try:
            parsed = int(raw_value) if raw_value is not None else default
        except (TypeError, ValueError):
            return default
        return max(parsed, 1)

    @staticmethod

    def _to_hashtag(text_value: str) -> str:
        clean = re.sub(r"[^\w\s]", "", text_value or "")

        words = [w for w in clean.split() if w]
        if not words:
            return "#PentaIA"
        selected = words[:2]
        return "#" + "".join(word.capitalize() for word in selected)


    @staticmethod
    def _trend_tokens(topic: str, hashtag: str) -> Tuple[str, str]:
        hashtag_token = (hashtag or "").lstrip("#").replace("_", " ")
        topic_token = (topic or "").replace("_", " ")
        return topic_token.strip(), hashtag_token.strip()

    async def _load_bird_counts(self, topic: str, hashtag: str) -> Dict[str, int]:
        """
        Cruza tendências com tabelas do Django (`core_bird` e `core_comment`) no mesmo PostgreSQL.
        Se as tabelas não existirem/estiverem indisponíveis, retorna zeros sem quebrar o endpoint.
        """
        topic_token, hashtag_token = self._trend_tokens(topic, hashtag)
        if not topic_token and not hashtag_token:
            return {"related_posts_count": 0, "related_news_count": 0}

        post_like_terms = []
        comment_like_terms = []
        params: Dict[str, str] = {}
        if topic_token:
            post_like_terms.append("lower(b.content) LIKE lower(:topic_pattern)")
            comment_like_terms.append("lower(c.content) LIKE lower(:topic_pattern)")
            params["topic_pattern"] = f"%{topic_token}%"
        if hashtag_token:
            post_like_terms.append("lower(b.content) LIKE lower(:hashtag_pattern)")
            comment_like_terms.append("lower(c.content) LIKE lower(:hashtag_pattern)")
            params["hashtag_pattern"] = f"%#{hashtag_token}%"

        post_where_clause = " OR ".join(post_like_terms) if post_like_terms else "1=0"
        comment_where_clause = " OR ".join(comment_like_terms) if comment_like_terms else "1=0"

        posts_sql = text(f"SELECT COUNT(*) FROM core_bird b WHERE {post_where_clause}")
        comments_sql = text(
            f"""
            SELECT COUNT(*)
            FROM core_comment c
            JOIN core_bird b ON b.id = c.bird_id
            WHERE ({post_where_clause}) OR ({comment_where_clause})
            """
        )

        try:
            async with async_session() as session:
                posts_count = int((await session.execute(posts_sql, params)).scalar() or 0)
                comments_count = int((await session.execute(comments_sql, params)).scalar() or 0)
            return {
                "related_posts_count": posts_count,
                "related_news_count": comments_count,
            }
        except Exception:
            return {"related_posts_count": 0, "related_news_count": 0}

    async def get_feed(self, request):
        ids, _meta = await self.get_feed_with_meta(request)
        return ids

    async def _run_stage_with_budget(self, stage_name: str, coro, fallback):
        start = time.perf_counter()
        timeout_s = max(self.budget_ms.get(stage_name, 20), 1) / 1000
        degraded = False

        try:
            result = await asyncio.wait_for(coro, timeout=timeout_s)
        except Exception:
            result = fallback
            degraded = True

        elapsed_ms = round((time.perf_counter() - start) * 1000, 2)
        return result, {"elapsed_ms": elapsed_ms, "degraded": degraded}

    async def get_feed_with_meta(self, request):
        raw_data = []
        degraded_global = False
        try:
            async with async_session() as session:
                repo = ContentRepository(session)
                raw_objects = await repo.get_candidates()
                raw_data = [


                {
                    "id": o.id,
                    "title": o.title,
                    "tags": o.tags,
                    "safety": o.safety_label,
                    "embedding": o.embedding,
                }
                for o in raw_objects

                ]
        except Exception:
            raw_data = []
            degraded_global = True

        if not raw_data:
            raw_data = [{"id": "test_1", "title": "Tendência Global", "tags": ["politics"], "safety": "safe"}]
            degraded_global = True

        clean, thalamus_meta = await self._run_stage_with_budget(
            "thalamus",
            self.thalamus.apply(request, raw_data),
            raw_data,
        )

        aligned, sara_meta = await self._run_stage_with_budget(
            "sara",
            self.sara.align(request.user_id, clean),
            clean,
        )

        ranked_ids, accumbens_meta = await self._run_stage_with_budget(
            "accumbens",
            self.accumbens.rank(aligned),
            [str(c["id"]) for c in aligned],
        )

        meta = {
            "degraded": degraded_global or thalamus_meta["degraded"] or sara_meta["degraded"] or accumbens_meta["degraded"],
            "stage_metrics": {
                "thalamus": thalamus_meta,
                "sara": sara_meta,
                "accumbens": accumbens_meta,
            },
            "budgets_ms": self.budget_ms,
        }

        return ranked_ids, meta

    async def get_trends(self, limit: int = 10):
        raw_objects = []
        try:
            async with async_session() as session:
                repo = ContentRepository(session)
                raw_objects = await repo.get_candidates(limit=500)
        except Exception:
            raw_objects = []

        trends = []
        tag_counter = Counter()

        for content in raw_objects:
            tags = content.tags or []
            for tag in tags:
                if tag:
                    tag_counter[str(tag).strip().lower()] += 1

        top_tags = tag_counter.most_common(limit)
        prepared_trends = []
        for idx, (tag, freq) in enumerate(top_tags):
            topic = tag.replace("_", " ").title()
            hashtag = self._to_hashtag(topic)
            prepared_trends.append((idx, tag, topic, hashtag, freq))

        if prepared_trends:
            counters_by_trend = await asyncio.gather(
                *(self._load_bird_counts(topic, hashtag) for _, _, topic, hashtag, _ in prepared_trends)
            )
        else:
            counters_by_trend = []

        for (idx, tag, topic, hashtag, freq), counters in zip(prepared_trends, counters_by_trend):
            trends.append(
                {
                    "id": f"trend_{idx + 1}",
                    "topic": topic,
                    "category": "TAS",

                    "hashtag": hashtag,
                    "engagement": int(freq * 10),
                    "related_posts_count": counters["related_posts_count"],
                    "related_news_count": counters["related_news_count"],

                    "link": f"/explore?q={tag}",
                }
            )

        if not trends:
            defaults = ["Mercado Financeiro", "IA Generativa", "Brasil Tecnologia", "Esportes Ao Vivo"]
            for idx, topic in enumerate(defaults[:limit]):

                hashtag = self._to_hashtag(topic)
                counters = await self._load_bird_counts(topic, hashtag)

                trends.append(
                    {
                        "id": f"fallback_{idx + 1}",
                        "topic": topic,
                        "category": "Fallback",

                        "hashtag": hashtag,
                        "engagement": 100 - (idx * 10),
                        "related_posts_count": counters["related_posts_count"],
                        "related_news_count": counters["related_news_count"],

                        "link": f"/explore?q={topic.replace(' ', '+')}",
                    }
                )

        return {
            "trends": trends[:limit],
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "source": "TAS",
        }


recommendation_service = RecommendationService()
