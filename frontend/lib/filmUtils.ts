import { Film } from "./api";

const formatFilmLength = (length: number | null): string => {
    if (!length) return "—";
    const hours = Math.floor(length / 60);
    const minutes = length % 60;
    if(!hours) return `${minutes}min`;
    return `${hours}h ${minutes}min`;
};

const formatFilmMeta = (film:Film):string =>{
    const parts: string[] = [];
    if(film.release_year) parts.push(String(film.release_year));
    if(film.length) parts.push(formatFilmLength(film.length));
    if(film.rating) parts.push(film.rating);
    return parts.join(" • ");

}

export { formatFilmLength, formatFilmMeta };