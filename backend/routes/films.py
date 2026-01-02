from fastapi import APIRouter, HTTPException, Query
from db.mysql import count_films_by_genre_and_years, search_films_by_actor, search_films_by_keyword, get_latest_films, get_all_genres, get_years_range, search_films_by_genre_and_years, get_film_by_id, get_actors_for_film
from log_writer import log_film_view, log_search, update_films_stats
from schemas.films import  ActorHit, CombinedSearchResponse, Film, FilmDetail, FilmResponse, Genre, GenresResponse, YearsRange
from services.actor_films_service import get_actor_hit_by_id
from services.popular_service import get_popular_films
from services.search_service import search_all

router = APIRouter(prefix='/films',tags=['films'])

@router.get('/latest', response_model=FilmResponse)
def get_latest_films_route(offset: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=50)):
    items = get_latest_films(offset=offset, limit=limit)
        
    return FilmResponse(
        items=[Film(**f) for f in items],
        offset=offset,
        limit=limit,
        count=len(items),
    )

@router.get('/popular')
def popular_films_route(limit: int = Query(10, ge=1, le=50)):
    items = get_popular_films(limit=limit)

    return {
        "items":items,
        "count": len(items),
        "limit":limit
    }

@router.get('/genres', response_model=GenresResponse)
def list_genres():
    genres = get_all_genres()
    return GenresResponse(
    items=[Genre(**g) for g in genres],
    count=len(genres),
    )
    
    
    
@router.get('/search/keyword')
def search_by_keyword_route(keyword:str,offset: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=50)):
    items = search_films_by_keyword(keyword,offset=offset, limit=limit)
    
    log_search(
    search_type="keyword",
    parameters={"query": keyword},
    results_count=len(items),
    )
    
    result_ids = [item['film_id'] for item in items]

    update_films_stats(result_ids=result_ids)

    
    return {
        "keyword": keyword,
        "items":items,
        "offset":offset,
        "limit":limit,
        "count": len(items)
    }
    
    
    
@router.get('/years-range', response_model=YearsRange)
def years_range():
    data = get_years_range()
    return data


@router.get('/search/genre', response_model=FilmResponse)
def search_by_genre_and_years(category_id:int, year_from:int, year_to:int, limit:int = Query(10, ge=1, le=50), offset:int = Query(0, ge=0)):
    items = search_films_by_genre_and_years(category_id=category_id, year_from=year_from,year_to=year_to,limit=limit,offset=offset)
    
    total = count_films_by_genre_and_years(category_id=category_id, year_from=year_from,year_to=year_to)
    
    log_search(
    search_type="genre",
    parameters={
        "category_id": category_id,
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
    
    
    
@router.get('/search/actor')
def search_by_actor(full_name:str, limit:int = Query(10, ge=1, le=50), offset:int = Query(0, ge=0)):
    items = search_films_by_actor(full_name=full_name,limit=limit,offset=offset)
    return {
        "full_name":full_name,
        "items":items,
        "offset":offset,
        "limit":limit,
        "count": len(items)
    }
    
    
@router.get('/search/all', response_model=CombinedSearchResponse)
def search_all_query(query: str, limit_per_section: int = Query(10, ge=1, le=50)):
    return search_all(query=query, limit_per_section=limit_per_section)
    
    
@router.get('/{film_id}', response_model=FilmDetail)
def get_film_by_id_route(film_id:int):
    film = get_film_by_id(film_id=film_id)
    
    if not film:
        raise HTTPException(status_code=404, detail='Film not found')


    log_film_view(film_id=film_id)
    update_films_stats(result_ids=[film_id])
    
    actors = get_actors_for_film(film_id=film_id)
    
    return {
        **film,
        "actors":actors
    }
        
        
@router.get('/actors/{actor_id}', response_model=ActorHit)
def get_actor_by_id_route(actor_id:int):
    actor = get_actor_hit_by_id(actor_id=actor_id)
    
    if not actor:
        raise HTTPException(status_code=404, detail='Actor not found')
    
    return actor