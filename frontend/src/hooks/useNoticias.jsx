// src/hooks/useNoticias.js
import { useState, useEffect } from "./hooks";

export function use_getNoticias() {
  const [noticias, setNoticias] = useState([]);
  const [error, setError] = useState(null);

  const getNoticias = async () => {
    try {
      const response = await fetch("http://localhost:8000/api/noticias");
      const data = await response.json();
      setNoticias(data);
    } catch (err) {
      console.error("Error fetching noticias:", err);
      setError(err);
    }
  };

  useEffect(() => {
    getNoticias();
  }, []);
  return { noticias, error, refetch: getNoticias };
}

export function use_getNoticia_id(id) {
  const [noticia, setNoticia] = useState(null);
  const [error, setError] = useState(null);

  const getNoticia_id = async () => {
    try {
      const response = await fetch(`http://localhost:8000/api/noticias/${id}`);
      const data = await response.json();
      setNoticia(data);
    } catch (err) {
      console.error("Error fetching noticia_id:", err);
      setError(err);
    }
  };

  useEffect(() => {
    if(id){
    getNoticia_id();
  }}, [id]);
  return { noticia, error, refetch: getNoticia_id };
}
