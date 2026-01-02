import mysql.connector
from settings import settings

dbconfig = {
    'user': settings.MYSQL_USER,
    'password': settings.MYSQL_PASSWORD,
    'host': settings.MYSQL_HOST,
    'database': settings.MYSQL_DB
}

_cfg = dbconfig.copy()

def query_all(sql:str, params: tuple = ())->list[dict]:
    with mysql.connector.connect(**_cfg) as conn:
        with conn.cursor(dictionary=True) as cur:
            cur.execute(sql, params)
            return cur.fetchall()
        

def get_latest_films(limit: int = 10, offset:int = 0)->list[dict]:
    sql = """
        SELECT film_id, title, release_year, length, rating, description
        FROM film
        ORDER BY release_year DESC, film_id DESC
        LIMIT %s OFFSET %s;
    """
    return query_all(sql,(limit, offset))



def search_films_by_keyword(keyword:str, limit: int = 10, offset: int = 0)->list[dict]:
    sql = """
        SELECT film_id, title, release_year, length, rating, description
        FROM film
        WHERE title LIKE CONCAT('%', %s, '%')
        ORDER BY release_year DESC, film_id DESC
        LIMIT %s OFFSET %s;
    """
    
    return query_all(sql,(keyword,limit,offset))





def get_all_genres()->list[dict]:
    sql = """
        SELECT category_id, name
        FROM category
        ORDER BY name;
    """    
    return query_all(sql)


def search_films_by_genre_and_years(category_id:int, year_from:int, year_to:int, limit:int = 10, offset:int = 0)-> list[dict]:
    sql = """
        SELECT f.film_id, f.title, f.description, f.release_year, f.length, f.rating, c.name as genre
        FROM film as f
        JOIN film_category as fc
        on fc.film_id = f.film_id
        JOIN category as c 
        on c.category_id = fc.category_id
        WHERE fc.category_id = %s
        AND f.release_year BETWEEN %s AND %s
        ORDER BY f.release_year DESC, f.film_id DESC
        LIMIT %s OFFSET %s;
    """
    return query_all(sql,(category_id, year_from, year_to, limit, offset))

def count_films_by_genre_and_years(category_id:int, year_from:int, year_to:int) -> int:
    sql = """
        SELECT COUNT(*) AS cnt
        FROM film AS f
        JOIN film_category AS fc ON fc.film_id = f.film_id
        WHERE fc.category_id = %s
          AND f.release_year BETWEEN %s AND %s;
    """
    row = query_all(sql, (category_id, year_from, year_to))
    return row[0]["cnt"] if row else 0


def get_years_range()->list[dict]:
    sql = """
        SELECT 
            MIN(release_year) as min_year,
            MAX(release_year) as max_year
        FROM film;
    """
    rows = query_all(sql)
    return rows[0] if rows else{"min_year":None, "max_year":None}



def search_films_by_actor(full_name: str, limit: int = 10, offset: int = 0) -> list[dict]:
    sql = """
        SELECT 
            f.film_id,
            f.title,
            f.description,
            f.release_year,
            f.length,
            f.rating,
            a.actor_id,
            CONCAT(a.first_name, ' ', a.last_name) AS actor_full_name
        FROM film AS f
        JOIN film_actor AS fa
            ON fa.film_id = f.film_id
        JOIN actor AS a
            ON a.actor_id = fa.actor_id
        WHERE CONCAT(a.first_name, ' ', a.last_name) LIKE %s
        ORDER BY f.release_year DESC, f.film_id DESC
        LIMIT %s OFFSET %s;
    """
    pattern = f"%{full_name}%"
    return query_all(sql, (pattern, limit, offset))

def get_actors_for_film(film_id: int) -> list[dict]:
    sql = """
        SELECT 
            a.actor_id,
            a.first_name,
            a.last_name,
            CONCAT(a.first_name, ' ', a.last_name) AS full_name
        FROM actor AS a
        JOIN film_actor AS fa
            ON fa.actor_id = a.actor_id
        WHERE fa.film_id = %s
        ORDER BY full_name;
    """
    return query_all(sql, (film_id,))


def get_film_by_id(film_id: int) -> dict | None:
    sql = """
        SELECT 
            f.film_id,
            f.title,
            f.description,
            f.release_year,
            f.rating,
            f.length,
            l.name AS language
        FROM film f
        JOIN language l ON f.language_id = l.language_id
        WHERE f.film_id = %s
    """
    rows = query_all(sql, (film_id,))
    return rows[0] if rows else None


def get_films_by_ids(ids: list[int]) -> list[dict]:
    if not ids:
        return []
    placeholders = ", ".join("%s" for _ in ids)
    sql = f"""
        SELECT 
            film_id,
            title,
            description,
            release_year,
            rating,
            length
        FROM film
        WHERE film_id IN ({placeholders})
    """
    return query_all(sql, tuple(ids))
    
    
def get_actor_by_id(actor_id: int) -> dict | None:
    sql = """
        SELECT 
            actor_id,
            first_name,
            last_name,
            CONCAT(first_name, ' ', last_name) AS full_name
        FROM actor
        WHERE actor_id = %s
    """
    rows = query_all(sql, (actor_id,))
    return rows[0] if rows else None

def get_films_by_actor_id(actor_id: int) -> list[dict]:
    sql = """
        SELECT 
            f.film_id,
            f.title,
            f.description,
            f.release_year,
            f.rating,
            f.length,
            l.name AS language
        FROM film f
        JOIN language l ON f.language_id = l.language_id
        JOIN film_actor fa ON f.film_id = fa.film_id
        WHERE fa.actor_id = %s
    """
    return query_all(sql, (actor_id,))