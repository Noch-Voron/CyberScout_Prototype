import { Link, useLocation } from "react-router-dom";
import { Shield, LayoutDashboard, Newspaper, Boxes, Rss, Activity, Palette } from "lucide-react";
import { Button } from "../components/ui/button";
import { useState, useEffect } from "react";  

const nav = [
  { to: "/", label: "Dashboard", icon: LayoutDashboard },
  { to: "/noticias", label: "Noticias", icon: Newspaper },
  { to: "/inventario", label: "Inventario", icon: Boxes },
  { to: "/fuentes", label: "Fuentes", icon: Rss },
  { to: "/auditoria", label: "Auditoría", icon: Activity },
];

export function AppShell({ children }) {
  const location = useLocation();
  const pathname = location.pathname;
  
  const [hue, setHue] = useState(222);

  return (
    <div className="min-h-screen flex flex-col bg-background text-foreground">
      {/* Header */}
      <header className="sticky top-0 z-40 backdrop-blur-xl bg-background/80 border-b border-border">
        <div className="container mx-auto px-4 h-16 flex items-center gap-8">
          <Link to="/" className="flex items-center gap-2 group">
            <div className="size-9 rounded-lg bg-hero shadow-glow grid place-items-center">
              <Shield className="size-5 text-primary-foreground" />
            </div>
            <div className="leading-tight">
              <div className="font-display font-semibold tracking-tight">CyberScout</div>
              <div className="text-[8px] uppercase tracking-[0.18uem] text-muted-foreground">
                Threat Intelligence · 
              </div>
            </div>
          </Link>

          {/* Navigation */}
          <nav className="hidden md:flex items-center gap-1 ml-4">
            {nav.map((item) => {
              const active = item.to === "/" ? pathname === "/" : pathname.startsWith(item.to);
              const baseClasses =
                "px-3 py-2 rounded-md text-sm font-medium flex items-center gap-2 transition-colors";
              const activeClasses = "bg-accent text-accent-foreground";
              const inactiveClasses =
                "text-muted-foreground hover:text-foreground hover:bg-accent/50";
              return (
                <Link
                  key={item.to}
                  to={item.to}
                  className={`${baseClasses} ${active ? activeClasses : inactiveClasses}`}
                >
                  <item.icon className="size-4" />
                  {item.label}
                </Link>
              );
            })}
          </nav>

        </div>
      </header>

      {/* Main content */}
      <main className="flex-1">{children}</main>

      {/* Footer */}
      <footer className="border-t border-border py-6 text-center text-xs text-muted-foreground">
         ... · CyberScout · ...
      </footer>
    </div>
  );
}
