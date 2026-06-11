import { useState, useMemo } from "react";
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
import { Input } from "../components/ui/input";
import { Button } from "../components/ui/button";
import { Card, CardContent } from "../components/ui/card";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "../components/ui/select";
import { formatDate, severityClasses, getFuente } from "../utils/funciones";
import { use_getNoticias } from "../hooks/useNoticias";
import { ClipboardList, Search, Calendar, RotateCcw, ExternalLink, ChevronDown, ChevronUp, Database, BrainCircuit } from "lucide-react";

export default function Auditoria() {
  // Utilizamos el hook existente para traer las noticias de la base de datos
  const { noticias, refetch } = use_getNoticias();
  
  const [q, setQ] = useState("");
  const [fuenteFiltro, setFuenteFiltro] = useState("all");
  const [fechaInicio, setFechaInicio] = useState("");
  const [fechaFin, setFechaFin] = useState("");
  
  const [expandedId, setExpandedId] = useState(null);

  const handleReprocesar = async (noticiaId) => {
    if(!window.confirm(`¿Estás seguro de enviar la Noticia ${noticiaId} a reprocesar por la IA?`)) return;
    
    try {
      const res = await fetch(`http://localhost:8000/api/noticias/${noticiaId}/reprocesar`, { method: "PUT" });
      if (res.ok) {
        refetch(); // Recargamos las noticias usando tu hook
      }
    } catch (error) {
      console.error("Error al reprocesar:", error);
    }
  };

  const filteredLogs = useMemo(() => {
    // Asegurarnos de que sea un arreglo
    const data = Array.isArray(noticias) ? noticias : [];
    
    return data
      // 1. Solo noticias procesadas (que tengan tags)
      .filter((n) => n.tags && Object.keys(n.tags).length > 0)
      // 2. Filtro por Fuente
      .filter((n) => {
        if (fuenteFiltro === "all") return true;
        const fuenteOrigen = getFuente(n.url).toLowerCase();
        return fuenteOrigen.includes(fuenteFiltro.toLowerCase());
      })
      // 3. Filtro por Fecha (usamos processdate)
      .filter((n) => {
        if (!fechaInicio || !n.processdate) return true;
        return new Date(n.processdate) >= new Date(fechaInicio);
      })
      .filter((n) => {
        if (!fechaFin || !n.processdate) return true;
        const end = new Date(fechaFin);
        end.setHours(23, 59, 59, 999);
        return new Date(n.processdate) <= end;
      })
      // 4. Búsqueda por texto libre
      .filter((n) => {
        if (!q.trim()) return true;
        const needle = q.toLowerCase();
        return (
          n.title?.toLowerCase().includes(needle) ||
          n.tags?.categoria?.toLowerCase().includes(needle) ||
          n.rawcontent?.toLowerCase().includes(needle)
        );
      })
      // 5. Ordenar de la más reciente a la más antigua según la fecha de procesamiento
      .sort((a, b) => {
        // Si no tiene fecha (está en cola), la forzamos arriba simulando "ahora"
        const dateA = a.processdate ? new Date(a.processdate).getTime() : Date.now();
        const dateB = b.processdate ? new Date(b.processdate).getTime() : Date.now();
        return dateB - dateA;
      });
  }, [noticias, q, fuenteFiltro, fechaInicio, fechaFin]);

  const toggleExpand = (id) => {
    if (expandedId === id) {
      setExpandedId(null); 
    } else {
      setExpandedId(id); 
    }
  };

  // Extraemos las fuentes únicas para el menú desplegable
  const fuentesDisponibles = useMemo(() => {
    const data = Array.isArray(noticias) ? noticias : [];
    const procesadas = data.filter((n) => n.tags && Object.keys(n.tags).length > 0 );
    const fuentes = procesadas.map(n => getFuente(n.url));
    return [...new Set(fuentes)]; // Elimina duplicados
  }, [noticias]);

  return (
    <AppShell>
      <section className="container mx-auto px-4 py-10">
        <div className="mb-6">
          <h1 className="text-3xl font-bold tracking-tight flex items-center gap-2">
            <ClipboardList className="size-7 text-primary" /> Auditoría del Sistema
          </h1>
          <p className="text-sm text-muted-foreground mt-1">
            Revisa cómo la IA interpretó y catalogó cada noticia. Marca inconsistencias para reentrenar el modelo.
          </p>
        </div>

        <Card className="mb-6">
          <CardContent className="p-4 flex flex-col md:flex-row gap-3 items-end md:items-center">
            <div className="relative flex-1 w-full">
              <Search className="absolute left-2.5 top-2.5 size-4 text-muted-foreground" />
              <Input
                placeholder="Buscar en títulos, contenido o categorías..."
                value={q}
                onChange={(e) => setQ(e.target.value)}
                className="pl-9"
              />
            </div>
            
            {/* Selector dinámico de fuentes */}
            <Select value={fuenteFiltro} onValueChange={setFuenteFiltro}>
              <SelectTrigger className="w-full md:w-48">
                <SelectValue placeholder="Filtrar por Fuente" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">Todas las fuentes</SelectItem>
                {fuentesDisponibles.map((f, i) => (
                  <SelectItem key={i} value={f}>{f}</SelectItem>
                ))}
              </SelectContent>
            </Select>

            <div className="flex items-center gap-2 w-full md:w-auto">
              <div className="relative">
                <Calendar className="absolute left-2.5 top-2.5 size-4 text-muted-foreground" />
                <Input type="date" value={fechaInicio} onChange={(e) => setFechaInicio(e.target.value)} className="pl-9 text-sm" title="Fecha de inicio" />
              </div>
              <span className="text-muted-foreground text-sm">a</span>
              <div className="relative">
                <Calendar className="absolute left-2.5 top-2.5 size-4 text-muted-foreground" />
                <Input type="date" value={fechaFin} onChange={(e) => setFechaFin(e.target.value)} className="pl-9 text-sm" title="Fecha de fin" />
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Fecha (Procesamiento)</TableHead>
                <TableHead>Fuente</TableHead>
                <TableHead>Noticia y Clasificación</TableHead>
                <TableHead className="text-center w-32">Acciones</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredLogs.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={4} className="text-center py-10 text-muted-foreground">
                    No hay noticias procesadas que coincidan con los filtros.
                  </TableCell>
                </TableRow>
              ) : (
                filteredLogs.map((n) => {
                  const isExpanded = expandedId === n.id;
                  const severidad = n.tags?.severidad || "Sin clasificar";
                  const productosList = Object.keys(n.tags?.activos_afectados || {});

                  return (
                  <TableRow key={n.id} className={isExpanded ? "bg-muted/10" : ""}>
                    <TableCell className="text-xs font-mono text-muted-foreground whitespace-nowrap align-top pt-4">
                      {n.processdate ? (
                        formatDate(n.processdate)
                      ) : (
                        <Badge variant="outline" className="text-[10px] bg-amber-50 text-amber-700 animate-pulse border-amber-200">
                          Procesando...
                        </Badge>
                      )}
                    </TableCell>
                    <TableCell className="align-top pt-4">
                      <Badge variant="secondary" className="text-[10px] font-medium">
                        {getFuente(n.url)}
                      </Badge>
                    </TableCell>
                    
                    <TableCell 
                      className="cursor-pointer hover:bg-muted/30 transition-colors py-4"
                      onClick={() => toggleExpand(n.id)}
                      title="Haz clic para expandir y auditar la interpretación"
                    >
                      <div className="flex flex-col gap-2">
                        <div className="flex items-start justify-between gap-4">
                          <h3 className={`font-semibold text-sm ${isExpanded ? "text-primary" : "text-foreground line-clamp-1"}`}>
                            {n.title}
                          </h3>
                          <div className="flex items-center gap-2 flex-shrink-0">
                            <Badge 
                              variant="outline" 
                              className={`text-[10px] uppercase border ${severityClasses ? severityClasses(severidad) : ''}`}
                            >
                              {severidad}
                            </Badge>
                            {isExpanded ? <ChevronUp className="size-4 text-muted-foreground" /> : <ChevronDown className="size-4 text-muted-foreground" />}
                          </div>
                        </div>

                        {/* PANEL DE AUDITORÍA EXPANDIDO */}
                        {isExpanded && (
                          <div className="mt-4 grid grid-cols-1 lg:grid-cols-2 gap-4 animate-in fade-in slide-in-from-top-2 duration-200 cursor-default" onClick={(e) => e.stopPropagation()}>
                            
                            {/* Columna Izquierda: Lo que entró (Input) */}
                            <div className="bg-gray-50 border border-gray-200 rounded-lg p-3">
                              <h4 className="flex items-center gap-1.5 text-xs font-bold text-gray-700 uppercase tracking-wider mb-2">
                                <Database className="size-3.5" /> Texto Original (Input)
                              </h4>
                              <p className="text-xs text-gray-600 whitespace-pre-wrap leading-relaxed max-h-60 overflow-y-auto pr-2 custom-scrollbar">
                                {n.rawcontent}
                              </p>
                            </div>

                            {/* Columna Derecha: Lo que salió (Output / Tags) */}
                            <div className="bg-blue-50/50 border border-blue-100 rounded-lg p-3">
                              <h4 className="flex items-center gap-1.5 text-xs font-bold text-blue-800 uppercase tracking-wider mb-3">
                                <BrainCircuit className="size-3.5" /> Estructura Asignada por IA
                              </h4>
                              
                              <div className="space-y-3 text-xs">
                                <div>
                                  <span className="font-semibold text-blue-900 block mb-1">Categoría:</span>
                                  <Badge variant="secondary" className="font-mono text-[10px]">{n.tags?.categoria}</Badge>
                                </div>
                                
                                <div>
                                  <span className="font-semibold text-blue-900 block mb-1">Activos Detectados:</span>
                                  {productosList.length > 0 ? (
                                    <div className="flex flex-wrap gap-1">
                                      {productosList.map(a => (
                                        <Badge key={a} className="bg-white border-blue-200 text-blue-700 hover:bg-blue-50 capitalize">
                                          {a}
                                        </Badge>
                                      ))}
                                    </div>
                                  ) : (
                                    <span className="text-muted-foreground italic">Ningún software identificado.</span>
                                  )}
                                </div>

                                {/* Si tienes una variable para el resumen de Gemini, muéstrala aquí */}
                                {n.tags?.resumen && (
                                  <div>
                                    <span className="font-semibold text-blue-900 block mb-1">Resumen / Lógica:</span>
                                    <p className="text-blue-800/80 leading-relaxed">
                                      {n.tags.resumen}
                                    </p>
                                  </div>
                                )}
                              </div>
                            </div>
                          </div>
                        )}
                      </div>
                    </TableCell>

                    <TableCell className="align-top pt-4 text-center">
                      <div className="flex items-center justify-center gap-2">
                        <Button 
                          size="icon" 
                          variant="outline" 
                          title="Marcar inconsistencia / Reprocesar" 
                          onClick={() => handleReprocesar(n.id)} 
                          className="size-8 bg-red-50 hover:bg-red-100 border-red-200"
                        >
                          <RotateCcw className="size-4 text-red-600" />
                        </Button>
                      </div>
                    </TableCell>
                  </TableRow>
                )})
              )}
            </TableBody>
          </Table>
        </Card>
      </section>
    </AppShell>
  );
}