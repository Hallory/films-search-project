
from db.mysql import search_films_by_keyword, search_films_by_actor
from schemas.films import ActorHit, ActorSearchResponse, CombinedSearchResponse, Film, FilmResponse


def search_all(query: str, limit_per_section: int = 10) -> dict[str,any]:
    title_rows = search_films_by_keyword(keyword=query, limit=limit_per_section, offset=0)
    
    by_title = FilmResponse(
        items=[Film(**film)for film in title_rows],
        offset=0,
        limit=limit_per_section,
        count=len(title_rows)
    )
    
    by_actor = build_actor_search_response(q=query, limit_per_actor=limit_per_section)
    
    return CombinedSearchResponse(
        query=query,
        by_title=by_title,
        by_actor=by_actor
    )
    
    
    
def build_actor_search_response(q:str, limit_per_actor: int = 10)->ActorSearchResponse:
    rows = search_films_by_actor(full_name=q, limit=100, offset=0)
    
    actors_map: dict[int,ActorHit] = {}
    items = []
    for row in rows:
        actor_id = row['actor_id']
        full_name = row['actor_full_name']

        film = Film(
            film_id=row['film_id'],
            title=row['title'],
            release_year=row['release_year'],
            description=row['description'],
            length=row['length'],
            rating=row['rating'],
            language=row.get('language')
        )
        
        if actor_id not in actors_map:
            actors_map[actor_id] = ActorHit(actor_id=actor_id, full_name=full_name, films=[film])
        else:
            if len(actors_map[actor_id].films) < limit_per_actor:
                actors_map[actor_id].films.append(film)
        
    items = list(actors_map.values())
        
    return ActorSearchResponse(items=items, count=len(items))