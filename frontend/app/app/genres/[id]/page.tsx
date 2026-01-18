'use client';

import { useParams } from 'next/navigation';
import { useQuery } from '@tanstack/react-query';
import { searchFilmsByGenreAndYears, getGenres } from '@/lib/api';
import FilmCardDetailed from '../../components/films/FilmCardDetailed';
import Pagination from '@/app/components/films/pagination/Pagination';
import Link from 'next/link';
import { useEffect, useRef, useState } from 'react';

export default function GenrePage() {
  const LIMIT = 20;
  const [page, setPage] = useState(1);
  const offset = (page - 1) * LIMIT;
  const params = useParams();
  const genreId = Number(params?.id);

  const { data: genres } = useQuery({
    queryKey: ['genres'],
    queryFn: getGenres,
  });

  const pageRef = useRef(1);

  useEffect(() => {
    pageRef.current = 1;
  }, [genreId]);
  const { data, isLoading } = useQuery({
    queryKey: ['films', 'genre', genreId, page],
    queryFn: () => searchFilmsByGenreAndYears(genreId, 1900, 2100, offset, LIMIT),
    enabled: Number.isFinite(genreId),
  });
  const genreName = genres?.items?.find((g) => g.genre_id === genreId)?.name ?? 'Genre';
  const total = data?.count ?? 0;
  const totalPages = Math.max(1, Math.ceil(total / LIMIT));

  return (
    <div className="pt-[120px] max-w-6xl mx-auto text-slate-50">
      <h1 className="text-3xl font-semibold">{genreName}</h1>

      {isLoading ? <div className="mt-6 text-white/70">Loading…</div> : null}

      <div className="mt-6 grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-4">
        {(data?.items ?? []).map((f) => (
          <Link
            key={f.film_id}
            href={`/films/${f.film_id}`}
            className="rounded-xl overflow-hidden bg-white/5"
          >
            <div className="rounded-xl overflow-hidden bg-white/5">
              <FilmCardDetailed film={f} />
              <div className="p-3 text-sm">
                <p className="text-slate-300">
                  {f.title}({f.release_year})
                </p>
              </div>
            </div>
          </Link>
        ))}
      </div>
      <Pagination page={page} totalPages={totalPages} onPageChange={setPage} />
    </div>
  );
}
