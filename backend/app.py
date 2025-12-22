from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from settings import settings

from routes.films import router as films_router

app = FastAPI(title="🎬 Movie Finder API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(films_router)