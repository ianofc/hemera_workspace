import { NavLink, useLocation, useNavigate } from "react-router-dom";
import { LayoutDashboard, BookOpen, ClipboardList, Calendar, Library, Sparkles, User, LogOut } from "lucide-react";
import { cn } from "@/lib/utils";
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip";
import { HemeraSun } from "./HemeraSun";
import { useAuth } from "@/hooks/useAuth";
import { toast } from "sonner";

interface FloatingSidebarProps {
  role: "aluno" | "professor";
}

const itemsByRole = {
  professor: [
    { to: "/professor", icon: LayoutDashboard, label: "Painel" },
    { to: "/professor/turmas", icon: BookOpen, label: "Turmas" },
    { to: "/professor/atividades", icon: ClipboardList, label: "Atividades" },
    { to: "/professor/calendario", icon: Calendar, label: "Calendário" },
    { to: "/professor/biblioteca", icon: Library, label: "Biblioteca" },
    { to: "/professor/zios", icon: Sparkles, label: "ZIOS · IA" },
  ],
  aluno: [
    { to: "/aluno", icon: LayoutDashboard, label: "Painel" },
    { to: "/aluno/disciplinas", icon: BookOpen, label: "Disciplinas" },
    { to: "/aluno/atividades", icon: ClipboardList, label: "Atividades" },
    { to: "/aluno/calendario", icon: Calendar, label: "Calendário" },
    { to: "/aluno/biblioteca", icon: Library, label: "Biblioteca" },
    { to: "/aluno/zios", icon: Sparkles, label: "ZIOS · IA" },
  ],
};

export const FloatingSidebar = ({ role }: FloatingSidebarProps) => {
  const items = itemsByRole[role];
  const { pathname } = useLocation();
  const navigate = useNavigate();
  const { signOut } = useAuth();

  const handleLogout = async () => {
    await signOut();
    toast.success("Até logo!");
    navigate("/auth/login", { replace: true });
  };

  return (
    <TooltipProvider delayDuration={120}>
      <aside className="fixed left-4 top-1/2 -translate-y-1/2 z-40 animate-fade-in">
        <nav className="glass-strong rounded-2xl py-3 px-2 flex flex-col items-center gap-1">
          <NavLink to="/" className="mb-2 p-2 rounded-xl hover:bg-accent/60 transition-colors">
            <HemeraSun size={28} animated />
          </NavLink>
          <div className="w-8 h-px bg-border my-1" />

          {items.map((item) => {
            const active = pathname === item.to;
            const Icon = item.icon;
            return (
              <Tooltip key={item.to}>
                <TooltipTrigger asChild>
                  <NavLink
                    to={item.to}
                    className={cn(
                      "relative grid place-items-center w-11 h-11 rounded-xl transition-all duration-300",
                      "hover:bg-accent/70 hover:scale-105",
                      active && "bg-primary text-primary-foreground shadow-[var(--shadow-glow)]"
                    )}
                  >
                    <Icon className="h-5 w-5" />
                    {active && (
                      <span className="absolute -left-2 top-1/2 -translate-y-1/2 w-1 h-6 rounded-full bg-sun" />
                    )}
                  </NavLink>
                </TooltipTrigger>
                <TooltipContent side="right" className="glass-strong border-primary/20">
                  <span className="font-medium">{item.label}</span>
                </TooltipContent>
              </Tooltip>
            );
          })}

          <div className="w-8 h-px bg-border my-1" />
          <Tooltip>
            <TooltipTrigger asChild>
              <NavLink to={`/${role}/perfil`} className="grid place-items-center w-11 h-11 rounded-xl hover:bg-accent/70 transition-colors">
                <User className="h-5 w-5" />
              </NavLink>
            </TooltipTrigger>
            <TooltipContent side="right" className="glass-strong">Perfil</TooltipContent>
          </Tooltip>
          <Tooltip>
            <TooltipTrigger asChild>
              <button onClick={handleLogout} aria-label="Sair"
                className="grid place-items-center w-11 h-11 rounded-xl hover:bg-destructive/15 hover:text-destructive transition-colors">
                <LogOut className="h-5 w-5" />
              </button>
            </TooltipTrigger>
            <TooltipContent side="right" className="glass-strong">Sair</TooltipContent>
          </Tooltip>
        </nav>
      </aside>
    </TooltipProvider>
  );
};
