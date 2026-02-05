'use client';

import { getPopularQueries, getRecentGenreSearches, GenresResponse, getGenres } from '@/lib/api';
import { useQuery } from '@tanstack/react-query';
type PopularItem = {
  query: string;
  count: number;
  avg_results?: number;
};
interface GenreRow {
  genre_id: number;
  year_from?: number;
  year_to?: number;
  timestamp: string;
  results_count: number;
  genre_name: string;
}

export default function PopularQueriesPage() {
  const popularQ = useQuery({
    queryKey: ['popular-queries', 'all'],
    queryFn: () => getPopularQueries(5, 'all'),
  });

  const recentGenreQ = useQuery({
    queryKey: ['recent-genre-searches'],
    queryFn: () => getRecentGenreSearches(5),
  });

  const genresQ = useQuery<GenresResponse>({
    queryKey: ['genres'],
    queryFn: getGenres,
  });

  const genresMap = new Map((genresQ.data?.items ?? []).map(g => [g.genre_id, g.name]));

  const popularItems = popularQ.data?.items ?? [];
  const maxCount = Math.max(1, ...popularItems.map((x: { count: number }) => x.count ?? 1));

  return (
    <main className="mx-auto max-w-4xl px-6 pt-24 pb-16 space-y-10">
      <header className="space-y-2">
        <h1 className="text-2xl font-semibold">Popular queries</h1>
        <p className="text-sm text-slate-400">
          Top searches and recent genre filters
        </p>
      </header>

      <section className="space-y-4">
        <div className="flex items-end justify-between">
          <h2 className="text-lg font-semibold">Top text searches</h2>
          <span className="text-xs text-slate-400">by frequency</span>
        </div>

        {popularQ.isLoading && <p className="text-sm text-slate-400">Loading…</p>}
        {popularQ.isError && <p className="text-sm text-red-400">Failed to load</p>}

        {!popularQ.isLoading && popularItems.length === 0 && (
          <p className="text-sm text-slate-400">No data yet. Try searching something.</p>
        )}

        <div className="space-y-3">
          {popularItems.map((item: PopularItem, idx: number) => {
            const pct = (item.count / maxCount) * 100;
            const avg = item.avg_results ? Math.round(item.avg_results) : null;

            return (
              <div
                key={item.query}
                className="rounded-2xl border border-slate-800/70 bg-slate-950/40 p-4"
              >
                <div className="flex items-start justify-between gap-4">
                  <div className="min-w-0">
                    <div className="text-xs text-slate-400">#{idx + 1}</div>
                    <div className="truncate text-lg font-semibold text-slate-100">
                      {item.query}
                    </div>
                    <div className="mt-1 text-xs text-slate-400">
                      {avg !== null ? `avg results: ~${avg}` : ' '}
                    </div>
                  </div>

                  <div className="text-right">
                    <div className="text-xs text-slate-400">searches</div>
                    <div className="text-2xl font-semibold text-slate-100">{item.count}</div>
                  </div>
                </div>

                <div className="mt-3 h-2 w-full rounded-full bg-slate-800/60 overflow-hidden">
                  <div
                    className="h-full rounded-full bg-indigo-500"
                    style={{ width: `${pct}%` }}
                  />
                </div>
              </div>
            );
          })}
        </div>
      </section>

      <section className="space-y-4">
        <div className="flex items-end justify-between">
          <h2 className="text-lg font-semibold">Recent genre filters</h2>
          <span className="text-xs text-slate-400">last 5</span>
        </div>

        {recentGenreQ.isLoading && <p className="text-sm text-slate-400">Loading…</p>}
        {recentGenreQ.isError && <p className="text-sm text-red-400">Failed to load</p>}

        <div className="space-y-3">
          {(recentGenreQ.data?.items ?? []).map((row: GenreRow) => {
            const genreName = genresMap.get(row.genre_id) ?? `Genre ${row.genre_id}`;
            const years =
              row.year_from && row.year_to
                ? `${row.year_from}–${row.year_to}`
                : row.year_from
                  ? `${row.year_from}`
                  : row.year_to
                    ? `${row.year_to}`
                    : 'any years';

            return (
              <div
                key={`${row.timestamp}-${row.genre_id}`}
                className="rounded-2xl border border-slate-800/70 bg-slate-950/40 p-4 flex items-center justify-between"
              >
                <div className="space-y-1">
                  <div className="text-sm font-semibold text-slate-100">
                    {genreName} <span className="text-slate-400 font-normal">({years})</span>
                  </div>
                  <div className="text-xs text-slate-400">
                    results: {row.results_count}
                  </div>
                </div>

                <div className="text-xs text-slate-500">
                  {new Date(row.timestamp).toLocaleString()}
                </div>
              </div>
            );
          })}
        </div>
      </section>
    </main>
  );
}
