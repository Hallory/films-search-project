from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):
    MYSQL_HOST: str 
    MYSQL_USER: str 
    MYSQL_PASSWORD: str 
    MYSQL_DB: str
    
    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://127.0.0.1:3000"] 
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )
    
settings = Settings()