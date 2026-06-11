import { Link, useParams } from "react-router-dom";
import { useEffect, useState } from "react";

import { AppShell } from "../components/AppShell";
import { Card, CardContent, CardHeader, CardTitle } from "../components/ui/card";
import { Badge } from "../components/ui/badge";
import { Button } from "../components/ui/button";

import {severityClasses, severityOrder, formatDate, getFuente} from "../utils/funciones";

import { ArrowLeft, ShieldAlert, ExternalLink, } from "lucide-react";

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
            <div className="lg:col-span-2  items-start">
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
            <div className="lg:col-span-3  items-start">
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

                    {alertas.map(a => (

                    <Link
                        key={`${a.noticia_id}-${a.software_afectado}`}
                        to={`/news/${a.noticia_id}`}
                        className="block"
                    >

                        <Card className="transition-all hover:shadow-elegant hover:border-primary/40 bg-[image:var(--gradient-card)]">
                            <CardContent className="p-5 flex gap-4 items-start">
                            <div className="flex flex-col gap-2">
                                <Badge
                                variant="outline"
                                className={`uppercase text-[10px] tracking-wider border ${severityClasses(a.noticia_original?.severidad ?? "sin severidad")}`}
                                >
                                {a.noticia_original?.severidad ?? "sin severidad"}
                                </Badge>
                                <Badge
                                className={`text-[9px] font-bold uppercase tracking-wider ${
                                    a.nivel_match === "full"
                                    ? "bg-red-500/20 text-red-500 border border-red-500/40"
                                    : "bg-amber-500/20 text-amber-500 border border-amber-500/40"
                                }`}
                                >
                                {a.nivel_match === "full" ? "Match Total" : "Match Parcial"}
                                </Badge>
                            </div>
        
                            <div className="flex-1 min-w-0">
                                <div className="flex flex-wrap items-center gap-2 text-xs text-muted-foreground">
                                <span>{getFuente(a.noticia_url)}</span>
                                <span>·</span>
                                <span>Extraído el {formatDate(a.noticia_extractdate)}</span>
                                </div>
                                <h3 className="mt-1 font-semibold text-lg leading-snug group-hover:text-primary transition-colors">
                                {a.noticia_titulo}
                                </h3>
                                <p className="mt-1 text-sm text-muted-foreground line-clamp-2">
                                {a.noticia_rawcontent && a.noticia_rawcontent.length > 100
                                    ? a.noticia_rawcontent.substring(0, 100) + "..."
                                    : a.noticia_rawcontent}
                                </p>
                                
                                <div className="mt-3 flex flex-wrap gap-2 items-center">
                                
                                {a.noticia_original?.cve_id && (
                                    <Badge variant="secondary" className="font-mono text-[10px]">
                                    {a.noticia_original.cve_id}
                                    </Badge>
                                )}
                                {a.noticia_original?.tipo_vulnerabilidad && (
                                    <Badge variant="secondary" className="font-mono text-[10px]">
                                    {a.noticia_original.tipo_vulnerabilidad}
                                    </Badge>
                                )}
                                </div>
                            </div>
                            <ExternalLink className="size-4 text-muted-foreground opacity-0 group-hover:opacity-100 transition-opacity mt-1" />
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