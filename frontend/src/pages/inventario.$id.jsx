import { Link, useParams } from "react-router-dom";
import { useEffect, useState } from "react";

import { AppShell } from "../components/AppShell";
import { Card, CardContent, CardHeader, CardTitle } from "../components/ui/card";
import { Badge } from "../components/ui/badge";
import { Button } from "../components/ui/button";

import { ArrowLeft, ShieldAlert } from "lucide-react";

export default function InventarioDetail() {

  const { id } = useParams();

  const [servidor, setServidor] = useState(null);
  const [alertas, setAlertas] = useState([]);

  useEffect(() => {

    const inventario =
      JSON.parse(localStorage.getItem("inventario") || "[]");

    const srv = inventario.find(s => s.id === id);

    setServidor(srv);

    const alertasGuardadas =
      JSON.parse(localStorage.getItem("alertas_sincronizadas") || "[]");

    const alertasServidor =
      alertasGuardadas.filter(
        a => a.id_servidor === id
      );

    setAlertas(alertasServidor);

  }, [id]);

  if (!servidor) {
    return (
      <AppShell>
        <div className="container mx-auto py-10">
          Servidor no encontrado
        </div>
      </AppShell>
    );
  }

  return (
    <AppShell>
      <section className="container mx-auto px-4 py-10 max-w-5xl">

        <Button variant="ghost" asChild className="mb-4">
          <Link to="/inventario">
            <ArrowLeft className="size-4 mr-2" />
            Volver a inventario
          </Link>
        </Button>
        <div className="grid lg:grid-cols-5 gap-6">
            {/* CONTENIDO PRINCIPAL */}
            <div className="lg:col-span-2 space-y-4">
                <div className="bg-white p-5 rounded-lg shadow-md border-l-4 border-blue-600 hover:shadow-lg transition-shadow">
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
            </div>

            {/* SIDEBAR */}
            <div className="lg:col-span-3 space-y-6">
            <Card className="mt-6">
            <CardHeader>
                <CardTitle className="flex items-center gap-2">
                <ShieldAlert className="size-5 text-red-500" />
                Alertas relacionadas
                </CardTitle>
            </CardHeader>

            <CardContent>

                {alertas.length === 0 ? (
                <p className="text-muted-foreground">
                    No existen alertas para este activo.
                </p>
                ) : (
                <div className="space-y-3">

                    {alertas.map(alerta => (

                    <Link
                        key={`${alerta.noticia_id}-${alerta.software_afectado}`}
                        to={`/noticias/${alerta.noticia_id}`}
                        className="block"
                    >
                        <Card className="hover:border-primary transition-colors">
                        <CardContent className="p-4">

                            <div className="flex items-center justify-between">

                            <div>
                                <div className="font-medium">
                                {alerta.software_afectado}
                                </div>

                                <div className="text-sm text-muted-foreground">
                                Noticia #{alerta.noticia_id}
                                </div>
                            </div>

                            <Badge variant="destructive">
                                Vulnerable
                            </Badge>

                            </div>

                        </CardContent>
                        </Card>
                    </Link>

                    ))}

                </div>
                )}

            </CardContent>
            </Card>
            </div>
        </div>



      </section>
    </AppShell>
  );
}