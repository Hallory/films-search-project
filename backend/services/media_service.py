from settings import settings
from repositories.media_repo import MediaRepo

def build_image_url(path: str, size: str) -> str:
    if not path:
        return
    
    return f"{settings.TMDB_IMAGE_BASE}/{size}{path}"


def attach_media(items: list[dict], media_repo: MediaRepo = MediaRepo()):
    film_ids = [it["film_id"] for it in items if "film_id" in it]
    media_map = media_repo.get_media_for_film_ids(film_ids)

    for it in items:
        m = media_map.get(it.get("film_id"))
        it["poster_url"] = build_image_url(m.get("poster_path") if m else None, settings.TMDB_POSTER_SIZE)
        it["backdrop_url"] = build_image_url(m.get("backdrop_path") if m else None, settings.TMDB_BACKDROP_SIZE)

    return items