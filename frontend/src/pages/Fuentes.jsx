import { useState } from "react";

import { AppShell } from "../components/AppShell";

import { Card, CardContent, CardHeader, CardTitle } from "../components/ui/card";
import { Button } from "../components/ui/button";
import { Input } from "../components/ui/input";
import { Badge } from "../components/ui/badge";

import { Plus, Trash2, RefreshCw, Rss } from "lucide-react";

import {
  use_getFuentes,
  addFuente,
  deleteFuente,
} from "../hooks/useFuentes";

import { runIngest } from "../hooks/useIngesta"

export default function Fuentes() {
  const { fuentes, error, refetch } = use_getFuentes();

  const [url, setUrl] = useState("");
  const [loading, setLoading] = useState(false);

  const handleAdd = async () => {
    if (!url.trim()) return;

    try {
      setLoading(true);

      await addFuente(url);

      setUrl("");
      refetch();
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id) => {
    try {
      await deleteFuente(id);
      refetch();
    } catch (err) {
      console.error(err);
    }
  };

  const handleIngest = async () => {
    try {
        await runIngest();

        // opcional: recargar la lista
        refetch();

        console.log("Ingesta completada");
    } catch (err) {
        console.error(err);
    }
  };

  return (
    <AppShell>
      <section className="container mx-auto px-4 py-10">
        {/* Header */}
        <div className="flex items-end justify-between flex-wrap gap-4 mb-6">
          <div>
            <h1 className="text-3xl font-bold flex items-center gap-2">
              <Rss className="size-7 text-primary" />
              Fuentes
            </h1>

            <p className="text-sm text-muted-foreground mt-1">
              Fuentes RSS configuradas en el sistema
            </p>
          </div>

          <Button variant="outline" onClick={refetch}>
            <RefreshCw className="size-4 mr-2" />
            Actualizar
          </Button>
          <Button
            variant="outline"
            onClick={handleIngest}
            >
            <RefreshCw className="size-4 mr-2" />
            Ejecutar ingesta
           </Button>
        </div>

        {/* Formulario */}
        <Card className="mb-6">
          <CardHeader>
            <CardTitle>Nueva fuente</CardTitle>
          </CardHeader>

          <CardContent className="flex gap-3">
            <Input
              placeholder="https://ejemplo.com/rss.xml"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
            />

            <Button onClick={handleAdd} disabled={loading}>
              <Plus className="size-4 mr-2" />
              Agregar
            </Button>
          </CardContent>
        </Card>

        {/* Error */}
        {error && (
          <Card className="mb-4 border-red-500">
            <CardContent className="p-4 text-red-500">
              Error al cargar fuentes
            </CardContent>
          </Card>
        )}

        {/* Lista */}
        <div className="grid gap-3">
          {fuentes.map((fuente) => (
            <Card key={fuente.id}>
              <CardContent className="p-4 flex items-center gap-4">
                <div className="size-10 rounded-lg bg-primary/10 flex items-center justify-center">
                  <Rss className="size-5 text-primary" />
                </div>

                <div className="flex-1">
                  <div className="flex items-center gap-2">
                    {fuente.processed ? (
                      <Badge className="bg-green-500">
                        Procesada
                      </Badge>
                    ) : (
                      <Badge variant="outline">
                        Pendiente
                      </Badge>
                    )}
                  </div>

                  <a
                    href={fuente.url}
                    target="_blank"
                    rel="noreferrer"
                    className="text-sm text-muted-foreground hover:text-primary break-all"
                  >
                    {fuente.url}
                  </a>

                  <div className="text-xs text-muted-foreground mt-1">
                    {new Date(fuente.processdate).toLocaleString()}
                  </div>
                </div>

                <Button
                  size="icon"
                  variant="ghost"
                  onClick={() => handleDelete(fuente.id)}
                >
                  <Trash2 className="size-4 text-red-500" />
                </Button>
              </CardContent>
            </Card>
          ))}

          {fuentes.length === 0 && (
            <Card>
              <CardHeader>
                <CardTitle className="text-center text-muted-foreground">
                  No hay fuentes configuradas
                </CardTitle>
              </CardHeader>
            </Card>
          )}
        </div>
      </section>
    </AppShell>
  );
}