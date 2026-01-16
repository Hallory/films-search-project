from db.tmdb_mysql import (
    search_titles_by_keyword,
    search_people_by_name,
    get_titles_for_person,
)
from services.tmdb_media_mapper import map_title_rows
from schemas.films import (
    CombinedSearchResponse,
    FilmResponse,
    Film,
    ActorSearchResponse,
    ActorHit,
)

def search_all(query: str, limit_per_section: int = 20) -> CombinedSearchResponse:
    # --- Films by title/keyword ---
    rows = search_titles_by_keyword(keyword=query, limit=limit_per_section, offset=0)
    rows = map_title_rows(rows)

    if not rows:
        return CombinedSearchResponse(query=query, by_title=FilmResponse(items=[], count=0), by_actor=ActorSearchResponse(items=[], count=0))

    by_title = FilmResponse(
        items=[Film(**r) for r in rows],
        offset=0,
        limit=limit_per_section,
        count=len(rows),
    )

    # --- Actors by name ---
    people = search_people_by_name(name=query, limit=limit_per_section, offset=0)

    if not people:
        return CombinedSearchResponse(query=query, by_title=by_title, by_actor=ActorSearchResponse(items=[], count=0))

    actor_items: list[ActorHit] = []
    for p in people:
        actor_id = p["person_id"]

        films = get_titles_for_person(actor_id, limit=8)
        films = map_title_rows(films)

        actor_items.append(
            ActorHit(
                actor_id=actor_id,
                full_name=p["name"],
                films=[Film(**f) for f in films],
            )
        )

    by_actor = ActorSearchResponse(items=actor_items, count=len(actor_items))

    return CombinedSearchResponse(query=query, by_title=by_title, by_actor=by_actor)

