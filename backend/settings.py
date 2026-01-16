from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    MYSQL_HOST: str
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_DB: str
    MYSQL_PORT: int = 3306

    MONGO_URI: str
    MONGO_DB_NAME: str
    MONGO_COLLECTION: str
    MONGO_FILM_VIEWS_COLL: str = "film_views"
    MONGO_FILM_STATS_COLL: str = "film_stats"
    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]

    MEDIA_MYSQL_HOST: str
    MEDIA_MYSQL_USER: str
    MEDIA_MYSQL_PASSWORD: str
    MEDIA_MYSQL_DB: str

    TMDB_API_KEY: str
    TMDB_IMAGE_BASE: str = "https://image.tmdb.org/t/p"
    TMDB_POSTER_SIZE: str = "w342"
    TMDB_BACKDROP_SIZE: str = "w780"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

settings = Settings()
