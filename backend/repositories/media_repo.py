import mysql.connector
from settings import settings


class MediaRepo:
    def __init__(self):
        self._cfg = {
            "user": settings.MEDIA_MYSQL_USER,
            "password": settings.MEDIA_MYSQL_PASSWORD,
            "host": settings.MEDIA_MYSQL_HOST,
            "database": settings.MEDIA_MYSQL_DB,
        }


    def get_media_for_film_ids(self, film_ids: list[int]) -> dict[int, dict]:
        if not film_ids:
            return {}

        placeholders = ",".join(["%s"] * len(film_ids))
        sql = f"""
        SELECT film_id, poster_path, backdrop_path
        FROM film_media
        WHERE film_id IN ({placeholders})
        """

        with mysql.connector.connect(**self._cfg) as conn:
            with conn.cursor(dictionary=True) as cur:
                cur.execute(sql, tuple(film_ids))
                rows = cur.fetchall()

        return {row["film_id"]: row for row in rows}

media_repo = MediaRepo()