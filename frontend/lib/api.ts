import axios from "axios";
const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || "http://127.0.0.1:8000";


export const api = axios.create({
    baseURL: API_BASE
})

export type Film = {
    film_id: number;
    title: string;
    description: string
    release_year: number;
    length: number | null;
    rating: string | null;
}

export type Films = {
    films: Film[];
    count: number;
    offset: number;
    limit: number;
}

export type FilmsResponse = {
    items: Film[];
    offset: number;
    limit: number;
    count: number;
}


export type GenresResponse = {
    items: Genre[];
    count: number;
}
export type Genre = {
    category_id: number ;
    name: string;
}


export async function fetchLatestFilms(offset = 0, limit = 10): Promise<FilmsResponse> {
    const res = await api.get(`/films/latest`, { params: { offset, limit } });
    return res.data;
}

export async function searchFilmsByKeyword(keyword: string, offset = 0, limit = 10): Promise<FilmsResponse> {
    const res = await api.get(`/films/search/keyword`, { params: { keyword, offset, limit } });
    return res.data;
}

export async function getGenres(): Promise<GenresResponse> {
  const res = await api.get("/films/genres");
  return res.data;
}

export async function getPopularFilms(limit: number): Promise<FilmsResponse> {
    const res = await api.get(`/films/popular`, { params: { limit } });
    return res.data;
    
}

