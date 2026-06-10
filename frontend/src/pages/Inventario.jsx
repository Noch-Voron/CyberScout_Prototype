import { useState, useEffect } from 'react';
import { AppShell } from "../components/AppShell";

export default function Inventario() {
  // 1. Preparamos el estado para guardar los datos del backend
  const [activos, setActivos] = useState([]);

  // 2. Buscamos los datos al cargar la página
  useEffect(() => {
    fetch('http://localhost:8000/api/inventario')
      .then(respuesta => respuesta.json())
      .then(datos => {
        setActivos(datos);
      })
      .catch(error => console.error("Error al traer el inventario:", error));
  }, []);

  // 3. Renderizamos manteniendo el AppShell de Giselle
  return(
    <AppShell>
      <section className="container mx-auto px-4 py-10">
        <div className="flex items-end justify-between flex-wrap gap-4 mb-6">
          <h1 className="text-3xl font-bold">Inventario</h1>
        </div>
        
        {/* Aquí inyectamos la grilla con los servidores */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-6">
          {activos.map((servidor) => (
            <div key={servidor.id} className="bg-white p-5 rounded-lg shadow-md border-l-4 border-blue-600 hover:shadow-lg transition-shadow">
              <h3 className="text-xl font-bold text-gray-800">{servidor.nombre}</h3>
              <p className="text-sm text-gray-500 mb-4 font-mono">{servidor.entorno}</p>
              
              <div className="bg-gray-50 p-3 rounded border border-gray-100">
                <span className="font-semibold text-sm text-gray-700 uppercase tracking-wider">Software Detectado</span>
                <ul className="mt-2 space-y-1 text-sm text-gray-600">
                  {Object.entries(servidor.software_instalado).map(([software, version]) => (
                    <li key={software} className="flex justify-between border-b border-gray-200 pb-1 last:border-0">
                      <span className="capitalize">{software}</span>
                      <span className="font-mono text-blue-600 bg-blue-50 px-2 py-0.5 rounded text-xs">{version}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          ))}
        </div>
      </section>
    </AppShell>
  );
}