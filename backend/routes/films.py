from fastapi import APIRouter, HTTPException, Query
from db.mysql import  get_latest_films, get_all_genres
from schemas.films import   Film, FilmDetail, FilmResponse, Genre, GenresResponse, YearsRange
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


@router.get('/genres', response_model=GenresResponse)
def list_genres():
    genres = get_all_genres()
    return GenresResponse(
    items=[Genre(**g) for g in genres],
    count=len(genres),
    )
    
  