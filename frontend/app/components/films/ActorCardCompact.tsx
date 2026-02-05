import { User } from 'lucide-react';
import Image from 'next/image';
type Actor = {
  actor_id: number;
  full_name: string;
  photo_url?: string | null;
  character?: string | null;
};

interface ActorCardProps {
  actor: Actor;
}
const ActorCardCompact = ({ actor }: ActorCardProps) => {
  return (
    <div className="flex items-center gap-3 rounded-xl px-2 py-1.5 hover:bg-white/5 transition">
      {actor.photo_url ? (
        <Image
          src={actor.photo_url}
          alt={actor.full_name}
          width={36}
          height={36}
          className="rounded-full"
        />
      ) : (
        <div className="h-9 w-9 rounded-full bg-slate-800 flex items-center justify-center">
          <User className="text-slate-400" />
        </div>
      )}
      <div className="flex-1">
        <p className="text-sm font-semibold">{actor.full_name}</p>
        <p className="text-xs text-slate-400">{actor.character}</p>
      </div>
    </div>
  );
};

export default ActorCardCompact;
