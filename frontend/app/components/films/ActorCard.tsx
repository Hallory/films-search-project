import Image from 'next/image';
import React from 'react';
type Actor = {
  actor_id: number;
  full_name: string;
  photo_url?: string | null;
  character?: string | null;
}

interface ActorCardProps {
  actor: Actor;
}
const ActorCard = ({ actor }: ActorCardProps) => {
    return (
        <div className="flex gap-10 px-2 py-1.5 hover:bg-white/5 transition">
            {actor.photo_url ? (
                <Image
                    src={actor.photo_url}
                    alt={actor.full_name}
                    width={136}
                    height={136}
                    className="rounded-sm"
                />
            ) : (
                <div className="h-9 w-9 rounded-full bg-slate-800 flex items-center justify-center">
                    <span className="text-slate-400">👤</span>
                </div>
            )}
            <div className="flex-1">
                <p className="text-sm font-semibold">{actor.full_name}</p>
                <p className="text-xs text-slate-400">{actor.character}</p>
            </div>
        </div>
    );
};

export default ActorCard;