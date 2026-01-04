import { Film } from '@/lib/api';
import React from 'react';

import { formatFilmLength } from '@/lib/filmUtils';
import Link from 'next/link';

type FilmCardCompactProps = {
  film: Film;
};
const FilmCardCompact = ({ film }: FilmCardCompactProps) => {
  return (
    <Link  href={`/films/${film.film_id}`} className='hover:opacity-80 transition min-w-[180px] max-w-[200px]
        shrink-0
        rounded-2xl border border-slate-700/80
        bg-slate-900/80
        px-5 py-4
        hover:bg-slate-800/80 flex flex-col justify-between'>
    
        <div className="flex justify-between flex-wrap items-center gap-4 mb-1">
          <span className="text-xs text-right w-full max-h-2 text-slate-400">
            {film.release_year}
          </span>
          <h3 className="text-lg w-full">{film.title}</h3>
        </div>
        <div className="text-sm w-full text-slate-400 flex gap-4 justify-between ">
          <span>{formatFilmLength(film.length ?? 0)}</span>
          <span>{film.rating ?? '-'}</span>
      </div>
        </Link>
  );
};

export default FilmCardCompact;
