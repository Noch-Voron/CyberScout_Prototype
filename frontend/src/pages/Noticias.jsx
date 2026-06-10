import { Link } from "react-router-dom";
import { AppShell } from "../components/AppShell";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "../components/ui/table";
import { Badge } from "../components/ui/badge";
import { Button } from "../components/ui/button";
import { Input } from "../components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "../components/ui/select";
import { Tabs, TabsList, TabsTrigger } from "../components/ui/tabs";
import { severityClasses, severityOrder, formatDate, getFuente } from "../utils/funciones";
import { LayoutGrid, Rows3, ExternalLink, ArrowRight } from "lucide-react";
import { Card, CardContent } from "../components/ui/card";
import { useState, useMemo } from "../hooks/hooks";
import { use_getNoticias } from "../hooks/useNoticias";

export default function Noticias() {
    const { noticias , error, refetch } = use_getNoticias();
    const [view, setView] = useState("grid");
    const [q, setQ] = useState("");
    const [sev, setSev] = useState("all");
    const [scope, setScope] = useState("relevant");

    const filtered = useMemo(() => {
        return (Array.isArray(noticias) ? noticias : [])
        .filter((n) => {
            if (scope !== "relevant") return true;
            
            // CORRECCIÓN: Extraemos las llaves del diccionario de activos que envía el Backend
            const affectedDict = n.tags?.activos_afectados || {};
            const products = Object.keys(affectedDict);
            
            return products.length > 0;
            })
        .filter((n) => sev === "all" ? true : n.tags?.severidad === sev)
        .filter((n) => {
            if (!q.trim()) return true;
            const needle = q.toLowerCase();
            return (
            n.title?.toLowerCase().includes(needle) ||
            n.rawcontent?.toLowerCase().includes(needle) ||
            n.tags?.categoria?.toLowerCase().includes(needle) ||
            (n.cve_id?.toLowerCase().includes(needle) ?? false)
            );
        })
        .sort((a, b) => {
            const sevDiff =
            severityOrder(a.tags?.severidad) -
            severityOrder(b.tags?.severidad);

        if (sevDiff !== 0) return sevDiff;

        return (
            new Date(b.extractdate) -
            new Date(a.extractdate)
        );
        });
    }, [noticias, q, sev, scope]);


    return (
        <AppShell>
        <section className="container mx-auto px-4 py-10">
            <div className="flex items-end justify-between flex-wrap gap-4 mb-6">
            <div>
                <h1 className="text-3xl font-bold">Noticias</h1>
                <p className="text-sm text-muted-foreground mt-1">
                {filtered.length} resultados · vista {view === "grid" ? "grilla" : "tabla"}
                </p>
            </div>
            <Tabs value={view} onValueChange={(v) => setView(v)}>
                <TabsList>
                <TabsTrigger value="grid" className="gap-2">
                    <LayoutGrid className="size-4" />
                </TabsTrigger>
                <TabsTrigger value="table" className="gap-2">
                    <Rows3 className="size-4" />
                </TabsTrigger>
                </TabsList>
            </Tabs>
            </div>

            <Card className="mb-6">
            <CardContent className="p-4 flex flex-wrap gap-3 items-center">
                <Input
                placeholder="Buscar por título, tag o CVE..."
                value={q}
                onChange={(e) => setQ(e.target.value)}
                className="max-w-xs"
                />
                <Select value={sev} onValueChange={setSev}>
                <SelectTrigger className="w-44">
                    <SelectValue placeholder="Severidad" />
                </SelectTrigger>
                <SelectContent>
                    <SelectItem value="all">Todas</SelectItem>
                    <SelectItem value="Critico">Crítica</SelectItem>
                    <SelectItem value="Alto">Alta</SelectItem>
                    <SelectItem value="Medio">Media</SelectItem>
                    <SelectItem value="Bajo">Baja</SelectItem>
                </SelectContent>
                </Select>
                <Select value={scope} onValueChange={setScope}>
                <SelectTrigger className="w-56">
                    <SelectValue placeholder="Alcance" />
                </SelectTrigger>
                <SelectContent>
                    <SelectItem value="relevant">Con activos detectados</SelectItem>
                    <SelectItem value="all">Todas las noticias</SelectItem>
                </SelectContent>
                </Select>
            </CardContent>
            </Card>

            {view === "grid" ? (
            <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
                {filtered.map((n) => (
                <Link key={n.id} to={`/news/${n.id}`} className="group">
                    <Card className="h-full transition-all hover:shadow-elegant hover:border-primary/40 bg-[image:var(--gradient-card)]">
                    <CardContent className="p-5 flex flex-col h-full">
                        <div className="flex items-center justify-between mb-2">
                        <Badge
                            variant="outline"
                            className={`uppercase text-[10px] tracking-wider border ${severityClasses(n.tags?.severidad)}`}
                        >
                            {n.tags?.severidad ?? "Sin clasificar"}
                        </Badge>
                        <span className="text-xs text-muted-foreground">{getFuente(n.url)}</span>
                        </div>
                        <h3 className="font-semibold leading-snug group-hover:text-primary transition-colors">
                        {n.title}
                        </h3>
                        <p className="mt-2 text-sm text-muted-foreground line-clamp-3 flex-1">
                        {n.rawcontent.length > 100
                            ? n.rawcontent.substring(0, 100) + "..."
                            : n.rawcontent}
                        </p>
                        <div className="mt-3 flex flex-wrap gap-1.5">
                            <Badge variant="secondary" className="font-mono text-[10px]">
                            {n.tags?.categoria}
                            </Badge>
                        </div>
                        <div className="mt-4 flex items-center justify-between text-xs text-muted-foreground">
                        <span>{formatDate(n.extractdate)}</span>
                        <span className="flex items-center gap-1 text-primary opacity-0 group-hover:opacity-100 transition-opacity">
                            Ver detalle <ArrowRight className="size-3" />
                        </span>
                        </div>
                    </CardContent>
                    </Card>
                </Link>
                ))}
            </div>
            ) : (
            <Card>
                <Table>
                <TableHeader>
                    <TableRow>
                    <TableHead>Severidad</TableHead>
                    <TableHead>Título</TableHead>
                    <TableHead>Fuente</TableHead>
                    <TableHead>Tags</TableHead>
                    <TableHead>Activos afectados</TableHead>
                    <TableHead>Publicado</TableHead>
                    <TableHead></TableHead>
                    </TableRow>
                </TableHeader>
                <TableBody>
                    {filtered.map((n) => {
                    // CORRECCIÓN: Extraemos las llaves para la tabla
                    const productsList = Object.keys(n.tags?.activos_afectados || {});
                    
                    return (
                    <TableRow key={n.id}>
                        <TableCell>
                        <Badge
                            variant="outline"
                            className={`uppercase text-[10px] tracking-wider border ${severityClasses(n.tags?.severidad)}`}
                        >
                            {n.tags?.severidad}
                        </Badge>
                        </TableCell>
                        <TableCell className="max-w-md">
                        <Link
                            to="/news/$id"
                            params={{ id: n.id }}
                            className="font-medium hover:text-primary"
                        >
                            {n.title}
                        </Link>
                        {n.cve && (
                            <div className="text-[10px] font-mono text-muted-foreground mt-0.5">
                            {n.cve_id}
                            </div>
                        )}
                        </TableCell>
                        <TableCell className="text-sm text-muted-foreground">{getFuente(n.url)}</TableCell>
                        <TableCell>
                        <div className="flex flex-wrap gap-1">
                            <Badge variant="secondary" className="font-mono text-[10px]">
                                {n.tags?.categoria}
                            </Badge>
                        </div>
                        </TableCell>
                        <TableCell>
                        {productsList.length === 0 ? (
                            <span className="text-xs text-muted-foreground">—</span>
                        ) : (
                            <div className="flex flex-wrap gap-1">
                            {productsList.map((a,index) => (
                                <Badge
                                key={index}
                                className="bg-primary/10 text-primary border-primary/30 border text-[10px] capitalize"
                                >
                                {a}
                                </Badge>
                            ))}
                            </div>
                        )}
                        </TableCell>
                        <TableCell className="text-xs text-muted-foreground whitespace-nowrap">
                        {formatDate(n.extractdate)}
                        </TableCell>
                        <TableCell>
                        <Button asChild size="sm" variant="ghost">
                            <a href={n.url} target="_blank" rel="noreferrer">
                            <ExternalLink className="size-4" />
                            </a>
                        </Button>
                        </TableCell>
                    </TableRow>
                    )})}
                </TableBody>
                </Table>
            </Card>
            )}
        </section>
        </AppShell>
    );
}