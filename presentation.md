# Films Search Project - 5 Minutes

## 0) Goal 
- Build a search system for films and actors.
- Add analytics for search usage.

## 1) Demo Flow 
- Search by keyword (films + actors).
- Open a film detail page.
- Open an actor page.
- Analytics page (popular queries + recent genre filters).

## 2) Architecture 
- Frontend: Next.js, React Query, Tailwind.
- Backend: FastAPI (REST).
- MySQL: films, people, genres.
- MongoDB: search logs and aggregated analytics.

## 3) How Search Works
1) Frontend calls `GET /films/search/all`.
2) Backend queries MySQL (titles + people).
3) Backend builds a combined response.
4) Backend logs the search in MongoDB.

## 4) Logging and Analytics
- Log format: `timestamp`, `search_type`, `parameters`, `results_count`.
- Aggregations: `backend/db/mongo_analytics_queries.py`.
- Analytics endpoints:
  - `GET /films/analytics/popular-queries`
  - `GET /films/analytics/recent-genre-searches`

## 5) Requirements Coverage
- Keyword search (limit/offset) -> `GET /films/search/keyword`.
- Genre and year range search -> `GET /films/search/genre`.
- Log searches to MongoDB -> `backend/services/mongo_logger.py`.
- Top-5 popular queries -> `GET /films/analytics/popular-queries`.

## 6) Extra Features
- Actor search -> `GET /films/search/actor`.
- Combined search (films + actors) -> `GET /films/search/all`.
- Web UI instead of console (same search logic).
- Film/actor pages, pagination, tests.

## 7) Tests
- Unit tests for services and Mongo aggregations.
- Run: `python -m pytest` from `backend/`.

## Closing
- Search and analytics work end-to-end.
