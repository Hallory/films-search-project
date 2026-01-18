from repositories.mysql_repo import query_all, query_one


def get_latest_titles(limit: int = 10, offset: int = 0) -> list[dict]:
    sql = """
        SELECT
          tmdb_id AS film_id,
          title,
          overview AS description,
          year AS release_year,
          runtime AS length,
          CAST(vote_average AS DOUBLE) AS rating,
          poster_path,
          backdrop_path,
          trailer_key
        FROM tmdb_titles
        ORDER BY release_date DESC, vote_count DESC
        LIMIT %s OFFSET %s;
    """
    return query_all(sql, (limit, offset))


def get_popular_titles(limit: int = 10, offset: int = 0) -> list[dict]:
    sql = """
        SELECT
          tmdb_id AS film_id,
          title,
          overview AS description,
          year AS release_year,
          runtime AS length,
          CAST(vote_average AS DOUBLE) AS rating,
          poster_path,
          backdrop_path,
          trailer_key
        FROM tmdb_titles
        ORDER BY vote_count DESC, vote_average DESC
        LIMIT %s OFFSET %s;
    """
    return query_all(sql, (limit, offset))


def search_titles_by_keyword(keyword: str, limit: int = 10, offset: int = 0) -> list[dict]:
    sql = """
        SELECT
          tmdb_id AS film_id,
          title,
          overview AS description,
          year AS release_year,
          runtime AS length,
          CAST(vote_average AS DOUBLE) AS rating,
          poster_path,
          backdrop_path,
          trailer_key
        FROM tmdb_titles
        WHERE title LIKE CONCAT('%', %s, '%')
        ORDER BY vote_count DESC, vote_average DESC
        LIMIT %s OFFSET %s;
    """
    return query_all(sql, (keyword, limit, offset))


def count_titles_by_keyword(keyword: str) -> int:
    sql = """
        SELECT COUNT(*) AS cnt
        FROM tmdb_titles
        WHERE title LIKE CONCAT('%', %s, '%');
    """
    row = query_one(sql, (keyword,))
    return int(row["cnt"]) if row and row.get("cnt") is not None else 0


def get_title_by_id(film_id: int) -> dict | None:
    sql = """
        SELECT
          tmdb_id AS film_id,
          title,
          media_type,
          overview AS description,
          year AS release_year,
          runtime AS length,
          CAST(vote_average AS DOUBLE) AS rating,
          poster_path,
          backdrop_path,
          tagline,
          homepage,
          status,
          trailer_key
        FROM tmdb_titles
        WHERE tmdb_id = %s
        LIMIT 1;
    """
    return query_one(sql, (film_id,))


def get_years_range_tmdb() -> dict:
    sql = """
        SELECT MIN(year) AS min_year, MAX(year) AS max_year
        FROM tmdb_titles;
    """
    row = query_one(sql)
    return row or {"min_year": None, "max_year": None}


from repositories.mysql_repo import query_all, query_one

def get_all_tmdb_genres() -> list[dict]:
    sql = """
        SELECT genre_id, name
        FROM tmdb_genres
        ORDER BY name;
    """
    return query_all(sql)

def get_titles_by_genre(
    genre_id: int,
    year_from: int | None = None,
    year_to: int | None = None,
    limit: int = 10,
    offset: int = 0,
) -> list[dict]:
    sql = """
        SELECT
          t.tmdb_id AS film_id,
          t.title,
          t.overview AS description,
          t.year AS release_year,
          t.runtime AS length,
          CAST(t.vote_average AS DOUBLE) AS rating,
          t.poster_path,
          t.backdrop_path,
          t.trailer_key
        FROM tmdb_titles t
        JOIN tmdb_title_genres tg
          ON tg.tmdb_id = t.tmdb_id AND tg.media_type = t.media_type
        WHERE tg.genre_id = %s
          AND (%s IS NULL OR t.year >= %s)
          AND (%s IS NULL OR t.year <= %s)
        ORDER BY t.vote_count DESC, t.vote_average DESC
        LIMIT %s OFFSET %s;
    """
    return query_all(sql, (genre_id, year_from, year_from, year_to, year_to, limit, offset))

def get_title_genres(tmdb_id: int, media_type: str) -> list[dict]:
    sql = """
        SELECT g.genre_id, g.name
        FROM tmdb_title_genres tg
        JOIN tmdb_genres g ON g.genre_id = tg.genre_id
        WHERE tg.tmdb_id = %s AND tg.media_type = %s
        ORDER BY g.name;
    """
    return query_all(sql, (tmdb_id, media_type))


def get_title_cast(tmdb_id: int, media_type: str, limit: int = 12) -> list[dict]:
    sql = """
        SELECT p.person_id, p.name, p.profile_path, c.character_name, c.cast_order
        FROM tmdb_title_cast c
        JOIN tmdb_people p ON p.person_id = c.person_id
        WHERE c.tmdb_id = %s AND c.media_type = %s
        ORDER BY c.cast_order ASC
        LIMIT %s;
    """
    return query_all(sql, (tmdb_id, media_type, limit))


def get_title_crew_key_people(tmdb_id: int, media_type: str) -> list[dict]:
    sql = """
        SELECT p.person_id, p.name, p.profile_path, c.job
        FROM tmdb_title_crew c
        JOIN tmdb_people p ON p.person_id = c.person_id
        WHERE c.tmdb_id = %s AND c.media_type = %s
          AND c.job IN ('Director','Producer','Executive Producer')
        ORDER BY FIELD(c.job,'Director','Executive Producer','Producer'), p.name
        LIMIT 10;
    """
    return query_all(sql, (tmdb_id, media_type))

def count_titles_by_genre(
    genre_id: int,
    year_from: int | None = None,
    year_to: int | None = None,
) -> int:
    sql = """
        SELECT COUNT(*) AS cnt
        FROM tmdb_titles t
        JOIN tmdb_title_genres tg
          ON tg.tmdb_id = t.tmdb_id AND tg.media_type = t.media_type
        WHERE tg.genre_id = %s
          AND (%s IS NULL OR t.year >= %s)
          AND (%s IS NULL OR t.year <= %s);
    """
    row = query_one(sql, (genre_id, year_from, year_from, year_to, year_to))
    return int(row["cnt"]) if row and row.get("cnt") is not None else 0


from repositories.mysql_repo import query_all, query_one

def search_people_by_name(name: str, limit: int = 10, offset: int = 0) -> list[dict]:
    sql = """
        SELECT
          person_id,
          name,
          profile_path
        FROM tmdb_people
        WHERE name LIKE CONCAT('%', %s, '%')
        ORDER BY name
        LIMIT %s OFFSET %s;
    """
    return query_all(sql, (name, limit, offset))


def count_people_by_name(name: str) -> int:
    sql = """
        SELECT COUNT(*) AS cnt
        FROM tmdb_people
        WHERE name LIKE CONCAT('%', %s, '%');
    """
    row = query_one(sql, (name,))
    return int(row["cnt"]) if row and row.get("cnt") is not None else 0



def get_titles_for_person(person_id: int, limit: int = 8) -> list[dict]:
    sql = """
        SELECT
          t.tmdb_id AS film_id,
          t.title,
          t.overview AS description,
          t.year AS release_year,
          t.runtime AS length,
          CAST(t.vote_average AS DOUBLE) AS rating,
          t.poster_path,
          t.backdrop_path,
          t.trailer_key
        FROM tmdb_title_cast c
        JOIN tmdb_titles t
          ON t.tmdb_id = c.tmdb_id AND t.media_type = c.media_type
        WHERE c.person_id = %s
        ORDER BY t.vote_count DESC, t.vote_average DESC
        LIMIT %s;
    """
    return query_all(sql, (person_id, limit))


def get_person_by_id(person_id: int) -> dict | None:
    sql = "SELECT person_id, name, profile_path FROM tmdb_people WHERE person_id=%s LIMIT 1;"
    return query_one(sql, (person_id,))


