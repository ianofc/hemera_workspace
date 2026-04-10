import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { Toaster } from "@/components/ui/toaster";
import { TooltipProvider } from "@/components/ui/tooltip";
import { AuthProvider, RequireAuth } from "@/hooks/useAuth";
import Index from "./pages/Index";
import Auth from "./pages/Auth";
import NotFound from "./pages/NotFound";
import DashboardLayout from "./components/layouts/DashboardLayout";
import DashboardHome from "./pages/dashboard/DashboardHome";
import TurmasPage from "./pages/dashboard/TurmasPage";
import DiarioPage from "./pages/dashboard/DiarioPage";
import MateriaisPage from "./pages/dashboard/MateriaisPage";
import NotasPage from "./pages/dashboard/NotasPage";
import BibliotecaPage from "./pages/dashboard/BibliotecaPage";
import {
  AvaliacoesPage,
  PlanejamentoPage,
  MensagensPage,
  AulasAlunoPage,
  AtividadesPage,
  AvaliacoesAlunoPage,
} from "./pages/dashboard/PlaceholderPages";

const queryClient = new QueryClient();

const App = () => (
  <QueryClientProvider client={queryClient}>
    <TooltipProvider>
      <Toaster />
      <Sonner />
      <BrowserRouter>
        <AuthProvider>
          <Routes>
            <Route path="/" element={<Index />} />
            <Route path="/auth" element={<Auth />} />

            <Route
              path="/dashboard"
              element={
                <RequireAuth>
                  <DashboardLayout />
                </RequireAuth>
              }
            >
              <Route index element={<DashboardHome />} />
              <Route path="turmas" element={<TurmasPage />} />
              <Route path="diario" element={<DiarioPage />} />
              <Route path="materiais" element={<MateriaisPage />} />
              <Route path="avaliacoes" element={<AvaliacoesPage />} />
              <Route path="planejamento" element={<PlanejamentoPage />} />
              <Route path="biblioteca" element={<BibliotecaPage />} />
              <Route path="mensagens" element={<MensagensPage />} />
              <Route path="notas" element={<NotasPage />} />
              <Route path="aulas" element={<AulasAlunoPage />} />
              <Route path="atividades" element={<AtividadesPage />} />
              <Route path="avaliacoes-aluno" element={<AvaliacoesAlunoPage />} />
            </Route>

            <Route path="*" element={<NotFound />} />
          </Routes>
        </AuthProvider>
      </BrowserRouter>
    </TooltipProvider>
  </QueryClientProvider>
);

export default App;
