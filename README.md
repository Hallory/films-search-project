# Films Search Project

## Overview
Full stack app for searching films and actors. The backend exposes a REST API and logs search analytics to MongoDB. The frontend is a Next.js UI that consumes the API.

## Features
- Film search by keyword
- Actor search with related films
- Combined search (titles + actors)
- Browse by genre and year range
- Film and actor detail pages
- Analytics: popular queries, recent genre filters, film view stats

## Architecture
- Frontend: Next.js (App Router), React Query, Tailwind CSS
- Backend: FastAPI, Pydantic
- MySQL: films, people, genres, relations
- MongoDB: search logs and aggregated analytics

## Data Flow (Search)
1) User submits a query in the frontend.
2) Frontend calls `GET /films/search/all`.
3) Backend queries MySQL for titles and people.
4) Backend returns combined results and writes a log entry to MongoDB.
5) Frontend renders results and analytics pages read aggregated data.

## Analytics
- Search logs are saved in `backend/services/mongo_logger.py`.
- Each log stores `timestamp`, `search_type`, `parameters`, `results_count`.
- Aggregations are in `backend/db/mongo_analytics_queries.py`.
- Frontend reads analytics via `/films/analytics/*` endpoints.

## API Quick Reference
Base URL (local): `http://127.0.0.1:8000`

- `GET /films/search/keyword`
- `GET /films/search/actor`
- `GET /films/search/all`
- `GET /films/search/genre`
- `GET /films/{film_id}`
- `GET /films/actors/{actor_id}`
- `GET /films/analytics/popular-queries`
- `GET /films/analytics/recent-genre-searches`

## Project Structure
- `backend/` - FastAPI app, services, DB access, analytics, tests
- `frontend/` - Next.js app, UI components, API client

## Setup

### Backend
1) `cd backend`
2) `python -m venv .venv`
3) Activate venv (Windows): `.\.venv\Scripts\activate`
4) `pip install -r requirements.txt`
5) Copy `backend/.env.example` to `backend/.env` and fill values
6) `uvicorn app:app --reload`

### Frontend
1) `cd frontend`
2) `npm install`
3) `npm run dev`

## Environment Variables
Backend (`backend/.env`):
- `MYSQL_HOST`, `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_DB`, `MYSQL_PORT`
- `MEDIA_MYSQL_HOST`, `MEDIA_MYSQL_USER`, `MEDIA_MYSQL_PASSWORD`, `MEDIA_MYSQL_DB`
- `MONGO_URI`, `MONGO_DB_NAME`, `MONGO_COLLECTION`, `MONGO_FILM_VIEWS_COLL`, `MONGO_FILM_STATS_COLL`
- `TMDB_API_KEY`
- `CORS_ORIGINS`

Frontend (optional):
- `NEXT_PUBLIC_API_BASE_URL` (defaults to `http://127.0.0.1:8000`)

## Tests
From `backend/`:
- Install dev deps: `pip install -r requirements-dev.txt`
- Run: `python -m pytest`

## Optional Screenshots
If screenshots are needed for presentation, place them in a `docs/` folder:
- `docs/ui-search.png`
- `docs/analytics-popular.png`
- `docs/mongo-log-entry.png`

## Notes
- MySQL stores film and people data (TMDB-based schema).
- MongoDB stores analytics logs and film stats.
