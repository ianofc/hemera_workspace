import { Outlet } from "react-router-dom";
import {
  SidebarProvider,
  SidebarTrigger,
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupLabel,
  SidebarGroupContent,
  SidebarMenu,
  SidebarMenuItem,
  SidebarMenuButton,
  useSidebar,
} from "@/components/ui/sidebar";
import { NavLink } from "@/components/NavLink";
import { useLocation } from "react-router-dom";
import { useAuth } from "@/hooks/useAuth";
import {
  LayoutDashboard, Users, BookOpen, ClipboardList,
  Calendar, BarChart3, FileText, LogOut, GraduationCap,
  MessageCircle, Library
} from "lucide-react";
import logo from "@/assets/hemera-logo.png";
import { Button } from "@/components/ui/button";

const professorLinks = [
  { title: "Painel", url: "/dashboard", icon: LayoutDashboard },
  { title: "Minhas Turmas", url: "/dashboard/turmas", icon: Users },
  { title: "Diário de Classe", url: "/dashboard/diario", icon: ClipboardList },
  { title: "Materiais & Aulas", url: "/dashboard/materiais", icon: BookOpen },
  { title: "Avaliações", url: "/dashboard/avaliacoes", icon: FileText },
  { title: "Planejamento", url: "/dashboard/planejamento", icon: Calendar },
  { title: "Biblioteca", url: "/dashboard/biblioteca", icon: Library },
  { title: "Mensagens", url: "/dashboard/mensagens", icon: MessageCircle },
];

const alunoLinks = [
  { title: "Painel", url: "/dashboard", icon: LayoutDashboard },
  { title: "Minhas Aulas", url: "/dashboard/aulas", icon: BookOpen },
  { title: "Notas & Boletim", url: "/dashboard/notas", icon: BarChart3 },
  { title: "Atividades", url: "/dashboard/atividades", icon: ClipboardList },
  { title: "Avaliações", url: "/dashboard/avaliacoes-aluno", icon: FileText },
  { title: "Biblioteca", url: "/dashboard/biblioteca", icon: Library },
  { title: "Mensagens", url: "/dashboard/mensagens", icon: MessageCircle },
];

function AppSidebar() {
  const { state } = useSidebar();
  const collapsed = state === "collapsed";
  const location = useLocation();
  const { user } = useAuth();

  // For now, show professor links by default. Role-based switching comes with DB roles.
  const links = professorLinks;

  return (
    <Sidebar collapsible="icon">
      <SidebarContent>
        <div className={`p-4 flex items-center gap-2 ${collapsed ? "justify-center" : ""}`}>
          <img src={logo} alt="Hemera" className="w-7 h-7" />
          {!collapsed && <span className="font-display text-lg text-sidebar-foreground">Hemera</span>}
        </div>

        <SidebarGroup>
          <SidebarGroupLabel>Navegação</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              {links.map((item) => (
                <SidebarMenuItem key={item.title}>
                  <SidebarMenuButton asChild>
                    <NavLink
                      to={item.url}
                      end={item.url === "/dashboard"}
                      className="hover:bg-sidebar-accent/50"
                      activeClassName="bg-sidebar-accent text-sidebar-primary font-medium"
                    >
                      <item.icon className="mr-2 h-4 w-4" />
                      {!collapsed && <span>{item.title}</span>}
                    </NavLink>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              ))}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
    </Sidebar>
  );
}

const DashboardLayout = () => {
  const { signOut } = useAuth();

  return (
    <SidebarProvider>
      <div className="min-h-screen flex w-full">
        <AppSidebar />
        <div className="flex-1 flex flex-col">
          <header className="h-14 flex items-center justify-between border-b bg-card px-4">
            <SidebarTrigger className="ml-0" />
            <Button variant="ghost" size="sm" onClick={signOut} className="text-muted-foreground gap-2">
              <LogOut className="w-4 h-4" />
              <span className="hidden sm:inline">Sair</span>
            </Button>
          </header>
          <main className="flex-1 p-6 overflow-auto">
            <Outlet />
          </main>
        </div>
      </div>
    </SidebarProvider>
  );
};

export default DashboardLayout;
