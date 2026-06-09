import { BrowserRouter, Routes, Route } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import Noticias from "./pages/Noticias";
import NewsDetail from "./pages/news.$id";
import Fuentes from "./pages/Fuentes";
import Inventario from "./pages/Inventario";
import Auditoria from "./pages/Auditoria";


export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/Noticias" element={<Noticias />} />
        <Route path="/Fuentes" element={<Fuentes />} />
        <Route path="/Auditoria" element={<Auditoria />} />
        <Route path="/Inventario" element={<Inventario />} />
        <Route path="/news/:id" element={<NewsDetail />} />

      </Routes>
    </BrowserRouter>
  );
}

