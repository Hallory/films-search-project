from pydantic import BaseModel

class Film(BaseModel):
    film_id: int
    title: str
    description: str | None = None
    release_year: int | None = None
    length: int | None = None
    rating: str | None = None
    
class FilmResponse(BaseModel):
    items: list[Film]
    offset: int
    limit: int
    count: int

class Genre(BaseModel):
    category_id: int
    name: str


class GenresResponse(BaseModel):
    items: list[Genre]
    count: int
    
