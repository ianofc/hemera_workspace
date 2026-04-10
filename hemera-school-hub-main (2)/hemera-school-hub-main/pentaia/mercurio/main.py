from datetime import datetime
import hashlib
import logging
import time
from typing import Any, Dict, List

import requests
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from core.config import (
    CORS_ALLOW_ORIGINS,
    HEIMDALL_CHECK_URL,
    IRIS_SCAN_URL,
    MERCURIO_BUNDLE_CACHE_TTL_S,
    MERCURIO_CIRCUIT_COOLDOWN_S,
    MERCURIO_CIRCUIT_FAILURE_LIMIT,
    MERCURIO_TOPIC_ALIASES,
    MERCURIO_WEIGHT_API,
    MERCURIO_WEIGHT_BIRD,
    MERCURIO_WEIGHT_RSS,
    REQUEST_TIMEOUT_DEFAULT,
    SERVICE_NAME,
    SERVICE_PORT,
    TAS_TRENDS_URL,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | MERCURIO: %(message)s")
logger = logging.getLogger("MERCURIO_HUB")

app = FastAPI(title="MERCÚRIO - Broadcaster Hub PentaIA", version="1.5.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ALLOW_ORIGINS or ["http://localhost:8080", "http://127.0.0.1:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


BUNDLE_CACHE: Dict[str, Any] = {"expires_at": 0.0, "payload": None}
SOURCE_STATE: Dict[str, Dict[str, float]] = {
    "tas": {"failures": 0.0, "cooldown_until": 0.0},
    "iris": {"failures": 0.0, "cooldown_until": 0.0},
}


def _normalize_slug(text: str) -> str:
    raw = (text or "").lower().strip()
    ascii_like = raw.encode("ascii", errors="ignore").decode("ascii")
    slug = "".join(ch if ch.isalnum() or ch in {"-", "_", " ", "#"} else " " for ch in ascii_like)
    return "-".join(slug.replace("#", "").split())


def _build_topic_alias_map() -> Dict[str, str]:
    aliases: Dict[str, str] = {}
    for block in [item.strip() for item in MERCURIO_TOPIC_ALIASES.split(";") if item.strip()]:
        if ":" not in block:
            continue
        canonical, variants_raw = block.split(":", 1)
        canonical_slug = _normalize_slug(canonical)
        if not canonical_slug:
            continue
        aliases[canonical_slug] = canonical_slug
        for variant in [v.strip() for v in variants_raw.split(",") if v.strip()]:
            aliases[_normalize_slug(variant)] = canonical_slug
    return aliases


TOPIC_ALIAS_MAP = _build_topic_alias_map()


def _canonical_topic_key(trend: Dict[str, Any]) -> str:
    hashtag = _normalize_slug(str(trend.get("hashtag", "")))
    topic = _normalize_slug(str(trend.get("topic", "")))
    key = hashtag or topic
    if not key:
        return "unknown-topic"
    return TOPIC_ALIAS_MAP.get(key, key)


def _topic_path_for_tag(hashtag: str) -> str:
    return f"/mercurio/topico/{_normalize_slug(hashtag)}"


def _build_bird_signal(seed_text: str) -> Dict[str, Any]:
    seed = int(hashlib.sha256(seed_text.encode("utf-8")).hexdigest(), 16)
    posts = 20 + (seed % 380)
    comments = int(posts * 2.4)
    return {
        "posts_count": posts,
        "comments_count": comments,
        "hotspots": ["/mercurio", "/mercurio/topico", "/feed"],
        "top_authors": [
            f"@trend_{(seed % 97) + 1}",
            f"@pulse_{(seed % 79) + 1}",
            f"@bird_{(seed % 53) + 1}",
        ],
    }


def _parse_numeric(value: Any) -> float:
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        cleaned = value.replace(".", "").replace(",", ".")
        digits = "".join(ch for ch in cleaned if ch.isdigit() or ch in {".", "-"})
        if not digits:
            return 0.0
        try:
            return float(digits)
        except ValueError:
            return 0.0
    return 0.0


def _extract_media_urls(payload: Dict[str, Any]) -> Dict[str, Any]:
    media_urls: List[str] = []

    direct_keys = [
        "image", "image_url", "thumbnail", "thumb", "photo", "photo_url",
        "cover", "cover_image", "video", "video_url", "media_url",
    ]
    list_keys = ["media", "media_urls", "images", "videos", "gallery", "attachments"]

    for key in direct_keys:
        value = payload.get(key)
        if isinstance(value, str) and value.strip():
            media_urls.append(value.strip())

    for key in list_keys:
        value = payload.get(key)
        if isinstance(value, list):
            for item in value:
                if isinstance(item, str) and item.strip():
                    media_urls.append(item.strip())
                elif isinstance(item, dict):
                    for dict_key in ("url", "src", "href", "image", "video"):
                        dict_value = item.get(dict_key)
                        if isinstance(dict_value, str) and dict_value.strip():
                            media_urls.append(dict_value.strip())

    dedup: List[str] = []
    seen = set()
    for url in media_urls:
        if url not in seen:
            seen.add(url)
            dedup.append(url)

    video_url = next((url for url in dedup if any(token in url.lower() for token in ("youtube.com", "youtu.be", "vimeo.com", ".mp4", ".webm", ".m3u8"))), "")
    image_url = next((url for url in dedup if any(token in url.lower() for token in (".jpg", ".jpeg", ".png", ".webp", ".gif", "image", "img"))), "")

    return {
        "media": dedup,
        "video_url": video_url,
        "image_url": image_url,
    }


def _infer_external_origin(data: Dict[str, Any]) -> str:
    explicit = str(data.get("origin", "")).upper().strip()
    if explicit in {"BIRD_NETWORK", "RSS", "API_NEWS"}:
        return explicit

    source = str(data.get("source", "")).lower()
    link = str(data.get("link", "")).lower()
    blob = f"{source} {link}"
    if any(token in blob for token in ("rss", "feed", "xml")):
        return "RSS"
    return "API_NEWS"


def _weight_for_origin(origin: str) -> int:
    if origin == "BIRD_NETWORK":
        return MERCURIO_WEIGHT_BIRD
    if origin == "RSS":
        return MERCURIO_WEIGHT_RSS
    if origin == "API_NEWS":
        return MERCURIO_WEIGHT_API
    return 0


def _score_trend(trend: Dict[str, Any]) -> float:
    signal = trend.get("bird_signal", {}) if isinstance(trend.get("bird_signal"), dict) else {}
    posts = _parse_numeric(signal.get("posts_count", 0))
    comments = _parse_numeric(signal.get("comments_count", 0))
    volume = _parse_numeric(trend.get("volume", 0))
    weight = _parse_numeric(trend.get("weight", 1))
    return (weight * 10_000) + (posts * 15) + (comments * 7) + volume


def _rank_weighted_trends(trends: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    if not trends:
        return []

    dedup: Dict[str, Dict[str, Any]] = {}
    for trend in trends:
        topic_key = _canonical_topic_key(trend)
        if topic_key not in dedup or _score_trend(trend) > _score_trend(dedup[topic_key]):
            dedup[topic_key] = trend

    return sorted(dedup.values(), key=_score_trend, reverse=True)


def _normalize_tas_trends(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    trends = payload.get("trends", []) if isinstance(payload, dict) else []
    normalized: List[Dict[str, Any]] = []
    for idx, trend in enumerate(trends):
        hashtag = trend.get("hashtag") or f"#trend_{idx + 1}"
        if not str(hashtag).startswith("#"):
            hashtag = f"#{hashtag}"

        topic = trend.get("topic", "Sem descrição")
        media = _extract_media_urls(trend)
        normalized.append(
            {
                "id": trend.get("id", f"tas_{idx + 1}"),
                "category": trend.get("category", "Geral"),
                "title": topic,
                "topic": topic,
                "summary": f"Assunto em alta no BIRD com foco em {topic.lower()}.",
                "source": "BIRD",
                "origin": "BIRD_NETWORK",
                "weight": _weight_for_origin("BIRD_NETWORK"),
                "hashtag": hashtag,
                "volume": trend.get("engagement", trend.get("volume", "N/A")),
                "link": trend.get("link") or _topic_path_for_tag(hashtag),
                "media": media["media"],
                "image_url": media["image_url"],
                "video_url": media["video_url"],
                "bird_signal": {
                    **_build_bird_signal(topic),
                    "posts_count": int(trend.get("related_posts_count", 0) or 0),
                    "comments_count": int(trend.get("related_news_count", 0) or 0),
                },
            }
        )
    return normalized


def _normalize_iris_trends(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    trends = payload.get("google_trends", []) if isinstance(payload, dict) else []
    normalized: List[Dict[str, Any]] = []
    for idx, trend in enumerate(trends):
        hashtag = trend.get("hashtag") or trend.get("topic") or f"trend_{idx + 1}"
        if not str(hashtag).startswith("#"):
            hashtag = f"#{hashtag}"

        topic = trend.get("topic", "Sem descrição")
        origin = _infer_external_origin(trend)
        media = _extract_media_urls(trend)
        normalized.append(
            {
                "id": trend.get("id", f"iris_{idx + 1}"),
                "category": trend.get("category", "Global"),
                "title": topic,
                "topic": topic,
                "summary": trend.get("context", "Sem resumo disponível."),
                "source": trend.get("source", trend.get("confidence", "IRIS")),
                "origin": origin,
                "weight": _weight_for_origin(origin),
                "hashtag": hashtag,
                "volume": trend.get("momentum", trend.get("volume", "N/A")),
                "link": trend.get("link") or _topic_path_for_tag(hashtag),
                "media": media["media"],
                "image_url": media["image_url"],
                "video_url": media["video_url"],
                "bird_signal": {
                    **_build_bird_signal(topic),
                    "posts_count": int(trend.get("related_posts_count", 0) or 0),
                    "comments_count": int(trend.get("related_news_count", 0) or 0),
                },
            }
        )
    return normalized


def _normalize_news_items(news_payload: Any) -> List[Dict[str, Any]]:
    if not isinstance(news_payload, list):
        return []

    normalized: List[Dict[str, Any]] = []
    for item in news_payload:
        if not isinstance(item, dict):
            continue

        source = str(item.get("source", "Mercurio"))
        link = str(item.get("link", ""))
        origin = _infer_external_origin({"origin": item.get("origin"), "source": source, "link": link})
        media = _extract_media_urls(item)
        normalized.append(
            {
                "source": source,
                "title": item.get("title", "Sem título"),
                "link": link,
                "published": item.get("published", "N/A"),
                "origin": origin,
                "weight": _weight_for_origin(origin),
                "media": media["media"],
                "image_url": media["image_url"],
                "video_url": media["video_url"],
            }
        )

    return sorted(normalized, key=lambda entry: entry.get("weight", 0), reverse=True)


def _is_circuit_open(source_name: str) -> bool:
    state = SOURCE_STATE[source_name]
    return time.time() < state.get("cooldown_until", 0.0)


def _mark_source_success(source_name: str) -> None:
    SOURCE_STATE[source_name]["failures"] = 0
    SOURCE_STATE[source_name]["cooldown_until"] = 0


def _mark_source_failure(source_name: str) -> None:
    SOURCE_STATE[source_name]["failures"] = SOURCE_STATE[source_name].get("failures", 0) + 1
    if SOURCE_STATE[source_name]["failures"] >= MERCURIO_CIRCUIT_FAILURE_LIMIT:
        SOURCE_STATE[source_name]["cooldown_until"] = time.time() + MERCURIO_CIRCUIT_COOLDOWN_S
        logger.warning("Circuit breaker ativado para %s por %ss", source_name, MERCURIO_CIRCUIT_COOLDOWN_S)


def _get_cached_bundle() -> Dict[str, Any] | None:
    if BUNDLE_CACHE["payload"] and time.time() < BUNDLE_CACHE["expires_at"]:
        payload = dict(BUNDLE_CACHE["payload"])
        payload["metadata"] = {**payload.get("metadata", {}), "cache_hit": True}
        return payload
    return None


def _store_cached_bundle(payload: Dict[str, Any]) -> None:
    BUNDLE_CACHE["payload"] = payload
    BUNDLE_CACHE["expires_at"] = time.time() + MERCURIO_BUNDLE_CACHE_TTL_S


@app.get("/")
async def health():
    return {
        "status": "online",
        "service": SERVICE_NAME,
        "port": SERVICE_PORT,
        "timestamp": datetime.utcnow().isoformat(),
    }


@app.get("/api/v1/mercurio/bundle")
async def get_integrated_bundle(request: Request):
    client_ip = request.client.host if request.client else "unknown"
    logger.info("Gerando bundle para IP %s", client_ip)

    cached = _get_cached_bundle()
    if cached:
        return cached

    security_data = {"status": "PROTECTED", "shield_level": "OPTIMAL", "client_ip": client_ip}
    try:
        sec_res = requests.get(HEIMDALL_CHECK_URL, params={"ip": client_ip}, timeout=REQUEST_TIMEOUT_DEFAULT)
        if sec_res.ok:
            security_data = sec_res.json()
    except requests.RequestException as exc:
        logger.warning("Heimdall indisponível, fallback local ativado: %s", exc)

    bird_trends: List[Dict[str, Any]] = []
    external_trends: List[Dict[str, Any]] = []
    news: List[Dict[str, Any]] = []
    sources: List[str] = []

    if not _is_circuit_open("tas"):
        try:
            tas_res = requests.get(TAS_TRENDS_URL, timeout=REQUEST_TIMEOUT_DEFAULT)
            if tas_res.ok:
                bird_trends = _normalize_tas_trends(tas_res.json())
                if bird_trends:
                    sources.append("BIRD_NETWORK")
                _mark_source_success("tas")
            else:
                _mark_source_failure("tas")
        except requests.RequestException as exc:
            logger.info("TAS indisponível: %s", exc)
            _mark_source_failure("tas")
    else:
        logger.info("TAS em cooldown de circuit breaker")

    if not _is_circuit_open("iris"):
        try:
            iris_res = requests.get(IRIS_SCAN_URL, timeout=REQUEST_TIMEOUT_DEFAULT * 2)
            if iris_res.ok:
                iris_payload = iris_res.json()
                external_trends = _normalize_iris_trends(iris_payload)
                news = _normalize_news_items(iris_payload.get("news", []))
                if external_trends or news:
                    sources.append("EXTERNAL_FEEDS")
                _mark_source_success("iris")
            else:
                _mark_source_failure("iris")
        except requests.RequestException as exc:
            logger.error("IRIS indisponível: %s", exc)
            _mark_source_failure("iris")
    else:
        logger.info("IRIS em cooldown de circuit breaker")

    final_trends = _rank_weighted_trends([*bird_trends, *external_trends])

    if not final_trends:
        final_trends = [
            {
                "id": "fallback_1",
                "category": "SISTEMA",
                "title": "Aguardando pulso de rede...",
                "topic": "Aguardando pulso de rede...",
                "summary": "Os sensores estão reconectando as fontes externas.",
                "source": "SYSTEM",
                "origin": "SYSTEM",
                "weight": 0,
                "hashtag": "#Sincronizando",
                "volume": "N/A",
                "link": "/mercurio",
                "bird_signal": _build_bird_signal("sincronizando"),
            }
        ]
        news = [{"source": "SYSTEM", "title": "Sem conexão com provedores", "link": "", "published": "N/A", "origin": "SYSTEM", "weight": 0}]
        sources = ["FALLBACK"]

    events = [{"id": "e1", "category": "PENTAIA", "title": "Protocolo Mercúrio Ativo"}]
    primary_source = sources[0] if sources else "NONE"

    payload = {
        "trends": final_trends,
        "security": security_data,
        "events": events,
        "news": news,
        "metadata": {
            "source": primary_source,
            "sources": sources,
            "weight_policy": {
                "BIRD_NETWORK": MERCURIO_WEIGHT_BIRD,
                "RSS": MERCURIO_WEIGHT_RSS,
                "API_NEWS": MERCURIO_WEIGHT_API,
            },
            "cache_ttl_s": MERCURIO_BUNDLE_CACHE_TTL_S,
            "cache_hit": False,
            "evolution_level": 2,
            "node": f"{SERVICE_NAME}_hub_{SERVICE_PORT}",
            "generated_at": datetime.utcnow().isoformat(),
        },
    }

    _store_cached_bundle(payload)
    return payload


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=SERVICE_PORT)