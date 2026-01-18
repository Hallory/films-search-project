from db.tmdb_mysql import (
    search_titles_by_keyword,
    count_titles_by_keyword,
    search_people_by_name,
    count_people_by_name,
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

def search_all(query: str, limit_per_section: int = 20, title_offset: int = 0) -> CombinedSearchResponse:
    # q = query.strip()
    # if len(q) < 2:
    #     return CombinedSearchResponse(
    #         query=q,
    #         by_title=FilmResponse(items=[], offset=0, limit=limit_per_section, count=0),
    #         by_actor=ActorSearchResponse(items=[], count=0),
    #     )
    total_titles = count_titles_by_keyword(keyword=query)
    rows = search_titles_by_keyword(keyword=query, limit=limit_per_section, offset=title_offset)
    rows = map_title_rows(rows)

    by_title = FilmResponse(
        items=[Film(**r) for r in rows],
        offset=title_offset,
        limit=limit_per_section,
        count=total_titles,
    )

    total_actors = count_people_by_name(name=query)
    people = search_people_by_name(name=query, limit=limit_per_section, offset=0)

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

    by_actor = ActorSearchResponse(items=actor_items, count=total_actors)

    return CombinedSearchResponse(query=query, by_title=by_title, by_actor=by_actor)

