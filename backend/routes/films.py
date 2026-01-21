import logging
from fastapi import APIRouter, HTTPException, Query

from services.search_service import search_all
from services.mongo_logger import log_film_view, log_search, update_films_stats
from services.tmdb_media_mapper import map_title_rows, map_title_row, build_profile_url

from db.tmdb_mysql_queries import (
    get_latest_titles,
    get_popular_titles,
    get_title_by_id,
    get_years_range_tmdb,
    get_all_tmdb_genres,
    get_titles_by_genre,
    count_titles_by_genre,
    search_titles_by_keyword,
    count_titles_by_keyword,
    get_person_by_id,
    search_people_by_name,
    count_people_by_name,
    get_titles_for_person,
    get_title_genres,
    get_title_cast,
    get_title_crew_key_people,
)

from db.mongo_analytics_queries import get_popular_search_queries, get_recent_genre_searches

from schemas.films import (
    CombinedSearchResponse,
    Film,
    FilmResponse,
    Genre,
    GenresResponse,
    YearsRange,
    SearchLogIn,
    FilmViewIn,
    PopularQueriesResponse,
    ActorSearchResponse,
)


logger = logging.getLogger(__name__)

router = APIRouter(prefix='/films',tags=['films'])

@router.get('/latest', response_model=FilmResponse)
def get_latest_films_route(offset: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=50)):
    items = get_latest_titles(offset=offset, limit=limit)
    items = map_title_rows(items)

    return FilmResponse(
        items=[Film(**f) for f in items],
        offset=offset,
        limit=limit,
        count=len(items),
    )

@router.get('/popular', response_model=FilmResponse)
def popular_films_route(limit: int = Query(10, ge=1, le=50), offset: int = Query(0, ge=0)):
    items = get_popular_titles(limit=limit, offset=offset)
    items = map_title_rows(items)

    return FilmResponse(
        items=[Film(**f) for f in items],
        offset=offset,
        limit=limit,
        count=len(items),
    )

@router.get('/genres', response_model=GenresResponse)
def list_genres():
    rows = get_all_tmdb_genres()
    items = [{"genre_id": r["genre_id"], "name": r["name"]} for r in rows]
    return GenresResponse(items=[Genre(**g) for g in items], count=len(items))

    
@router.get('/search/keyword', response_model=FilmResponse)
def search_by_keyword_route(keyword: str, offset: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=50)):
    keyword = keyword.strip()
    logger.info("search/keyword keyword=%s offset=%s limit=%s", keyword, offset, limit)
    items = search_titles_by_keyword(keyword, offset=offset, limit=limit)
    items = map_title_rows(items)
    total = count_titles_by_keyword(keyword)

    log_search(
        search_type="title",
        parameters={
            "query": keyword,
            "offset": offset,
            "limit": limit,
        },
        results_count=total,
    )


    return FilmResponse(
        items=[Film(**f) for f in items],
        offset=offset,
        limit=limit,
        count=total,
    )

    
@router.get('/years-range', response_model=YearsRange)
def years_range():
    return get_years_range_tmdb()


@router.get('/search/genre', response_model=FilmResponse)
def search_by_genre_and_years(
    genre_id: int,
    year_from: int | None = None,
    year_to: int | None = None,
    limit: int = Query(10, ge=1, le=50),
    offset: int = Query(0, ge=0),
):
    logger.info(
        "search/genre genre_id=%s year_from=%s year_to=%s offset=%s limit=%s",
        genre_id,
        year_from,
        year_to,
        offset,
        limit,
    )
    items = get_titles_by_genre(
        genre_id=genre_id,
        year_from=year_from,
        year_to=year_to,
        limit=limit,
        offset=offset,
    )
    total = count_titles_by_genre(
        genre_id=genre_id,
        year_from=year_from,
        year_to=year_to,
    )

    items = map_title_rows(items)

    log_search(
        search_type="genre",
        parameters={
            "genre_id": genre_id,
            "year_from": year_from,
            "year_to": year_to,
            "offset": offset,
            "limit": limit,
        },
        results_count=len(items),
    )

    return FilmResponse(
        items=[Film(**f) for f in items],
        offset=offset,
        limit=limit,
        count=total
    )

    

@router.get('/search/all', response_model=CombinedSearchResponse)
def search_all_query(
    query: str,
    limit_per_section: int = Query(10, ge=1, le=50),
    title_offset: int = Query(0, ge=0),
):
    logger.info(
        "search/all query=%s limit_per_section=%s title_offset=%s",
        query,
        limit_per_section,
        title_offset,
    )
    data = search_all(query=query, limit_per_section=limit_per_section, title_offset=title_offset)

    by_title_count = data.by_title.count
    by_actor_count = data.by_actor.count
    total = by_title_count + by_actor_count

    log_search(
        search_type="all",
        parameters={
            "query": data.query,
            "limit_per_section": limit_per_section,
            "title_offset": title_offset,
            "by_title": by_title_count,
            "by_actor": by_actor_count,
        },
        results_count=total,
    )
    return data


@router.post('/analytics/search')
def log_search_route(payload: SearchLogIn):
    log_search(
        search_type=payload.search_type,
        parameters=payload.parameters,
        results_count=payload.results_count,
    )
    return {"ok": True}


@router.post('/analytics/film-view')
def log_film_view_route(payload: FilmViewIn):
    log_film_view(film_id=payload.film_id)
    update_films_stats(result_ids=[payload.film_id])
    return {"ok": True}


@router.get('/analytics/popular-queries', response_model=PopularQueriesResponse)
def popular_queries(
    limit: int = Query(5, ge=1, le=50),
    min_results: int = Query(1, ge=0),
    search_type: str | None = Query(None),
):
    search_type = search_type or None
    rows = get_popular_search_queries(limit=limit, min_results=min_results, search_type=search_type)
    items = [
        {
            "query": row.get("_id"),
            "count": row.get("count", 0),
            "last_seen_at": row.get("last_seen_at"),
        }
        for row in rows
    ]
    return {"items": items, "count": len(items)}
    
    
@router.get('/analytics/recent-genre-searches')
def recent_genre_searches(limit: int = Query(5, ge=1, le=50)):
    rows = get_recent_genre_searches(limit=limit)
    return {"items": rows, "count": len(rows)}

@router.get('/{film_id}')
def film_detail(film_id: int):
    film = get_title_by_id(film_id)
    if not film:
        raise HTTPException(status_code=404, detail="Film not found")

    media_type = film.get("media_type", "movie")

    film = map_title_row(film)

    genres = get_title_genres(film_id, media_type)
    cast = get_title_cast(film_id, media_type, limit=12)
    crew = get_title_crew_key_people(film_id, media_type)

    actors = []
    for a in cast:
        actors.append({
            "actor_id": a["person_id"],
            "full_name": a["name"],
            "photo_url": build_profile_url(a.get("profile_path")),
            "character": a.get("character_name"),
        })

    director = next((x for x in crew if x.get("job") == "Director"), None)
    producers = [x for x in crew if x.get("job") in ("Producer", "Executive Producer")][:4]

    if director:
        director = {
            "person_id": director["person_id"],
            "full_name": director["name"],
            "photo_url": build_profile_url(director.get("profile_path")),
            "job": director["job"],
        }

    producers_out = []
    for p in producers:
        producers_out.append({
            "person_id": p["person_id"],
            "full_name": p["name"],
            "photo_url": build_profile_url(p.get("profile_path")),
            "job": p["job"],
        })

    return {
        **film,
        "genres": genres,
        "actors": actors,
        "director": director,
        "producers": producers_out,
    }
    
    
@router.get("/actors/{actor_id}")
def get_actor(actor_id: int):
    person = get_person_by_id(actor_id)
    if not person:
        raise HTTPException(status_code=404, detail="Actor not found")

    films = get_titles_for_person(actor_id, limit=50)
    films = map_title_rows(films)

    return {
        "actor_id": actor_id,
        "full_name": person["name"],
        "photo_url": build_profile_url(person.get("profile_path")),
        "films": films,
    }

@router.get("/search/actor", response_model=ActorSearchResponse) 
def search_actor(full_name: str, limit: int = Query(10, ge=1, le=20), offset: int = Query(0, ge=0)):
    full_name = full_name.strip()
    logger.info("search/actor full_name=%s offset=%s limit=%s", full_name, offset, limit)
    people = search_people_by_name(full_name, limit=limit, offset=offset)
    total = count_people_by_name(full_name)

    items = []
    for p in people:
        films = get_titles_for_person(p["person_id"], limit=8)
        films = map_title_rows(films)

        items.append({
            "actor_id": p["person_id"],
            "full_name": p["name"],
            "films": films,
        })
        

    log_search(
        search_type="actor",
        parameters={
            "query": full_name,
            "offset": offset,
            "limit": limit,
        },
        results_count=total,
    )

    return {"items": items, "count": total}

