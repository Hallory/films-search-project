# Films Search Project 

## 0) Goal 
- Build a simple search system for films and actors.
- Provide analytics for search usage.

## 1) Demo Flow 
- Search by keyword (shows films and actors).
- Open a film detail page.
- Open an actor page (list of films).
- Show analytics page (popular queries + recent genre filters).

## 2) Architecture 
- Frontend: Next.js, React Query, Tailwind.
- Backend: FastAPI with REST endpoints.
- MySQL: films, people, genres.
- MongoDB: search logs and analytics aggregates.

## 3) How Search Works 
1) Frontend calls `GET /films/search/all`.
2) Backend queries MySQL for titles and people.
3) Backend returns combined results.
4) Backend logs the search in MongoDB.

## 4) Logging and Analytics 
- Log entry format:
  - `timestamp`, `search_type`, `parameters`, `results_count`
- Aggregations are built in `backend/db/mongo_analytics_queries.py`.
- Frontend reads:
  - `GET /films/analytics/popular-queries`
  - `GET /films/analytics/recent-genre-searches`

## 5) Tests 
- Unit tests cover search service and Mongo analytics helpers.
- Run: `python -m pytest` from `backend/`.


## Closing 
- Search and analytics are working end-to-end.
- Future work: richer filters, caching, more analytics metrics.
