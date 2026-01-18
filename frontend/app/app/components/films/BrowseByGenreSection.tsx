'use client';
import { Genre, getGenres, FilmsResponse, searchFilmsByGenreAndYears } from '@/lib/api';
import { useQuery } from '@tanstack/react-query';
import React, { useState } from 'react';

const FILMS_PER_PAGE = 10;
const BrowseByGenreSection = () => {
  const [selectedGenreId, setSelectedGenreId] = useState<number | null>(null);
  const [yearFrom, setYearFrom] = useState<number>(1990);
  const [yearTo, setYearTo] = useState<number>(2025);
  const [page, setPage] = useState(1);

  const offset = (page - 1) * FILMS_PER_PAGE;

  const {
    data: genresData,
    isLoading,
    isError,
  } = useQuery({
    queryKey: ['search', 'genre'],
    queryFn: getGenres,
  });

  const genres: Genre[] = genresData?.items ?? [];

  const handleGenreChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const value = e.target.value;
    setSelectedGenreId(value ? Number(value) : null);
  };

  const handleYearFromChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setYearFrom(Number(e.target.value || yearFrom));
  };

  const handleYearToChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setYearTo(Number(e.target.value || yearTo));
  };

  return (
    <section className="space-y-4">
      <h2>Browse by genre</h2>

      <div className="flex flex-wrap items-center gap-4 text-sm">
        <label className="flex items-center gap-2">
          <span className="text-slate-300">Genre:</span>
          <select
            value={selectedGenreId ?? ''}
            onChange={handleGenreChange}
            className="rounded-md bg-slate-900 border border-slate-700 px-3 py-1 text-sm"
          >
            <option value="">Select Genre</option>
            {genres.map((g) => (
              <option key={g.category_id} value={g.category_id}>
                {g.name}
              </option>
            ))}
          </select>
        </label>
        <label className="flex items-center gap-2">
          <span className="text-slate-300">Year from:</span>
          <input
            type="number"
            min={1990}
            max={2025}
            value={yearFrom}
            onChange={handleYearFromChange}
            className="w-24 rounded-md bg-slate-900 border border-slate-700 px-2 py-1 text-sm"
          />
        </label>
        <label className="flex items-center gap-2">
          <span className="text-slate-300">Year To:</span>
          <input
            type="number"
            min={1990}
            max={2025}
            value={yearTo}
            onChange={handleYearToChange}
            className="w-24 rounded-md bg-slate-900 border border-slate-700 px-2 py-1 text-sm"
          />
        </label>
      </div>
    </section>
  );
};

export default BrowseByGenreSection;
