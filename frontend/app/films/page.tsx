'use client';
import { searchFilmsByGenreAndYears } from '@/lib/api';
import { useQuery } from '@tanstack/react-query';
import { useRouter, useSearchParams } from 'next/navigation';
import FilmCardDetailed from '../components/films/FilmCardDetailed';
import Pagination from '../components/films/pagination/Pagination';
import FilmCardDetailedSkeleton from '../components/films/skeletons/FilmCardDetailedSkeleton';
import Link from 'next/link';

const FILMS_PER_PAGE = 10;
const DEFAULT_YEAR_FROM = 1990;
const DEFAULT_YEAR_TO = 2025;
const FilmsPage = () => {
  const asInt = (value: string | null, fallback: number) => {
    const n = Number(value);
    return Number.isFinite(n) ? Math.trunc(n) : fallback;
  };

  const asIntOrNull = (value: string | null) => {
    const n = Number(value);
    return Number.isFinite(n) ? Math.trunc(n) : null;
  };

  const clamp = (value: number, min: number, max: number) => Math.min(Math.max(value, min), max);
  const searchParams = useSearchParams();
  const router = useRouter();

  const genreIdParam = searchParams.get('genreId');
  const yearFromParam = searchParams.get('yearFrom');
  const yearToParam = searchParams.get('yearTo');
  const pageParam = searchParams.get('page');

  const selectedGenreId = asIntOrNull(genreIdParam);
  const yearFromRaw = asInt(yearFromParam, DEFAULT_YEAR_FROM);
  const yearToRaw = asInt(yearToParam, DEFAULT_YEAR_TO);

  const yearFrom = Math.min(yearFromRaw, yearToRaw);
  const yearTo = Math.max(yearFromRaw, yearToRaw);

  const pageRaw = asInt(pageParam, 1);
  const page = Math.max(1, pageRaw);

  const offset = (page - 1) * FILMS_PER_PAGE;

  const {
    data: filmsData,
    isLoading,
    isError,
  } = useQuery({
    queryKey: ['films', 'byGenre', selectedGenreId, yearFrom, yearTo, page],
    queryFn: () =>
      searchFilmsByGenreAndYears(
        selectedGenreId as number,
        yearFrom,
        yearTo,
        offset,
        FILMS_PER_PAGE,
      ),
    enabled: selectedGenreId !== null,
    placeholderData:(prev) => prev
  });

  const films = filmsData?.items ?? [];
  const total = filmsData?.count ?? 0;
  const totalPages = Math.max(1, Math.ceil(total / FILMS_PER_PAGE));

  const updateParams = (updates: {
    genreId?: number | null;
    yearFrom?: number;
    yearTo?: number;
    page?: number;
  }) => {
    const params = new URLSearchParams(searchParams.toString());

    if (updates.genreId !== undefined) {
      if (updates.genreId === null) {
        params.delete('genreId');
      } else {
        params.set('genreId', String(updates.genreId));
      }
    }

    if (updates.yearFrom !== undefined) {
      params.set('yearFrom', String(updates.yearFrom));
    }
    if (updates.yearTo !== undefined) {
      params.set('yearTo', String(updates.yearTo));
    }
    if (updates.page !== undefined) {
      params.set('page', String(updates.page));
    }

    router.replace(`/films?${params.toString()}`);
  };
  const skeletons = Array.from({ length: FILMS_PER_PAGE });
  const goToPage = (nextPage: number) => {
    const p = clamp(page, 1, totalPages);
    if (p === nextPage) return;
    updateParams({ page: nextPage, yearFrom, yearTo });
  };

  if (selectedGenreId === null) {
  return <div className="max-w-6xl mx-auto pt-24 text-slate-300">Select genre first</div>;
}

if (isError) {
  return <div className="max-w-6xl mx-auto pt-24 text-red-300">Error loading films</div>;
}
return (
  <div className="max-w-6xl mx-auto pt-24">
    
    <div className="grid grid-cols-2 gap-4">
      {isLoading
        ? skeletons.map((_, idx) => (
            <FilmCardDetailedSkeleton key={`sk-${idx}`} />
          ))
        : films.length === 0
          ? null
          : films.map((f) => (
              <div key={f.film_id}>
                <Link href={`/films/${f.film_id}`}>
                <FilmCardDetailed film={f} />
                </Link>
              </div>
            ))}
    </div>

    {!isLoading && films.length === 0 && (
      <div className="text-slate-300 mt-6">No films found</div>
    )}

    {totalPages > 1 && (
      <Pagination page={page} totalPages={totalPages} onPageChange={goToPage} />
    )}
  </div>
);

};

export default FilmsPage;
