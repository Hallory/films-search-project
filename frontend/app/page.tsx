'use client';
import { fetchLatestFilms, getPopularFilms } from '@/lib/api';
import FilmsRow from './components/layout/films/FilmsRow';

export default function Home() {
  return (
    <main className="">
      <div className="max-w-[calc(100%-2rem)] flex flex-col gap-10 mx-auto py-8 px-4 pt-24">
        <FilmsRow
          queryFn={() => getPopularFilms(10)}
          queryKey={['films', 'popular']}
          title="Popular Films"
        />
        <FilmsRow
          queryFn={() => fetchLatestFilms(0, 20)}   
          queryKey={['films', 'latest']}
          title="Latest Films"
        />
      </div>
    </main>
  );
}
