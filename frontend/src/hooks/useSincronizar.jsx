import { useState, useEffect } from "react";

const DEFAULT_INVENTARIO = [
  {
    nombre: "SRV-PROD-FEDORA",
    id: "srv-001",
    entorno: "Linux Fedora 42 (goated)",
    software_instalado: {
      nginx: "1.18.0",
      python: "3.10.4",
      postgresql: "15.2.0"
    }
  },
  {
    nombre: "SRV-LEGACY-WIN",
    id: "srv-002",
    entorno: "Windows Server 2019 (trash)",
    software_instalado: {
      apache: "2.4.49",
      java: "1.8.0",
      postgresql: "11.5.0"
    }
  }
];

export function useSincronizar() {
  const [alertas, setAlertas] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Initialize localStorage and load stored alerts on mount
  useEffect(() => {
    const storedInventario = localStorage.getItem("inventario");
    if (!storedInventario) {
      localStorage.setItem("inventario", JSON.stringify(DEFAULT_INVENTARIO));
    }

    const storedLastId = localStorage.getItem("id_ultima_noticia");
    if (storedLastId === null) {
      localStorage.setItem("id_ultima_noticia", "0");
    }

    const storedAlertas = localStorage.getItem("alertas_sincronizadas");
    if (storedAlertas) {
      try {
        setAlertas(JSON.parse(storedAlertas));
      } catch (e) {
        console.error("Error parsing stored alerts:", e);
      }
    }
  }, []);

  const sincronizar = async () => {
    setLoading(true);
    setError(null);
    try {
      const inventario = JSON.parse(localStorage.getItem("inventario") || JSON.stringify(DEFAULT_INVENTARIO));
      const lastIdStr = localStorage.getItem("id_ultima_noticia") || "0";
      const idUltimaNoticia = parseInt(lastIdStr, 10);

      const response = await fetch("http://localhost:8000/api/v1/sincronizar", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          id_ultima_noticia: idUltimaNoticia,
          inventario_local: inventario
        })
      });

      if (!response.ok) {
        throw new Error(`Error en servidor: ${response.statusText}`);
      }

      const data = await response.json();
      const { nuevas_alertas, id_ultimo_sincronizado } = data;

      let updatedAlertas = [];
      const storedAlertas = localStorage.getItem("alertas_sincronizadas");
      if (storedAlertas) {
        try {
          updatedAlertas = JSON.parse(storedAlertas);
        } catch (e) {
          updatedAlertas = [];
        }
      }

      if (nuevas_alertas && nuevas_alertas.length > 0) {
        // Append new alerts while preventing duplicates (by news ID, server ID, and affected software)
        const existingKeys = new Set(
          updatedAlertas.map(a => `${a.noticia_id}-${a.id_servidor}-${a.software_afectado}`)
        );

        const filteredNuevas = nuevas_alertas.filter(a => {
          const key = `${a.noticia_id}-${a.id_servidor}-${a.software_afectado}`;
          if (existingKeys.has(key)) return false;
          existingKeys.add(key);
          return true;
        });

        updatedAlertas = [...filteredNuevas, ...updatedAlertas];
        setAlertas(updatedAlertas);
        localStorage.setItem("alertas_sincronizadas", JSON.stringify(updatedAlertas));
      }

      localStorage.setItem("id_ultima_noticia", id_ultimo_sincronizado.toString());
    } catch (err) {
      console.error("Error during synchronization:", err);
      setError(err.message || err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const timer = setTimeout(() => {
      sincronizar();
    }, 100);
    return () => clearTimeout(timer);
  }, []);

  return { alertas, sincronizar, loading, error };
}
