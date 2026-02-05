import { Film } from '@/lib/api';
import { formatFilmLength } from '@/lib/filmUtils';
import Link from 'next/link';
import React from 'react';
import { motion } from 'framer-motion';
import YouTubePreview from './media/YoutubePreview';
const HOVER_DELAY_MS = 800;

type FilmCardCompactProps = {
  film: Film;
  activePreviewId?: number | null;
  setActivePreviewId?: React.Dispatch<React.SetStateAction<number | null>>;
};

const FilmCardCompact = ({ film, setActivePreviewId, activePreviewId }: FilmCardCompactProps) => {
  const hasPoster = Boolean(film.poster_url);
  const posterUrl = film.poster_url as string | undefined;
  const [shouldPlay, setShouldPlay] = React.useState(false);
  const hoverTimerRef = React.useRef<number | null>(null);
  const hasTrailer = Boolean(film.trailer_key);
  const [isHovered, setIsHovered] = React.useState(false);

  const isActive = activePreviewId === film.film_id;

  const shouldPreview = isHovered && isActive && shouldPlay && hasTrailer;

  const onMouseEnter = () => {
    setIsHovered(true);

    if (setActivePreviewId) {
      setActivePreviewId(film.film_id);
    }

    if (!hasTrailer) return;

    hoverTimerRef.current = window.setTimeout(() => {
      setShouldPlay(true);
    }, HOVER_DELAY_MS);
  };
  const onMouseLeave = () => {
    setIsHovered(false);
    setShouldPlay(false);

    if (setActivePreviewId && activePreviewId === film.film_id) {
      setActivePreviewId(null);
    }

    if (hoverTimerRef.current) {
      window.clearTimeout(hoverTimerRef.current);
      hoverTimerRef.current = null;
    }
  };

  React.useEffect(() => {
    return () => {
      if (hoverTimerRef.current) window.clearTimeout(hoverTimerRef.current);
    };
  }, []);
  const metaVariants = {
    hidden: { opacity: 0, y: 6, transition: { duration: 0.15 } },
    visible: { opacity: 1, y: 0, transition: { duration: 0.18 } },
  };

  return (
    <Link href={`/films/${film.film_id}`} className="relative shrink-0">
      <motion.div
        onMouseEnter={onMouseEnter}
        onMouseLeave={onMouseLeave}
        initial={false}
        animate={{ scale: isHovered ? 1.3 : 1 }}
        transition={{ type: 'spring', stiffness: 400, damping: 40 }}
        className={[
          `
    relative
    w-[200px] h-[130px]
    rounded-2xl border border-slate-700/80
    overflow-hidden
    px-5 py-4
    flex flex-col justify-between
    origin-center
    will-change-transform
  `,
          isHovered ? 'z-50' : 'z-0',
        ].join(' ')}
      >
        <div
          className={[
            'absolute inset-0',
            hasPoster ? 'bg-cover bg-center' : 'bg-slate-900/80',
          ].join(' ')}
          style={hasPoster ? { backgroundImage: `url(${posterUrl})` } : undefined}
        />

        <div
          className={[
            'absolute inset-0 transition-opacity duration-200',
            shouldPreview ? 'opacity-40' : 'opacity-100',
            'bg-linear-to-br from-slate-950/90 via-slate-950/55 to-slate-950/15',
          ].join(' ')}
        />

        {shouldPreview && film.trailer_key && (
          <div className="absolute inset-0 z-10">
            <YouTubePreview videoKey={film.trailer_key} />
            <div className="absolute inset-0 bg-slate-950/20 pointer-events-none" />
          </div>
        )}

        <motion.div layout className={['relative transition-opacity duration-150'].join(' ')}>
          <motion.div
            layout
            className={[
              'mb-1 flex items-center gap-2',
              isHovered ? 'justify-between' : 'flex-col items-center',
            ].join(' ')}
          >
            <motion.h3
              layout
              className={[
                'text-white',
                isHovered
                  ? 'text-sm font-semibold text-left flex-1 truncate z-10'
                  : 'text-lg text-center w-full',
              ].join(' ')}
            >
              {film.title}
            </motion.h3>

            <motion.span
              layout
              className={[
                'text-slate-300/90',
                isHovered ? 'text-xs shrink-0 z-10' : 'text-xs order-first ',
              ].join(' ')}
            >
              {film.release_year}
            </motion.span>
          </motion.div>

          <motion.div
            layout
            variants={metaVariants}
            initial={false}
            animate={!shouldPreview ? 'visible' : 'hidden'}
            className="text-sm w-full text-slate-200/80 flex gap-4 justify-between"
          >
            <span>{formatFilmLength(film.length ?? 0)}</span>
            <span>{film.rating ?? '-'}</span>
          </motion.div>
        </motion.div>
      </motion.div>
    </Link>
  );
};

export default FilmCardCompact;
