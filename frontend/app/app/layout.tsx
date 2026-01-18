import type { Metadata } from "next";
import "../styles/globals.css";
import { Providers } from "./Providers";
import Header from "./components/layout/Header";


export const metadata: Metadata = {
  title: "Films App",
  description: "Learning project for Python and Databases ",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="text-slate-50"
      >
        <main className="min-h-screen bg-slate-950 text-slate-50 mt-8">
        <Providers>
          <Header />
          {children}
        </Providers></main>
      </body>
    </html>
  );
}
