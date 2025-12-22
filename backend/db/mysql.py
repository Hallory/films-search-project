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



def get_all_genres()->list[dict]:
    sql = """
        SELECT category_id, name
        FROM category
        ORDER BY name;
    """    
    return query_all(sql)

