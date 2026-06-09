// src/hooks/useFuentes.js
import { useState, useEffect } from "./hooks";

export function use_getFuentes() {
  const [fuentes, setFuentes] = useState([]);
  const [error, setError] = useState(null);

  const getFuentes = async () => {
    try {
      const response = await fetch("http://localhost:8000/api/fuentes");
      const data = await response.json();
      setFuentes(data);
    } catch (err) {
      console.error("Error fetching Fuentes:", err);
      setError(err);
    }
  };

  useEffect(() => {
    getFuentes();
  }, []);
  return { fuentes, error, refetch: getFuentes };
}

export function use_getFuente_id(id) {
  const [fuente, setFuente] = useState(null);
  const [error, setError] = useState(null);

  const getFuente_id = async () => {
    try {
      const response = await fetch(`http://localhost:8000/api/fuentes/${id}`);
      const data = await response.json();
      setFuente(data);
    } catch (err) {
      console.error("Error fetching Fuente_id:", err);
      setError(err);
    }
  };

  useEffect(() => {
    if(id){
    getFuente_id();
  }}, [id]);
  return { fuente, error, refetch: getFuente_id };
}

export async function addFuente(url) {
  const response = await fetch(
    "http://localhost:8000/api/fuentes",
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        url: url,
      }),
    }
  );

  return await response.json();
}

export async function deleteFuente(id) {
  const response = await fetch(
    `http://localhost:8000/api/fuentes/${id}`,
    {
      method: "DELETE",
    }
  );

  return await response.json();
}