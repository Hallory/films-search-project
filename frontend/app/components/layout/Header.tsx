'use client';
import Link from 'next/link';
import SearchBar from '@/components/search/SearchBar';

const Header = () => {
  return (
    <header className="fixed  top-0 z-20 w-full border-slate-800/70 bg-slate-950/70 backdrop-blur">
      <div className="mx-auto max-w-full pt-4 pb-8 px-4 flex justify-between items-center">
        <Link href="/" className="flex items-center gap-2">
          <div className="h-8 w-12 rounded-xl bg-linear-to-br from-indigo-500 to-violet-500 shadow-lg shadow-indigo-500/30">
            <span className="text-2xl font-semibold tracking-tight">Films Scope</span>
          </div>
        </Link>
        <nav className="flex items-center gap-6 text-sm text-slate-300">
          <SearchBar clearOnSubmit />
          <Link className="hover:text-white transition-colors" href="/">
            Account
          </Link>
          <span className="rounded-full border border-slate-700 px-3 py-1 text-[11px] uppercase tracking-wide text-slate-400">
            beta
          </span>
        </nav>
      </div>
    </header>
  );
};

export default Header;
