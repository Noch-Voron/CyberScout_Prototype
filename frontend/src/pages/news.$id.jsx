import { Link, useParams, useNavigate} from "react-router-dom";
import { AppShell } from "../components/AppShell";
import { Card, CardContent, CardHeader, CardTitle } from "../components/ui/card";
import { Badge } from "../components/ui/badge";
import { Button } from "../components/ui/button";
import { severityClasses, formatDate, getFuente } from "../utils/funciones";
import { ArrowLeft, ExternalLink, ShieldAlert, Boxes } from "lucide-react";
import { use_getNoticia_id } from "../hooks/useNoticias";

export default function NewsDetail() {
    
    const { id } = useParams()
    const navigate = useNavigate();

    const { noticia , error, refetch } = use_getNoticia_id(Number(id));

  if (noticia === null) {
    return (
        <AppShell>
        <div className="container mx-auto py-20">
            Cargando...
        </div>
        </AppShell>
    );
    }
    
  if (noticia == null) {
    return (
        <AppShell>
            <div className="container mx-auto px-4 py-20 text-center">
            <h1 className="text-2xl font-semibold">Noticia no encontrada</h1>
            <Button className="mt-6" onClick={() => navigate("/noticias")}>
                Volver a noticias
            </Button>
            </div>
        </AppShell>
        );
    }

    // --- LA CORRECCIÓN EMPIEZA AQUÍ ---
    // Extraemos las llaves del diccionario dinámico que manda Gemini/Python
    const affectedDict = noticia?.tags?.activos_afectados || {};
    const productosAfectados = Object.keys(affectedDict);
    // --- LA CORRECCIÓN TERMINA AQUÍ ---

    const inventario = JSON.parse(
      localStorage.getItem("inventario") || "[]"
    );
    const softwareInstalado = new Set();
    inventario.forEach((srv) => {
      Object.keys(srv.software_instalado || {}).forEach((sw) => {
        softwareInstalado.add(sw.toLowerCase());
      });
    });

    return (
    <AppShell>
      <section className="container mx-auto px-4 py-10 max-w-5xl">
        <Button variant="ghost" size="sm" asChild className="mb-4">
          <Link to="/noticias">
            <ArrowLeft className="size-4" /> Volver a noticias
          </Link>
        </Button>

        <div className="grid lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-base">
                  <Boxes className="size-4 text-primary" />
                  Activos afectados
                </CardTitle>
              </CardHeader>
              <CardContent>
                {/* Cambiamos la condición para usar nuestra nueva variable productosAfectados */}
                {productosAfectados.length === 0 ? (
                <p className="text-sm text-muted-foreground">
                    Ningún activo del inventario coincide con esta noticia. Aún así puede ser
                    informativa para tu sector.
                </p>
                ) : (
                <div className="flex flex-wrap gap-1">
                  {productosAfectados.map((a, index) => {
                    const coincideInventario =
                      softwareInstalado.has(a.toLowerCase());

                    return (
                      <Badge
                        key={index}
                        className={
                          coincideInventario
                            ? "bg-red-500 text-white border-red-600 border text-[10px] capitalize"
                            : "bg-primary/10 text-primary border-primary/30 border text-[10px] capitalize"
                        }
                      >
                        {a}
                      </Badge>
                    );
                  })}
                </div>
                )}
                
              </CardContent>
            </Card>
            <Card className="bg-[image:var(--gradient-card)]">
              <CardContent className="p-6">
                <div className="flex flex-wrap items-center gap-2 mb-3">
                  <Badge
                    variant="outline"
                    className={`uppercase text-[10px] tracking-wider border ${severityClasses(noticia.tags?.severidad)}`}
                  >
                    {noticia.tags?.severidad ?? "Sin clasificar"}
                  </Badge>
                  {noticia.cve_id && (
                    <Badge variant="secondary" className="font-mono">
                      {noticia.cve_id}
                    </Badge>
                  )}
                  <span className="text-xs text-muted-foreground">
                    {getFuente(noticia.url)} · {formatDate(noticia.extractdate)}
                  </span>
                </div>
                <h1 className="text-3xl font-bold leading-tight">{noticia.title}</h1>
                <p className="mt-4 text-muted-foreground leading-relaxed">
                    {noticia.rawcontent}                        
                </p>

                <div className="mt-5 flex flex-wrap gap-1.5">
                    <Badge  variant="secondary" className="font-mono text-xs">
                      {noticia.tags?.categoria}
                    </Badge>
                </div>

                <div className="mt-6 flex gap-2 flex-wrap">
                  <Button asChild>
                    <a href={noticia.url} target="_blank" rel="noreferrer">
                      <ExternalLink className="size-4" /> Leer noticia original
                    </a>
                  </Button>
                </div>
              </CardContent>
            </Card>
          </div>

          <div className="space-y-4">

            <Card>
              <CardHeader>
                <CardTitle className="text-base">Noticia original</CardTitle>
              </CardHeader>
              <CardContent className="text-sm space-y-2">
                <div>
                  <div className="text-xs text-muted-foreground">Publicada por</div>
                  <div className="font-medium">{getFuente(noticia.url)}</div>
                </div>
                <div>
                  <div className="text-xs text-muted-foreground">URL</div>
                  <a
                    href={noticia.url}
                    target="_blank"
                    rel="noreferrer"
                    className="text-primary hover:underline break-all"
                  >
                    {noticia.url}
                  </a>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>
    </AppShell>
  );
}