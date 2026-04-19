import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { Toaster } from "@/components/ui/toaster";
import { TooltipProvider } from "@/components/ui/tooltip";
import Index from "./pages/Index";
import AlunoDashboard from "./pages/AlunoDashboard";
import ProfessorDashboard from "./pages/ProfessorDashboard";
import SalaDeAula from "./pages/SalaDeAula";
import Biblioteca from "./pages/Biblioteca";
import CrecheDashboard from "./pages/CrecheDashboard";
import FundamentalDashboard from "./pages/FundamentalDashboard";
import MedioDashboard from "./pages/MedioDashboard";
import GraduacaoDashboard from "./pages/GraduacaoDashboard";
import Profile from "./pages/Profile";
import NotFound from "./pages/NotFound";

const queryClient = new QueryClient();

const App = () => (
  <QueryClientProvider client={queryClient}>
    <TooltipProvider>
      <Toaster />
      <Sonner />
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Index />} />
          <Route path="/creche" element={<CrecheDashboard />} />
          <Route path="/fundamental" element={<FundamentalDashboard />} />
          <Route path="/medio" element={<MedioDashboard />} />
          <Route path="/graduacao" element={<GraduacaoDashboard />} />
          <Route path="/aluno" element={<AlunoDashboard />} />
          <Route path="/disciplinas" element={<AlunoDashboard />} />
          <Route path="/desempenho" element={<AlunoDashboard />} />
          <Route path="/biblioteca" element={<Biblioteca />} />
          <Route path="/sala-de-aula/:id" element={<SalaDeAula />} />
          <Route path="/professor" element={<ProfessorDashboard />} />
          <Route path="/professor/*" element={<ProfessorDashboard />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </BrowserRouter>
    </TooltipProvider>
  </QueryClientProvider>
);

export default App;
