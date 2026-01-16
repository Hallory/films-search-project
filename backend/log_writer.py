from datetime import datetime, timezone

from pymongo import MongoClient

from settings import settings

_client = MongoClient(settings.MONGO_URI)
_db = _client[settings.MONGO_DB_NAME]
search_log_collection = _db[settings.MONGO_COLLECTION]
film_views_collection = _db[settings.MONGO_FILM_VIEWS_COLL]
film_stats_collection = _db[settings.MONGO_FILM_STATS_COLL]

def log_search(search_type:str, parameters:dict, results_count:int)->None:
    
    doc = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "search_type": search_type,
        "parameters": parameters,
        "results_count": results_count
    }
    
    try:
        search_log_collection.insert_one(doc)
    except Exception as e:
        print("MongoDB Error",e)
        

def log_film_view(film_id:int):
    log_entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "film_id": film_id,
    }
    
    try:
        film_views_collection.insert_one(log_entry)
    except Exception as e:
        print("MongoDB Error",e)
        
        
def update_films_stats(result_ids:list[int])->None:
    now = datetime.now(timezone.utc).isoformat()
    
    for film_id in result_ids:
        try:
            film_stats_collection.update_one(
                {"film_id": film_id},
                {
                    "$inc": {"search_impressions": 1},
                    "$set": {"last_seen_at": now},
                },
                upsert=True,
            )
        except Exception as e:
            print("MongoDB Error",e)
            

