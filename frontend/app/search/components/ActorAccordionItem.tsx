'use client';

import React from 'react';
import Link from 'next/link';
import { AnimatePresence, motion } from 'framer-motion';
import { ChevronDown } from 'lucide-react';

type ActorFilm = {
  film_id: number;
  title: string;
  release_year: number;
};

type ActorHit = {
  actor_id: number;
  full_name: string;
  films: ActorFilm[];
};

function getInitials(fullName: string): string {
  const parts = fullName.split(' ').filter(Boolean);
  if (parts.length === 0) return '?';
  if (parts.length === 1) return parts[0].slice(0, 2).toUpperCase();
  return (parts[0][0] + parts[1][0]).toUpperCase();
}

export default function ActorAccordionItem({ actor }: { actor: ActorHit }) {
  const [open, setOpen] = React.useState(false);

  const previewCount = 6;
  const filmsPreview = actor.films.slice(0, previewCount);
  const hasMore = actor.films.length > previewCount;


  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900/60">
      <button
        type="button"
        onClick={() => setOpen((v) => !v)}
        className="w-full px-4 py-3 flex items-center justify-between"
      >
        <div className="flex items-center gap-3 min-w-0">
          <div className="flex h-9 w-9 shrink-0 items-center justify-center overflow-hidden rounded-full bg-linear-to-br from-slate-700 to-slate-900 text-slate-200 text-xs font-semibold">
            {getInitials(actor.full_name)}
          </div>

          <div className="text-left min-w-0">
            <div className="text-sm font-semibold text-slate-200 truncate">
              <Link href={`/actors/${actor.actor_id}`}>{actor.full_name}</Link>
            </div>
            <div className="text-xs text-slate-400">{actor.films.length} films</div>
          </div>
        </div>

        <ChevronDown
          size={18}
          className={['transition-transform', open ? 'rotate-180' : ''].join(' ')}
        />
      </button>

      <AnimatePresence initial={false}>
        {open && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.18 }}
            className="overflow-hidden"
          >
            <div className="px-4 pb-4 pt-1 space-y-2">
              {filmsPreview.map((film) => (
                <Link
                  key={film.film_id}
                  href={`/films/${film.film_id}`}
                  className="flex items-center justify-between rounded-lg border border-slate-800 px-3 py-2 text-sm text-slate-200 hover:border-slate-600 transition-colors"
                >
                  <span className="truncate">{film.title}</span>
                  <span className="text-xs text-slate-400 ml-3">{film.release_year}</span>
                </Link>
              ))}

              {hasMore && (
                <Link
                  href={`/actors/${actor.actor_id}`}
                  className="inline-flex text-xs text-indigo-300 hover:text-indigo-200 transition-colors pt-2"
                >
                  Show all films →
                </Link>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
