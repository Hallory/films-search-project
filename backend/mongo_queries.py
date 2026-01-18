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
    search_type: str | None = None, 
) -> list[dict]:
    match: dict = {
        "results_count": {"$gte": min_results},
        "parameters.query": {"$type": "string", "$ne": ""},
        "search_type": {"$in": ["all", "title", "actor"]},  
    }

    if search_type:
        match["search_type"] = search_type

    pipeline = [
        {"$match": match},
        {"$project": {"query": {"$toLower": "$parameters.query"}, "timestamp": 1, "results_count": 1}},
        {"$group": {
            "_id": "$query",
            "count": {"$sum": 1},
            "last_seen_at": {"$max": "$timestamp"},
            "avg_results": {"$avg": "$results_count"}, 
        }},
        {"$sort": {"count": -1, "last_seen_at": -1}},
        {"$limit": limit},
    ]

    try:
        return list(search_log_collection.aggregate(pipeline))
    except Exception as e:
        print("MongoDB Error while fetching popular queries:", e)
        return []


def get_recent_genre_searches(limit: int = 5) -> list[dict]:
    pipeline = [
        {"$match": {"search_type": "genre"}},
        {"$sort": {"timestamp": -1}},
        {"$limit": limit},
        {"$project": {
            "_id": 0,
            "timestamp": 1,
            "genre_id": "$parameters.genre_id",
            "year_from": "$parameters.year_from",
            "year_to": "$parameters.year_to",
            "results_count": 1,
        }},
    ]
    try:
        return list(search_log_collection.aggregate(pipeline))
    except Exception as e:
        print("MongoDB Error while fetching recent genre searches:", e)
        return []