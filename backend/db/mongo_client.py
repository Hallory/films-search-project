from pymongo import MongoClient
from settings import settings

_client = MongoClient(settings.MONGO_URI)
_db = _client[settings.MONGO_DB_NAME]

search_log_collection = _db[settings.MONGO_COLLECTION]
film_views_collection = _db[settings.MONGO_FILM_VIEWS_COLL]
film_stats_collection = _db[settings.MONGO_FILM_STATS_COLL]

