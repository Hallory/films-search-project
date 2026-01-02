from mongo_queries import get_popular_films_stats
from db.mysql import get_films_by_ids

def get_popular_films(limit: int =10)->list[dict[str,any]]:
    stats = get_popular_films_stats(limit=limit)
    films_ids = [item['film_id'] for item in stats]
    
    films_rows = get_films_by_ids(ids=films_ids)
    
    films_by_id = {f['film_id']:f for f in films_rows}
    
    result: list[dict[str, any]] = []
    
    for s in stats:
        film = films_by_id.get(s['film_id'])
        if not film:
            continue
        if film:
            films_with_stats = {
                **film,
                "search_impressions": s.get('search_impressions',0),
                "last_seen_at": s.get('last_seen_at'),
            }
            result.append(films_with_stats)
    return result