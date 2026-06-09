import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Route, Routes, Navigate } from "react-router-dom";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { Toaster } from "@/components/ui/toaster";
import { TooltipProvider } from "@/components/ui/tooltip";
import AlunoDashboard from "./pages/AlunoDashboard";
import AlunoCursos from "./pages/AlunoCursos";
import AlunoNotas from "./pages/AlunoNotas";
import ProfessorDashboard from "./pages/ProfessorDashboard";
import SalaDeAula from "./pages/SalaDeAula";
import Biblioteca from "./pages/Biblioteca";
import CrecheDashboard from "./pages/CrecheDashboard";
import FundamentalDashboard from "./pages/FundamentalDashboard";
import MedioDashboard from "./pages/MedioDashboard";
import GraduacaoDashboard from "./pages/GraduacaoDashboard";
import Profile from "./pages/Profile";
import OlimpoDashboard from "./pages/OlimpoDashboard";
import NotFound from "./pages/NotFound";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import { AuthProvider } from "./hooks/useAuth";
import { LyceumProvider } from "./contexts/LyceumContext";
import { ProtectedRoute } from "./components/ProtectedRoute";

const queryClient = new QueryClient();

const App = () => (
  <QueryClientProvider client={queryClient}>
    <TooltipProvider>
      <AuthProvider>
        <LyceumProvider>
          <Toaster />
          <Sonner />
          <BrowserRouter
            future={{ 
              v7_startTransition: true, 
              v7_relativeSplatPath: true 
            }}
          >
            <Routes>
              {/* Rotas Públicas */}
              <Route path="/login" element={<Login />} />
              <Route path="/signup" element={<Signup />} />
              <Route path="/" element={<Navigate to="/login" replace />} />
              
              {/* Rotas Protegidas */}
              <Route path="/creche" element={<ProtectedRoute><CrecheDashboard /></ProtectedRoute>} />
              <Route path="/fundamental" element={<ProtectedRoute><FundamentalDashboard /></ProtectedRoute>} />
              <Route path="/medio" element={<ProtectedRoute><MedioDashboard /></ProtectedRoute>} />
              <Route path="/graduacao" element={<ProtectedRoute><GraduacaoDashboard /></ProtectedRoute>} />
              
              <Route path="/aluno" element={<ProtectedRoute requireRole="aluno"><AlunoDashboard /></ProtectedRoute>} />
              <Route path="/aluno/cursos" element={<ProtectedRoute requireRole="aluno"><AlunoCursos /></ProtectedRoute>} />
              <Route path="/aluno/notas" element={<ProtectedRoute requireRole="aluno"><AlunoNotas /></ProtectedRoute>} />
              <Route path="/disciplinas" element={<ProtectedRoute requireRole="aluno"><AlunoDashboard /></ProtectedRoute>} />
              <Route path="/desempenho" element={<ProtectedRoute requireRole="aluno"><AlunoDashboard /></ProtectedRoute>} />
              <Route path="/biblioteca" element={<ProtectedRoute><Biblioteca /></ProtectedRoute>} />
              <Route path="/sala-de-aula/:id" element={<ProtectedRoute><SalaDeAula /></ProtectedRoute>} />
              
              <Route path="/professor" element={<ProtectedRoute requireRole="professor"><ProfessorDashboard /></ProtectedRoute>} />
              <Route path="/professor/*" element={<ProtectedRoute requireRole="professor"><ProfessorDashboard /></ProtectedRoute>} />
              
              <Route path="/olimpo" element={<ProtectedRoute requireRole="admin"><OlimpoDashboard /></ProtectedRoute>} />
            <Route path="/olimpo/*" element={<ProtectedRoute requireRole="admin"><OlimpoDashboard /></ProtectedRoute>} />
            <Route path="/profile" element={<ProtectedRoute><Profile /></ProtectedRoute>} />
              
              <Route path="*" element={<NotFound />} />
            </Routes>
          </BrowserRouter>
        </LyceumProvider>
      </AuthProvider>
    </TooltipProvider>
  </QueryClientProvider>
);

export default App;
