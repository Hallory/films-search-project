'use client';

import Skeleton, { SkeletonTheme } from 'react-loading-skeleton';
import 'react-loading-skeleton/dist/skeleton.css';

const FilmCardCompactSkeleton = () => (
  <SkeletonTheme baseColor="#0f172a" highlightColor="#1e293b">
    <div
      className="
        w-[200px] h-[130px]
        shrink-0
        rounded-2xl border border-slate-700/80
        bg-rgba(20,20,20,0.5)
        px-5 py-4
        flex flex-col justify-between
      "
    >
      <div className="flex flex-col gap-2">
        <div className="flex justify-end">
          <Skeleton width={36} height={12} />
        </div>
        <Skeleton width="85%" height={18} />
      </div>

      <div className="flex justify-between text-sm">
        <Skeleton width={60} height={12} />
        <Skeleton width={28} height={12} />
      </div>
    </div>
  </SkeletonTheme>
);

export default FilmCardCompactSkeleton;
