import type { Film, FilmDetail } from '@/lib/api';
import { formatFilmMeta } from '@/lib/filmUtils';
import Image from 'next/image';

type FilmCardDetailedProps = {
  film: Film;
};

const FilmCardDetailed = ({ film }: FilmCardDetailedProps) => {
  return (
    <article className="flex flex-col md:flex-row gap-4 rounded-2xl border border-slate-800 bg-slate-900/80 p-4 hover:bg-slate-800/80 transition">
      <div className="w-full md:w-40 lg:w-48 shrink-0">
        <div className="relative aspect-2/3 rounded-xl overflow-hidden bg-linear-to-br from-slate-700 to-slate-900">
          {film.poster_url && (
            <Image
              src={film.poster_url}
              alt={film.title}
              fill
              className="object-cover object-center"
            />
          )}
        </div>
      </div>

      <div className="flex-1 space-y-2">
        <header className="space-y-1">
          <h2 className="text-base md:text-lg font-semibold">{film.title}</h2>
          <p className="text-xs text-slate-400">{formatFilmMeta(film)}</p>
        </header>

        {film.description && (
          <p className="text-sm text-slate-300 line-clamp-3 md:line-clamp-4">{film.description}</p>
        )}

        <div className="flex flex-wrap items-center gap-2 pt-1">
          {film.rating && (
            <span className="inline-flex items-center rounded-full border border-slate-600 px-2 py-0.5 text-[10px] font-semibold text-slate-200">
              {film.rating}
            </span>
          )}
        </div>
      </div>
    </article>
  );
};

export default FilmCardDetailed;
