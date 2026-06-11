import { useState, useEffect } from "react";

const STORAGE_KEY = "inventario_local";

export function useActivos() {
  const [activos, setActivos] = useState([]);

  useEffect(() => {
    const saved = localStorage.getItem(STORAGE_KEY);

    if (saved) {
      try {
        setActivos(JSON.parse(saved));
      } catch {
        setActivos([]);
      }
    }
  }, []);

  const guardar = (nuevosActivos) => {
    setActivos(nuevosActivos);

    localStorage.setItem(
      STORAGE_KEY,
      JSON.stringify(nuevosActivos)
    );
  };

  const importar = (nuevosActivos) => {
    guardar(nuevosActivos);
  };

  const eliminar = (id) => {
    guardar(
      activos.filter((a) => a.id !== id)
    );
  };

  return {
    activos,
    importar,
    eliminar,
  };
}