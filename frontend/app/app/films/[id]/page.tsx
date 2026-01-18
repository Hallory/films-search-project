'use client';
import ActorCard from '@/app/components/films/ActorCardCompact';
import FilmsPageSkeleton from '@/app/components/films/skeletons/FilmsPageSkeleton';
import { FilmDetail, getFilm, logFilmView } from '@/lib/api';
import { formatFilmLength } from '@/lib/filmUtils';
import { useQuery } from '@tanstack/react-query';
import Image from 'next/image';
import Link from 'next/link';
import { useParams } from 'next/navigation';
import { useEffect, useRef } from 'react';

const Film = () => {
  const params = useParams();
  const filmId = Number(params?.id);
  const isValid = Number.isFinite(filmId);

  const loggedRef = useRef(false);

  const { data: film, isLoading } = useQuery<FilmDetail>({
    queryKey: ['film', filmId],
    queryFn: () => getFilm(filmId),
    enabled: isValid,
  });

  useEffect(() => {
    if (!filmId || loggedRef.current) return;
    loggedRef.current = true;
    logFilmView(filmId);
  }, [filmId]);


  return (
    <div className="text-slate-50 pt-[120px] flex flex-col items-center max-w-6xl mx-auto">
      {isLoading && <FilmsPageSkeleton />}

      {film && (
        <div className="flex flex-col w-full gap-12 ">
          <div className="flex justify-between ">
            <h2 className="text-3xl font-semibold">{film.title}</h2>
          </div>
          <div className="flex  gap-4 justify-between">
            <div className="relative w-full max-w-60 aspect-2/3 rounded-xl overflow-hidden bg-linear-to-br from-slate-700 to-slate-900">
              {film.poster_url && (
                <Image
                  src={film.poster_url}
                  alt={film.title}
                  fill
                  className="object-cover object-center"
                />
              )}
            </div>
            <div className="flex flex-col justify-between">
              <div className="flex flex-col gap-1 max-w-full">
                <p>Release year: {film?.release_year}</p>
                <p>Rating: {film?.rating}</p>
                <p>Length: {formatFilmLength(film?.length)}</p>
                {film.genres?.length ? (
                  <div className="flex flex-wrap gap-2">
                    {film.genres.map((g) => (
                      <Link key={g.genre_id ?? g.genre_id ?? g.name} href={`/genres/${g.genre_id}`} className='hover:opacity-80'>
                      <span
                        className="px-2 py-1 rounded-lg bg-white/10 text-xs text-white/80"
                      >
                        {g.name}
                      </span>
                      </Link>
                    ))}
                  </div>
                ) : null}
              </div>
              <span className="flex flex-col gap-2">
                {film.director?.full_name ? <p>Director: {film.director.full_name}</p> : null}
                <p>About the film:</p> {film?.description}
              </span>
            </div>
          </div>
          <div className="flex flex-wrap gap-2">
            {film.actors.map((actor) => (
              <Link
                className="cursor-pointer hover:opacity-80"
                href={`/actors/${actor.actor_id}`}
                key={actor.actor_id}
              >
                <ActorCard actor={actor} />
              </Link>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default Film;
