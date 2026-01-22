from settings import settings

TMDB_IMAGE_BASE = settings.TMDB_IMAGE_BASE
TMDB_POSTER_SIZE = settings.TMDB_POSTER_SIZE
TMDB_BACKDROP_SIZE = settings.TMDB_BACKDROP_SIZE



def build_image_url(path: str | None, size: str) -> str | None:
    if not path:
        return None
    return f"{TMDB_IMAGE_BASE}/{size}{path}"

def build_profile_url(path: str | None) -> str | None:
    return build_image_url(path, "w185")

def map_title_row(row: dict) -> dict:
    poster_path = row.pop("poster_path", None)
    backdrop_path = row.pop("backdrop_path", None)

    row["poster_url"] = build_image_url(poster_path, TMDB_POSTER_SIZE)
    row["backdrop_url"] = build_image_url(backdrop_path, TMDB_BACKDROP_SIZE)

    return row


def map_title_rows(rows: list[dict]) -> list[dict]:
    return [map_title_row(r) for r in rows]
