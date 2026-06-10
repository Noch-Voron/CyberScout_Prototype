import { Link } from "react-router-dom";
import { AppShell } from "../components/AppShell";
import { Card, CardContent, CardHeader, CardTitle } from "../components/ui/card";
import { Badge } from "../components/ui/badge";
import { Button } from "../components/ui/button";
import {
  ShieldAlert,
  ArrowRight,
  ScanSearch,
  Boxes,
  TrendingUp,
  ExternalLink,
} from "lucide-react";
import {severityClasses, severityOrder, formatDate, getFuente} from "../utils/funciones";
import { use_getNoticias } from "../hooks/useNoticias"

export default function Dashboard() {
  const { noticias } = use_getNoticias();

  // CORRECCIÓN 1: Filtramos usando las llaves del diccionario
  const relevant = noticias.filter((n) => {
    const affectedDict = n.tags?.activos_afectados || {};
    return Object.keys(affectedDict).length > 0;
  });
  
  const sorted = [...relevant].sort((a, b) => {
    const rankA = severityOrder[a.tags?.severidad];
    const rankB = severityOrder[b.tags?.severidad];

    // primero por severidad
    if (rankA !== rankB) {
      return rankA - rankB;
    }

    // si tienen la misma severidad, ordena por fecha descendente
    return +new Date(b.extractdate) - +new Date(a.extractdate);
  });

  const total = noticias.length;
  const relevantPct = total ? Math.round((relevant.length / total) * 100) : 0;
  const critical = relevant.filter((n) => n.tags?.severidad === "Crítico" || n.tags?.severidad === "critical").length; // Ajusté por si acaso viene con mayúscula

  return (
    <AppShell>
      {/* Hero */}
      <section className="relative overflow-hidden border-b border-border">
        <div className="absolute inset-0 cyber-grid opacity-60" />
        <div className="absolute inset-0 bg-gradient-to-b from-transparent via-background/40 to-background" />
        <div className="container mx-auto px-4 py-14 relative">
          <div className="flex items-center gap-2 text-xs uppercase tracking-[0.2em] text-primary font-mono mb-3">
            <span className="size-1.5 rounded-full bg-primary animate-pulse" />
            Sistema operando
          </div>

          <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-4 max-w-4xl">
            <Stat
              icon={<ShieldAlert className="size-5" />}
              label="Alertas relevantes"
              value={String(relevant.length)}
              hint={`${critical} críticas`}
            />
            <Stat
              icon={<TrendingUp className="size-5" />}
              label="Relevancia"
              value={`${relevantPct}%`}
              hint={`${relevant.length} de ${total} clasificadas`}
            />
          </div>
        </div>
      </section>

      {/* Relevant news list */}
      <section className="container mx-auto px-4 py-12">
        <div className="flex items-end justify-between mb-6 flex-wrap gap-3">
          <h2 className="text-2xl font-semibold flex items-center gap-2">
            <ScanSearch className="size-6 text-primary" />
            Noticias relevantes para tu inventario
          </h2>
          <Button variant="outline" asChild>
            <Link to="/noticias">
              Ver todas las noticias <ArrowRight className="size-4" />
            </Link>
          </Button>
        </div>

          {sorted.length === 0 ? (
          <Card>
            <CardContent className="py-16 text-center text-muted-foreground">
              No hay noticias relevantes. Agrega tecnologías a tu inventario para empezar a filtrar.
              <div className="mt-4">
                <Button asChild>
                  <Link to="/inventario">Ir al inventario</Link>
                </Button>
              </div>
            </CardContent>
          </Card>
        ) : (
          <div className="grid gap-3">
            {sorted.map((n) => {
              // CORRECCIÓN 2: Extraemos los productos afectados para cada noticia
              const affectedDict = n.tags?.activos_afectados || {};
              const productosAfectados = Object.keys(affectedDict);

              return (
              <Link key={n.id}
                to="/news/$id"
                params={{ id: n.id }}
                className="group block">
                <Card className="transition-all hover:shadow-elegant hover:border-primary/40 bg-[image:var(--gradient-card)]">
                  <CardContent className="p-5 flex gap-4 items-start">
                    <Badge
                      variant="outline"
                      className={`uppercase text-[10px] tracking-wider border ${severityClasses(n.tags?.severidad ?? "sin severidad")}`}
                    >
                      {n.tags?.severidad?? "sin severidad"}
                    </Badge>
                    {n.cve_id && (
                        <div className="mt-2 text-[10px] font-mono text-muted-foreground">
                          {n.cve_id}
                        </div>
                      )}
                    <div className="flex-1 min-w-0">
                      <div className="flex flex-wrap items-center gap-2 text-xs text-muted-foreground">
                        <span>{getFuente(n.url)}</span>
                        <span>·</span>
                        <span>Extraido el {formatDate(n.extractdate)}</span>
                      </div>
                      <h3 className="mt-1 font-semibold text-lg leading-snug group-hover:text-primary transition-colors">
                        {n.title}
                      </h3>
                      <p className="mt-1 text-sm text-muted-foreground line-clamp-2">
                        {n.rawcontent.length > 100
                        ? n.rawcontent.substring(0, 100) + "..."
                        : n.rawcontent}
                      </p>
                      <div className="mt-3 flex flex-wrap gap-1.5">
                          <Badge variant="secondary" className="font-mono text-[10px]">
                            {n.tags?.categoria}
                          </Badge>
                        
                      </div>
                      
                      {/* CORRECCIÓN 3: Dibujamos las etiquetas si existen productos afectados */}
                      {productosAfectados.length > 0 && (
                        <div className="mt-3 text-xs flex flex-wrap items-center gap-2">
                          <span className="text-foreground font-medium">Activos afectados:</span>
                          {productosAfectados.map((a,index) => (
                            <Badge key={index} className="bg-primary/10 text-primary border-primary/30 border capitalize">
                              {a}
                            </Badge>
                          ))}
                        </div>
                      )}
                    </div>
                    <ExternalLink className="size-4 text-muted-foreground opacity-0 group-hover:opacity-100 transition-opacity mt-1" />
                  </CardContent>
                </Card>
              </Link>
            )})}
          </div>
        )}
      </section>
    </AppShell>
  );
}

function Stat({ icon, label, value, hint }) {
  return (
    <Card className="bg-[image:var(--gradient-card)] border-border/60">
      <CardHeader className="pb-2 flex-row items-center justify-between space-y-0">
        <CardTitle className="text-sm font-medium text-muted-foreground">{label}</CardTitle>
        <div className="text-primary">{icon}</div>
      </CardHeader>
      <CardContent>
        <div className="text-3xl font-bold font-display">{value}</div>
        {hint && <div className="text-xs text-muted-foreground mt-1">{hint}</div>}
      </CardContent>
    </Card>
  );
}