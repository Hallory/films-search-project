import { FilmsResponse } from '@/lib/api';
import { useQuery } from '@tanstack/react-query';
import React, { useRef } from 'react';
import { ChevronLeftIcon, ChevronRightIcon } from '@heroicons/react/24/outline';
import FilmCardCompact from './FilmCardCompact';

type FilmsRowProps = {
  title: string;
  queryKey: (string | number)[];
  queryFn: () => Promise<FilmsResponse>;
};

const FilmsRow = ({ title, queryKey, queryFn }: FilmsRowProps) => {
  const listRef = useRef<HTMLDivElement | null>(null);

  const { data, isLoading, isError } = useQuery({
    queryKey,
    queryFn,
  }); 

  const films = data?.items ?? [];

  const scroll = (direction: 'left' | 'right') => {
    const node = listRef.current;
    if (!node) return;

    const amount = node.clientWidth * 0.9;

    node.scrollBy({
      left: direction === 'left' ? -amount : amount,
      behavior: 'smooth',
    });
  };

  return (
    <section className="space-y-4">
      <h2 className="text-lg font-semibold">{title}</h2>

      {isLoading && <p className="text-slate-400 text-sm">Loading...</p>}
      {isError && <p className="text-slate-400 text-sm">Error</p>}
      {!isLoading && !isError && films.length === 0 && (
        <p className="text-slate-400 text-sm">No films found</p>
      )}

      {!isLoading && !isError && films.length > 0 && (
  <div className="relative">
    <button
      type="button"
      onClick={() => scroll("left")}
      className="
        hidden md:flex
        absolute top-0 bottom-0 -left-6 z-10
        w-16 items-center justify-center
        bg-linear-to-r from-slate-950 via-slate-950/80 to-transparent
        hover:from-slate-900 hover:via-slate-900/80
        transition
      "
    >
      
      <ChevronLeftIcon className="h-6 w-6" />
    </button>

    <button
      type="button"
      onClick={() => scroll("right")}
      className="
        hidden md:flex
        absolute top-0 bottom-0 -right-6 z-10
        w-16 items-center justify-center
        bg-linear-to-l from-slate-950 via-slate-950/80 to-transparent
        hover:from-slate-900 hover:via-slate-900/80
        transition
      "
    >
      <ChevronRightIcon className="h-6 w-6" />
    </button>

    <div
      ref={listRef}
      className="
        flex gap-4 overflow-x-auto
        scroll-smooth select-none [&::-webkit-scrollbar]:hidden
        px-6
      "
    >
      {films.map((film) => (
        <FilmCardCompact key={film.film_id} film={film} />
      ))}
          </div>

          <div className="pointer-events-none absolute inset-y-0 left-0 w-16 bg-linear-to-r from-slate-950 to-transparent" />
          <div className="pointer-events-none absolute inset-y-0 right-0 w-16 bg-linear-to-l from-slate-950 to-transparent" />
        </div>
      )}
    </section>
  );
};

export default FilmsRow;
