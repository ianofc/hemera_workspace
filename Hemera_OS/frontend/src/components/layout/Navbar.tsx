import { useState } from "react";
import { Link, useLocation } from "react-router-dom";

interface NavItem {
  label: string;
  icon: string;
  path: string;
}

interface NavbarProps {
  role: "aluno" | "professor";
}

const alunoNav: NavItem[] = [
  { label: "Início", icon: "fas fa-home", path: "/" },
  { label: "Disciplinas", icon: "fas fa-book-open", path: "/disciplinas" },
  { label: "Desempenho", icon: "fas fa-chart-line", path: "/desempenho" },
  { label: "Biblioteca", icon: "fas fa-bookmark", path: "/biblioteca" },
];

const professorNav: NavItem[] = [
  { label: "Painel", icon: "fas fa-layer-group", path: "/professor" },
  { label: "Turmas", icon: "fas fa-users", path: "/professor/turmas" },
  { label: "Planejamento", icon: "fas fa-calendar-alt", path: "/professor/planejamento" },
  { label: "Avaliações", icon: "fas fa-clipboard-check", path: "/professor/avaliacoes" },
];

const Navbar = ({ role }: NavbarProps) => {
  const [userMenuOpen, setUserMenuOpen] = useState(false);
  const location = useLocation();
  const navItems = role === "aluno" ? alunoNav : professorNav;
  const isAluno = role === "aluno";

  const logoIcon = isAluno ? "fas fa-atom" : "fas fa-chalkboard-teacher";
  const subtitle = isAluno ? "Ambiente do Aluno" : "Portal do Docente";
  const homePath = isAluno ? "/" : "/professor";

  return (
    <nav className="sticky top-0 z-50 w-full transition-all duration-300 shadow-sm glass-nav">
      <div className="max-w-[1600px] mx-auto px-6 h-20 flex items-center justify-between">
        {/* Logo */}
        <Link to={homePath} className="flex items-center gap-3 group">
          <div className="relative flex items-center justify-center w-10 h-10 rounded-xl bg-gradient-to-br from-primary to-secondary shadow-neon transition-transform group-hover:scale-105 text-primary-foreground">
            <i className={`${logoIcon} text-lg`} />
          </div>
          <div className="flex flex-col">
            <span className="text-lg font-bold tracking-tight text-foreground font-display group-hover:text-primary transition-colors">
              Lumenios
            </span>
            <span className="text-[9px] font-bold tracking-[0.2em] uppercase text-muted-foreground">
              {subtitle}
            </span>
          </div>
        </Link>

        {/* Center nav pills */}
        <div className="hidden md:flex items-center bg-card/50 backdrop-blur-md px-2 py-1.5 rounded-full border border-border/50 shadow-inner gap-1">
          {navItems.map((item) => {
            const isActive = location.pathname === item.path;
            return (
              <Link
                key={item.path}
                to={item.path}
                className={`flex items-center gap-2 px-5 py-2 text-sm font-bold transition-all rounded-full ${
                  isActive
                    ? "bg-card text-primary shadow-sm"
                    : "text-muted-foreground hover:text-primary hover:bg-card"
                }`}
              >
                <i className={item.icon} /> {item.label}
              </Link>
            );
          })}
        </div>

        {/* Right side */}
        <div className="flex items-center gap-4">
          <button className="flex items-center justify-center w-10 h-10 transition border rounded-full shadow-sm bg-card/60 hover:bg-card text-muted-foreground hover:text-accent border-border">
            <i className={isAluno ? "far fa-bell" : "fas fa-inbox"} />
          </button>

          <div className="relative pl-4 border-l border-border">
            <button
              onClick={() => setUserMenuOpen(!userMenuOpen)}
              className="flex items-center gap-3 group"
            >
              <div className="hidden text-right lg:block">
                <p className="text-xs font-bold text-foreground">
                  {isAluno ? "Estudante" : "Professor"}
                </p>
                <p className="text-[10px] text-muted-foreground font-bold uppercase">
                  {isAluno ? "Matriculado" : "Docente"}
                </p>
              </div>
              <img
                src={`https://ui-avatars.com/api/?name=${isAluno ? "Aluno" : "Prof"}&background=${isAluno ? "6366f1" : "a855f7"}&color=fff`}
                alt="Avatar"
                className="object-cover w-10 h-10 transition-colors border-2 border-card shadow-sm rounded-xl group-hover:border-primary"
              />
            </button>

            {userMenuOpen && (
              <div className="absolute right-0 w-56 p-2 space-y-1 border shadow-xl top-12 bg-card/90 backdrop-blur-xl rounded-2xl border-border/50 z-50">
                <Link
                  to="#"
                  className="flex items-center gap-3 px-3 py-2 text-xs font-bold transition rounded-xl text-foreground hover:bg-muted hover:text-primary"
                  onClick={() => setUserMenuOpen(false)}
                >
                  <i className={`w-4 ${isAluno ? "fas fa-id-card" : "fas fa-user-tie"}`} />
                  {isAluno ? "Carteirinha" : "Meu Perfil"}
                </Link>
                <Link
                  to="#"
                  className="flex items-center gap-3 px-3 py-2 text-xs font-bold transition rounded-xl text-foreground hover:bg-muted hover:text-primary"
                  onClick={() => setUserMenuOpen(false)}
                >
                  <i className="w-4 fas fa-cog" /> Configurações
                </Link>
                <div className="h-px my-1 bg-muted" />
                <button className="flex items-center gap-3 px-3 py-2 text-xs font-bold transition rounded-xl text-destructive hover:bg-destructive/10 w-full">
                  <i className="w-4 fas fa-sign-out-alt" /> Sair
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
