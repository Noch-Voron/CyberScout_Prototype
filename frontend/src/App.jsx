import { useEffect, useState, useRef } from 'react';
import './App.css';

function App() {
  const [alertas, setAlertas] = useState([]);
  const [inventario, setInventario] = useState([]);
  const ultimoIdRef = useRef(0); // Usamos useRef para el ID para evitar dependencias circulares en useEffect

  // 1. Inicialización: Cargar inventario simulado y sincronizar backlog
  useEffect(() => {
    // Inventario quemado inicial para la demo (simulando que se sacó del localStorage)
    const inventarioDemo = [
      {
        nombre: "SRV-PROD-FEDORA",
        id: "srv-001",
        entorno: "Linux Fedora 42 (goated)",
        software_instalado: { "nginx": "1.18.0", "python": "3.10.4", "postgresql": "15.2.0" }
      },
      {
        nombre: "SRV-LEGACY-WIN",
        id: "srv-002",
        entorno: "Windows Server 2019 (trash)",
        software_instalado: { "apache": "2.4.49", "java": "1.8.0", "postgresql": "11.5.0" }
      }
    ];
    setInventario(inventarioDemo);
    
    // Al abrir la página, preguntamos si hay backlog
    sincronizar(inventarioDemo, ultimoIdRef.current);
  }, []);

  // 2. El "Oído" (SSE): Escuchar el ping de nuevas noticias
  useEffect(() => {
    const sse = new EventSource('http://localhost:8000/api/noticias/stream');

    sse.onmessage = (event) => {
      console.log("¡Ping recibido! El servidor procesó una nueva amenaza.");
      // No mostramos la noticia. Sincronizamos en silencio con nuestro inventario
      if (inventario.length > 0) {
        sincronizar(inventario, ultimoIdRef.current);
      }
    };

    return () => sse.close(); // Limpieza al cerrar
  }, [inventario]); // Se re-conecta si cambia el inventario

  // 3. El Gatillo: Ir al backend a cruzar los datos
  const sincronizar = async (invActual, ultimoId) => {
    try {
      const response = await fetch('http://localhost:8000/api/v1/sincronizar', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          id_ultima_noticia: ultimoId,
          inventario_local: invActual
        })
      });

      if (response.ok) {
        const data = await response.json();
        
        // Si hay alertas nuevas, las sumamos a las que ya teníamos
        if (data.nuevas_alertas.length > 0) {
          setAlertas(prev => [...data.nuevas_alertas, ...prev]);
        }
        
        // Actualizamos nuestro rastreador de sincronización
        ultimoIdRef.current = data.id_ultimo_sincronizado;
      }
    } catch (error) {
      console.error("Error sincronizando con CyberScout:", error);
    }
  };

  return (
    <div className="dashboard">
      <header className="header">
        <h1>🛡️ CyberScout SOC</h1>
        <p>Zero-Trust Threat Intelligence</p>
      </header>

      <main className="content">
        <section className="alert-panel">
          <h2>Alertas Activas en su Infraestructura</h2>
          
          {alertas.length === 0 ? (
            <div className="no-alerts">✅ Ningún servidor de su inventario está bajo amenaza.</div>
          ) : (
            <div className="alert-grid">
              {alertas.map((alerta, index) => (
                <div key={index} className={`alert-card ${alerta.nivel_match}`}>
                  <div className="alert-badge">{alerta.nivel_match.toUpperCase()} MATCH</div>
                  <h3>{alerta.nombre_servidor}</h3>
                  <p><strong>Software Vulnerable:</strong> {alerta.software_afectado}</p>
                  <p><strong>CVE:</strong> {alerta.noticia_original.cve_id || "N/A"}</p>
                  <p><strong>Severidad Global:</strong> {alerta.noticia_original.severidad}</p>
                </div>
              ))}
            </div>
          )}
        </section>
      </main>
    </div>
  );
}

export default App;