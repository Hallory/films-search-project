from datetime import datetime, timezone
import logging

from db.mongo_client import (
    search_log_collection,
    film_views_collection,
    film_stats_collection,
)

logger = logging.getLogger(__name__)
def _normalize_parameters(search_type: str, parameters: dict) -> dict:
    p = dict(parameters or {})

    if "query" in p and isinstance(p["query"], str):
        p["query"] = p["query"].strip().lower()

    if "full_name" in p and isinstance(p["full_name"], str):
        p["full_name"] = p["full_name"].strip().lower()

    return p


def log_search(search_type: str, parameters: dict, results_count: int) -> None:
    doc = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "search_type": search_type,
        "parameters": _normalize_parameters(search_type, parameters),
        "results_count": results_count,
    }
    try:
        search_log_collection.insert_one(doc)
    except Exception:
        logger.exception("MongoDB error while logging search")


def log_film_view(film_id: int) -> None:
    log_entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "film_id": film_id,
    }
    try:
        film_views_collection.insert_one(log_entry)
    except Exception:
        logger.exception("MongoDB error while logging film view")


def update_films_stats(result_ids: list[int]) -> None:
    now = datetime.now(timezone.utc).isoformat()

    for film_id in result_ids:
        try:
            film_stats_collection.update_one(
                {"film_id": film_id},
                {"$inc": {"search_impressions": 1}, "$set": {"last_seen_at": now}},
                upsert=True,
            )
        except Exception:
            logger.exception("MongoDB error while updating films stats (film_id=%s)", film_id)
