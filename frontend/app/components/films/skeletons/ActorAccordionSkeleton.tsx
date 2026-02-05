import React from 'react';

const ActorAccordionSkeleton = () => {
  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900/60 px-4 py-3 animate-pulse">
      <div className="flex items-center gap-3">
        <div className="h-9 w-9 rounded-full bg-slate-800" />
        <div className="flex-1">
          <div className="h-3 w-40 bg-slate-800 rounded" />
          <div className="h-2 w-20 bg-slate-800 rounded mt-2" />
        </div>
      </div>
    </div>
  );
};

export default ActorAccordionSkeleton;
