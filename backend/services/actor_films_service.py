from db.mysql import get_actor_by_id, get_films_by_actor_id
from schemas.films import ActorHit, Film


def get_actor_hit_by_id(actor_id:int)-> ActorHit | None:
    actor_row = get_actor_by_id(actor_id)
    
    if actor_row is None:
        return None
    
    films_data = get_films_by_actor_id(actor_id)
    
    return ActorHit(
        actor_id=actor_id,
        full_name=actor_row['full_name'],
        films=[Film(**row) for row in films_data]
    )