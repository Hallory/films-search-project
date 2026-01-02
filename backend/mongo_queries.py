from log_writer import film_stats_collection

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
        
        