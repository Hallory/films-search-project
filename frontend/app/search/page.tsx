'use client';

import { useRouter, useSearchParams } from 'next/navigation';
import { useQuery } from '@tanstack/react-query';
import { searchAll } from '@/lib/api';
import FilmCardDetailed from '../components/films/FilmCardDetailed';
import FilmCardDetailedSkeleton from '../components/films/skeletons/FilmCardDetailedSkeleton';
import Link from 'next/link';
import ActorAccordionItem from './components/ActorAccordionItem';
import ActorAccordionSkeleton from '../components/films/skeletons/ActorAccordionSkeleton';
import { useState } from 'react';
import { AnimatePresence, motion } from 'framer-motion';
import Pagination from '../components/films/pagination/Pagination';

const FILMS_PER_PAGE = 10;
const skeletons = Array.from({ length: FILMS_PER_PAGE });

export default function SearchPage() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const query = searchParams.get('q') ?? '';
  const pageParam = searchParams.get('page');
  const pageRaw = Number(pageParam);
  const page = Number.isFinite(pageRaw) ? Math.max(1, Math.trunc(pageRaw)) : 1;

  const enabled = query.length > 0;
  const offset = (page - 1) * FILMS_PER_PAGE;

  const { data, isLoading, isError } = useQuery({
    queryKey: ['films', 'search-all', query, page],
    queryFn: () => searchAll(query, FILMS_PER_PAGE, offset),
    enabled,
    placeholderData: (prev) => prev,
  });

  const byTitle = data?.by_title.items ?? [];
  const totalTitles = data?.by_title.count ?? 0;
  const totalPages = Math.max(1, Math.ceil(totalTitles / FILMS_PER_PAGE));
  const actors = data?.by_actor.items ?? [];

  const ACTORS_PREVIEW = 2;
  const [showAllActors, setShowAllActors] = useState(false);



  const actorsWithFilms = actors.filter((a) => a.films.length > 0);

  const actorsToRender = showAllActors
    ? actorsWithFilms
    : actorsWithFilms.slice(0, ACTORS_PREVIEW);

  const hasMoreActors = actorsWithFilms.length > ACTORS_PREVIEW;

  const goToPage = (nextPage: number) => {
    const safePage = Math.max(1, Math.min(nextPage, totalPages));
    if (safePage === page) return;
    const params = new URLSearchParams(searchParams.toString());
    params.set('page', String(safePage));
    router.replace(`/search?${params.toString()}`);
  };


  return (
    <main>
      <div className="mx-auto max-w-6xl px-6 pt-24 pb-12 space-y-8">
        <h1 className="text-2xl font-semibold">Search</h1>


        {query && (
          <p className="text-sm text-slate-400">
            Results for: <span className="font-semibold text-slate-200">{query}</span>
          </p>
        )}

        {isError && <p className="text-red-400 text-sm">Failed to load results.</p>}

        {isLoading && enabled && (
          <div className="space-y-10 flex flex-col gap-4">
            <section className="space-y-4 w-full">
              <div className="flex items-center justify-between">
                <h2 className="text-lg font-semibold">By actor</h2>

                <span className="text-xs text-slate-400">Loading…</span>
              </div>

              <div className="space-y-3">
                {Array.from({ length: 2 }).map((_, idx) => (
                  <ActorAccordionSkeleton key={`actor-sk-${idx}`} />
                ))}
              </div>
            </section>

            <section className="space-y-4 w-full">
              <h2 className="text-lg font-semibold mb-3">By title</h2>

              <div className="grid grid-cols-1 md:grid-cols-1 lg:grid-cols-2 gap-4">
                {skeletons.map((_, idx) => (
                  <FilmCardDetailedSkeleton key={`film-sk-${idx}`} />
                ))}
              </div>
            </section>
          </div>
        )}

        {!isLoading && !isError && enabled && data && (
          <div className="space-y-10 flex flex-col gap-4">
            <section className="space-y-4 w-full">
              <div className="flex items-center justify-between">
                <h2 className="text-lg font-semibold">By actor</h2>

                <span
                  className="relative text-xs text-slate-400 group"
                  aria-label={`Found ${actors.length} actors, ${actorsWithFilms.length} have films`}
                >
                  {actorsWithFilms.length} match{actorsWithFilms.length === 1 ? '' : 'es'} *
                  {actors.length > actorsWithFilms.length && (
                    <span className="pointer-events-none absolute right-0 top-0 -translate-y-7 whitespace-nowrap rounded-md border border-slate-700 bg-slate-900/95 px-2 py-1 text-[11px] text-slate-200 opacity-0 shadow-lg transition group-hover:opacity-100">
                      Found {actors.length} actors, {actorsWithFilms.length} have films
                    </span>
                  )}
                </span>
              </div>
              {hasMoreActors && showAllActors && (
                <button
                  type="button"
                  onClick={() => setShowAllActors((v) => !v)}
                  className="text-xs text-indigo-300 hover:text-indigo-200 transition-colors cursor-pointer"
                >
                  {showAllActors ? 'Show less' : `Show all actors (${actors.length}) →`}
                </button>
              )}
              {actorsWithFilms.length === 0 ? (
                <p className="text-slate-400 text-sm">No films by actor.</p>
              ) : (
                <div className="space-y-4">
                  <motion.div
                    layout="size"
                    transition={{ duration: 0.28, ease: [0.22, 1, 0.36, 1] }}
                    className="space-y-4"
                  >
                    <AnimatePresence initial={false}>
                      {actorsToRender.map((actor) => (
                        <motion.div
                          key={actor.actor_id}
                          layout
                          initial={{ opacity: 0, y: -6 }}
                          animate={{ opacity: 1, y: 0 }}
                          exit={{ opacity: 0, y: -6 }}
                          transition={{ duration: 0.2 }}
                        >
                          <ActorAccordionItem actor={actor} />
                        </motion.div>
                      ))}
                    </AnimatePresence>
                  </motion.div>

                  {hasMoreActors && (
                    <button
                      type="button"
                      onClick={() => setShowAllActors((v) => !v)}
                      className="text-xs text-indigo-300 hover:text-indigo-200 transition-colors cursor-pointer"
                    >
                      {showAllActors
                        ? 'Show less'
                        : `Show all actors (${actorsWithFilms.length}) →`}
                    </button>
                  )}
                </div>
              )}
            </section>

            <section className="space-y-4 w-full">
              <div className="flex items-center justify-between">
              <h2 className="text-lg font-semibold mb-3">By title</h2>
              <span className="text-xs text-slate-400">
              {byTitle.length} match{byTitle.length === 1 ? '' : 'es'} 
              </span>
              </div>

              {byTitle.length === 0 ? (
                <p className="text-slate-400 text-sm">No films by title.</p>
              ) : (
                <>
                  <div className="grid grid-cols-1 md:grid-cols-1 lg:grid-cols-2 gap-4">
                    {byTitle.map((film) => (
                      <Link href={`/films/${film.film_id}`} key={film.film_id} className="w-full">
                        <FilmCardDetailed film={film} />
                      </Link>
                    ))}
                  </div>
                  {totalPages > 1 && (
                    <Pagination page={page} totalPages={totalPages} onPageChange={goToPage} />
                  )}
                </>
              )}
            </section>
          </div>
        )}

        {!isLoading && !isError && enabled && !data && (
          <p className="text-slate-400 text-sm">No results.</p>
        )}
      </div>
    </main>
  );
}
