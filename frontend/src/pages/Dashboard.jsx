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
import { use_getNoticias } from "../hooks/useNoticias";
import { useSincronizar } from "../hooks/useSincronizar";

export default function Dashboard() {
  const { noticias } = use_getNoticias();
  const { alertas } = useSincronizar();

  const sortedAlertas = [...alertas].sort((a, b) => {
    const rankA = severityOrder[a.noticia_original?.severidad] ?? 999;
    const rankB = severityOrder[b.noticia_original?.severidad] ?? 999;

    if (rankA !== rankB) {
      return rankA - rankB;
    }

    const dateA = a.noticia_extractdate ? new Date(a.noticia_extractdate) : 0;
    const dateB = b.noticia_extractdate ? new Date(b.noticia_extractdate) : 0;
    return dateB - dateA;
  });

  const total = noticias.length;
  const relevantPct = total ? Math.round((alertas.length / total) * 100) : 0;
  const critical = alertas.filter((a) => {
    const sev = a.noticia_original?.severidad?.toLowerCase();
    return sev === "crítico" || sev === "critical" || a.nivel_match === "full";
  }).length;

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
              value={String(alertas.length)}
              hint={`${critical} críticas`}
            />
            <Stat
              icon={<TrendingUp className="size-5" />}
              label="Relevancia"
              value={`${relevantPct}%`}
              hint={`${alertas.length} de ${total} clasificadas`}
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

          {sortedAlertas.length === 0 ? (
          <Card>
            <CardContent className="py-16 text-center text-muted-foreground">
              No hay alertas detectadas para tu inventario actual.
              <div className="mt-4">
                <Button asChild>
                  <Link to="/inventario">Ir al inventario</Link>
                </Button>
              </div>
            </CardContent>
          </Card>
        ) : (
          <div className="grid gap-3">
            {sortedAlertas.map((a, idx) => (
              <Link key={`${a.noticia_id}-${a.id_servidor}-${a.software_afectado}-${idx}`}
                to={`/news/${a.noticia_id}`}
                className="group block">
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
                        <span className="text-xs font-semibold text-foreground/80">Servidor:</span>
                        <Badge variant="outline" className="bg-primary/5 text-primary border-primary/20">
                          {a.nombre_servidor} ({a.software_afectado})
                        </Badge>
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