"use client";

import { FilmsResponse, searchFilmsByKeyword } from "@/lib/api";
import { useDebounce } from "@/lib/useDebounce";
import { MagnifyingGlassIcon } from "@heroicons/react/24/outline";
import { useQuery } from "@tanstack/react-query";
import { useRouter } from "next/navigation";
import React from "react";

type SearchBarProps = {
  placeholder?: string;
  withSuggestions?: boolean;
  clearOnSubmit?: boolean;
  initialQuery?: string;
};

const SearchBar = ({
  placeholder = "Title, actors, genres",
  withSuggestions = true,
  clearOnSubmit = false,
  initialQuery = "",
}: SearchBarProps) => {
  const router = useRouter();
  

  const [query, setQuery] = React.useState(initialQuery);
  const debounced = useDebounce(query, 400);

  const { data, isLoading } = useQuery<FilmsResponse>({
    queryKey: ["films", "search", debounced],
    queryFn: () => searchFilmsByKeyword(debounced, 0, 5),
    enabled: withSuggestions && debounced.length >= 2, 
  });

  const suggestions = data?.items ?? [];

  const resetSearch = ()=>{
    if(clearOnSubmit){
      setQuery("");
    }
  }

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!query.trim()) return;
    router.push(`/search?q=${encodeURIComponent(query.trim())}`);
    resetSearch();
  };

 

  return (
    <div className="relative w-full max-w-xl">
      <form onSubmit={handleSubmit}>
        <div className="flex items-center gap-2 rounded-full border border-slate-600 bg-slate-900/80 px-3 py-2">
          <MagnifyingGlassIcon className="h-5 w-5 text-slate-300" />
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder={placeholder}
            className="w-full bg-transparent text-sm outline-none placeholder:text-slate-500"
          />
          <button
            type="submit"
            className="text-xs font-semibold uppercase tracking-wide text-slate-300 hover:text-white"
          >
            Search
          </button>
        </div>
      </form>

      {withSuggestions &&
        query.length >= 2 &&
        (isLoading || suggestions.length > 0) && (
          <div className="absolute left-0 right-0 mt-2 rounded-xl border border-slate-700 bg-slate-900/95 shadow-xl backdrop-blur">
            {isLoading && (
              <div className="px-4 py-3 text-sm text-slate-400">
                Searching…
              </div>
            )}

            {!isLoading &&
              suggestions.map((film) => (
                <button
                  key={film.film_id}
                  type="button"
                  onClick={() =>{
                    router.push(
                      `/search?q=${encodeURIComponent(film.title)}`
                    );
                    resetSearch();
                  }}
                  className="w-full px-4 py-2 text-left text-sm text-slate-300 hover:bg-slate-800 hover:text-white first:rounded-t-xl last:rounded-b-xl"
                >
                  <span className="truncate">
                    {film.title}
                    {film.release_year && (
                      <span className="ml-2 text-xs text-slate-400">
                        ({film.release_year})
                      </span>
                    )}
                    {film.rating && (
                      <span className="ml-2 text-xs text-slate-400">
                        ({film.rating})
                      </span>
                    )}
                  </span>
                </button>
              ))}

            {!isLoading && suggestions.length === 0 && (
              <div className="px-4 py-3 text-sm text-slate-400">
                No films found
              </div>
            )}
          </div>
        )}
    </div>
  );
};

export default SearchBar;
