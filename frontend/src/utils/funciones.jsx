//Nivel de severidad
export function severityOrder(severity) {
  const order = {
    critica: 0,
    alta: 1,
    media: 2,
    baja: 3,
  };
  return order[severity] ?? 99;
}

export function formatDate(datestring){
  const d = new Date(datestring);
  return d.toLocaleString("es", {
    day: "2-digit",
    month: "short",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

export function getFuente(url) {
  try {
    const hostname = new URL(url).hostname; // ej: "thehackernews.com"
    // quitar "www." si existe
    const clean = hostname.replace(/^www\./, "");
    // convertir a nombre legible
    return clean
      .split(".")[0] // "thehackernews"
      .replace(/-/g, " ") // "the hackernews"
      .replace(/\b\w/g, c => c.toUpperCase()); // "The Hackernews"
  } catch {
    return "Fuente desconocida";
  }
}

export function severityClasses(severity) {
  switch (severity) {
    case "critical":
    case "critico":
      return "bg-red-600 text-white border-red-700";
    case "alta":
      return "bg-orange-500 text-white border-orange-600";
    case "media":
      return "bg-yellow-400 text-black border-yellow-500";
    case "baja":
      return "bg-green-500 text-white border-green-600";
    default:
      return "bg-gray-200 text-gray-700 border-gray-300";
  }
}