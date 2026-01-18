'use client';
import Skeleton, { SkeletonTheme } from 'react-loading-skeleton';

const FilmCardDetailedSkeleton = () => {
  return (
    <SkeletonTheme baseColor="#0f172a" highlightColor="#1e293b">
      <article className="flex flex-col md:flex-row gap-4 rounded-2xl border border-slate-800 bg-slate-900/80 p-4">
        <div className="w-full md:w-40 lg:w-48 shrink-0">
          <div className="relative aspect-2/3 rounded-xl overflow-hidden">
            <Skeleton className="h-full w-full" />
          </div>
        </div>

        <div className="flex-1 space-y-2">
          <header className="space-y-1">
            <Skeleton width="70%" height={18} />
            <Skeleton width="40%" height={12} />
          </header>

          <div className="space-y-1">
            <Skeleton height={12} />
            <Skeleton height={12} />
            <Skeleton width="80%" height={12} />
          </div>

          <div className="flex flex-wrap gap-2 pt-1">
            <Skeleton width={40} height={16} className="rounded-full" />
          </div>
        </div>
      </article>
    </SkeletonTheme>
  );
};

export default FilmCardDetailedSkeleton;
