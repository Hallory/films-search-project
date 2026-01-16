from log_writer import film_stats_collection, search_log_collection

def get_popular_films_stats(limit: int = 10)->list[dict]:
    try:
        cursor = film_stats_collection.find(
            {"last_seen_at": {"$exists": True}},
            {"film_id": 1, "search_impressions": 1},
            ).sort([("search_impressions", -1),("last_seen_at", -1)],
            ).limit(limit)
        return list(cursor)
    except Exception as e:
        print("MongoDB Error while fetching popular films:", e)
        return []


def get_popular_search_queries(
    limit: int = 5,
    min_results: int = 1,
    search_type: str | None = "keyword",
) -> list[dict]:
    match: dict = {
        "results_count": {"$gte": min_results},
        "parameters.query": {"$type": "string", "$ne": ""},
    }
    if search_type:
        match["search_type"] = search_type

    pipeline = [
        {"$match": match},
        {"$project": {"query": {"$toLower": "$parameters.query"}, "timestamp": 1}},
        {"$group": {"_id": "$query", "count": {"$sum": 1}, "last_seen_at": {"$max": "$timestamp"}}},
        {"$sort": {"count": -1, "last_seen_at": -1}},
        {"$limit": limit},
    ]

    try:
        cursor = search_log_collection.aggregate(pipeline)
        return list(cursor)
    except Exception as e:
        print("MongoDB Error while fetching popular queries:", e)
        return []
        
        
