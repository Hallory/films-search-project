
from pydantic import BaseModel, Field

class Film(BaseModel):
    film_id: int
    title: str
    description: str | None = None
    release_year: int | None = None
    length: int | None = None
    rating: float | None = None
    poster_url: str | None = None
    backdrop_url: str | None = None
    trailer_key: str | None = None
    
class FilmResponse(BaseModel):
    items: list[Film] = Field(default_factory=list)
    offset: int = 0
    limit: int = 10
    count: int = 0

class Genre(BaseModel):
    genre_id: int
    name: str


class GenresResponse(BaseModel):
    items: list[Genre]
    count: int
    
class YearsRange(BaseModel):
    min_year: int | None = None
    max_year: int | None = None
    
class Actor(BaseModel):
    actor_id: int
    first_name: str | None = None
    last_name: str | None = None
    full_name: str
    
class ActorHit(BaseModel):
    actor_id: int
    full_name: str
    films: list[Film]
    
class ActorSearchResponse(BaseModel):
    items: list[ActorHit]
    count: int

class SearchBreakdown(BaseModel):
    by_title: int = 0
    by_actor: int = 0

class SearchLogIn(BaseModel):
    search_type: str
    parameters: dict
    results_count: int
    breakdown: SearchBreakdown | None = None
    source: str | None = None

class FilmViewIn(BaseModel):
    film_id: int

class PopularQuery(BaseModel):
    query: str
    count: int
    last_seen_at: str | None = None

class PopularQueriesResponse(BaseModel):
    items: list[PopularQuery]
    count: int
    
class CombinedSearchResponse(BaseModel):
    query: str
    by_title: FilmResponse
    by_actor: ActorSearchResponse
class FilmDetail(Film):
    actors: list[Actor]
    language: str | None = None
    poster_url: str | None = None
    backdrop_url: str | None = None
    
