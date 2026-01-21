import mysql.connector
from mysql.connector import Error
import logging

from settings import settings

class DatabaseError(RuntimeError):
    pass

dbconfig = {
    'user': settings.MYSQL_USER,
    'password': settings.MYSQL_PASSWORD,
    'host': settings.MYSQL_HOST,
    'port': settings.MYSQL_PORT,
    'database': settings.MYSQL_DB
}

_cfg = dbconfig.copy()

logger = logging.getLogger(__name__)

def query_all(sql: str, params: tuple = ()) -> list[dict]:
    try:
        with mysql.connector.connect(**_cfg) as conn:
            with conn.cursor(dictionary=True) as cur:
                cur.execute(sql, params)
                return cur.fetchall()
    except Error as e:
        logger.exception("MySQL query failed: %s", sql)
        raise DatabaseError("DB query failed") from e

def query_one(sql: str, params: tuple = ()) -> dict | None:
    rows = query_all(sql, params)
    return rows[0] if rows else None
