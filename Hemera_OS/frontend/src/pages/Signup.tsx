import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Link, useNavigate } from "react-router-dom";
import { authService } from "@/services/api";
import { useHemera } from "@/contexts/HemeraContext";
import { 
  Lock, User, AlertCircle, Loader2, Mail, ShieldCheck, Sparkles, Eye, EyeOff, LayoutDashboard, Sun 
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { toast } from "sonner";

export default function Signup() {
  const [name, setName] = useState("");
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  const { login } = useHemera();
  const navigate = useNavigate();

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);

    try {
      // Simula a criação de conta pela Mock API
      const authData = await authService.register({ name, username, email, password });
      
      // Auto-Login
      await login(authData.user.username || username, authData.token);
      
      toast.success("Conta Criada!", { description: "Bem-vindo ao Hemera OS." });
      navigate("/");
    } catch (err: any) {
      setError(err.response?.data?.detail || "Erro ao registrar. Tente novamente.");
      setIsLoading(false);
    }
  };

  return (
    <div className="relative flex items-center justify-center w-full min-h-screen p-4 overflow-hidden bg-[#FAF9FB]">
      
      {/* Background Aurora */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-40 -left-60 w-[700px] h-[700px] bg-amber-200/40 rounded-full mix-blend-multiply filter blur-[120px] animate-pulse" />
        <div className="absolute top-1/4 -right-20 w-[500px] h-[500px] bg-orange-200/40 rounded-full mix-blend-multiply filter blur-[100px] animate-pulse delay-1000" />
        <div className="absolute -bottom-40 left-1/4 w-[600px] h-[600px] bg-sky-200/30 rounded-full mix-blend-multiply filter blur-[100px] animate-pulse delay-2000" />
        <div className="absolute inset-0 opacity-[0.02]" style={{ backgroundImage: `linear-gradient(#000 1px, transparent 1px), linear-gradient(90deg, #000 1px, transparent 1px)`, backgroundSize: '40px 40px' }} />
      </div>

      <div className="relative z-10 flex flex-col md:flex-row items-center justify-center w-full max-w-[1000px] gap-8 lg:gap-16">
        
        {/* TEXTO INSPIRACIONAL (ESQUERDA) */}
        <div className="hidden md:flex flex-col text-left max-w-[400px]">
           <motion.div initial={{ opacity: 0, x: -30 }} animate={{ opacity: 1, x: 0 }} transition={{ duration: 0.8 }}>
              <div className="inline-flex items-center gap-2 px-3 py-1 mb-6 text-xs font-bold text-amber-700 bg-amber-100/80 rounded-full">
                <Sparkles className="w-3 h-3" /> Junte-se ao Hemera
              </div>
              <h1 className="text-4xl font-black text-slate-800 tracking-tight leading-tight mb-4">
                Expanda sua <br/><span className="text-transparent bg-clip-text bg-gradient-to-r from-amber-500 to-orange-500">experiência educacional</span>.
              </h1>
              <p className="text-slate-600 mb-8 leading-relaxed">
                O Hemera OS redefine a forma como as escolas, alunos e pais interagem. Conecte-se e tenha uma inteligência ao seu favor.
              </p>
              
              <div className="space-y-4">
                <div className="flex items-center gap-3 text-sm text-slate-700 font-medium">
                  <div className="w-8 h-8 rounded-full bg-cyan-100 flex items-center justify-center text-cyan-600"><LayoutDashboard className="w-4 h-4" /></div>
                  Dashboards Proativos
                </div>
                <div className="flex items-center gap-3 text-sm text-slate-700 font-medium">
                  <div className="w-8 h-8 rounded-full bg-purple-100 flex items-center justify-center text-purple-600"><Sparkles className="w-4 h-4" /></div>
                  Aconselhamento por Inteligência Artificial
                </div>
                <div className="flex items-center gap-3 text-sm text-slate-700 font-medium">
                  <div className="w-8 h-8 rounded-full bg-rose-100 flex items-center justify-center text-rose-600"><ShieldCheck className="w-4 h-4" /></div>
                  Privacidade Total by Heimdall
                </div>
              </div>
           </motion.div>
        </div>

        {/* LADO DIREITO: Card de Registro (Glassmorphism Soft) */}
        <div className="w-full max-w-[420px] flex-shrink-0">
          <motion.div 
            initial={{ opacity: 0, x: 20 }} 
            animate={{ opacity: 1, x: 0 }} 
            transition={{ duration: 0.5 }}
            className="relative w-full bg-white/70 backdrop-blur-2xl border border-white shadow-[0_8px_32px_rgba(0,0,0,0.06)] rounded-[2.5rem] overflow-hidden"
          >
            <div className="absolute opacity-40 -inset-1 bg-gradient-to-l from-amber-400/20 via-orange-400/20 to-sky-400/20 rounded-[2rem] blur-xl -z-10" />

            <div className="px-8 pt-8 pb-4 text-center relative z-10">
              <div className="relative inline-flex items-center justify-center w-14 h-14 mb-4 shadow-xl rounded-2xl bg-gradient-to-br from-amber-400 to-orange-500 shadow-amber-500/30">
                <Sun className="relative z-10 w-7 h-7 text-white" />
              </div>
              <h2 className="mb-1 text-2xl font-black text-slate-800 tracking-tight">Criar Conta</h2>
              <p className="text-xs font-medium text-slate-500">PREENCHA SEUS DADOS</p>
            </div>

            <div className="px-8 pb-8 relative z-10">
              <form onSubmit={handleRegister} className="space-y-4">
                
                <AnimatePresence>
                  {error && (
                    <motion.div initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: 'auto' }} exit={{ opacity: 0, height: 0 }} className="flex items-start gap-3 p-4 text-sm text-rose-600 border border-rose-100 rounded-xl bg-rose-50/80 mb-4">
                      <AlertCircle className="w-5 h-5 shrink-0 mt-0.5" /> <span>{error}</span>
                    </motion.div>
                  )}
                </AnimatePresence>

                {/* Nome */}
                <div className="space-y-1">
                  <div className="relative">
                     <User className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                    <input
                      type="text" placeholder="Seu nome completo" value={name} onChange={(e) => setName(e.target.value)} disabled={isLoading} required
                      className="w-full h-11 pl-11 pr-4 transition-all shadow-sm bg-white/80 border border-slate-200 rounded-xl text-slate-800 placeholder:text-slate-400 focus:outline-none focus:border-cyan-400 focus:ring-4 focus:ring-cyan-500/10 disabled:opacity-50 text-sm font-medium"
                    />
                  </div>
                </div>

                {/* Username */}
                <div className="space-y-1">
                  <div className="relative">
                     <User className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                    <input
                      type="text" placeholder="Nome de utilizador" value={username} onChange={(e) => setUsername(e.target.value)} disabled={isLoading} required
                      className="w-full h-11 pl-11 pr-4 transition-all shadow-sm bg-white/80 border border-slate-200 rounded-xl text-slate-800 placeholder:text-slate-400 focus:outline-none focus:border-cyan-400 focus:ring-4 focus:ring-cyan-500/10 disabled:opacity-50 text-sm font-medium"
                    />
                  </div>
                </div>

                {/* Email */}
                <div className="space-y-1">
                  <div className="relative">
                     <Mail className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                    <input
                      type="email" placeholder="E-mail" value={email} onChange={(e) => setEmail(e.target.value)} disabled={isLoading} required
                      className="w-full h-11 pl-11 pr-4 transition-all shadow-sm bg-white/80 border border-slate-200 rounded-xl text-slate-800 placeholder:text-slate-400 focus:outline-none focus:border-cyan-400 focus:ring-4 focus:ring-cyan-500/10 disabled:opacity-50 text-sm font-medium"
                    />
                  </div>
                </div>

                {/* Senha */}
                <div className="space-y-1">
                  <div className="relative">
                    <Lock className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                    <input
                      type={showPassword ? "text" : "password"} placeholder="Palavra-chave" value={password} onChange={(e) => setPassword(e.target.value)} disabled={isLoading} required
                      className="w-full h-11 pl-11 pr-11 transition-all shadow-sm bg-white/80 border border-slate-200 rounded-xl text-slate-800 placeholder:text-slate-400 focus:outline-none focus:border-cyan-400 focus:ring-4 focus:ring-cyan-500/10 disabled:opacity-50 text-sm font-medium"
                    />
                    <button type="button" onClick={() => setShowPassword(!showPassword)} className="absolute p-2 transition-colors -translate-y-1/2 rounded-lg right-2 top-1/2 text-slate-400 hover:text-slate-600">
                      {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                    </button>
                  </div>
                </div>

                <Button type="submit" disabled={isLoading || !username || !password} className="w-full h-12 mt-4 font-bold text-white transition-all duration-300 shadow-lg bg-slate-900 hover:bg-slate-800 rounded-xl shadow-slate-900/30 disabled:opacity-50 disabled:cursor-not-allowed group border-0">
                  {isLoading ? <Loader2 className="w-5 h-5 animate-spin" /> : "Registar"}
                </Button>
              </form>
            </div>
            
            <div className="flex items-center justify-center gap-2 px-8 py-4 text-xs font-medium border-t bg-slate-50/80 border-slate-100 text-slate-500">
              <ShieldCheck className="w-4 h-4 text-cyan-500" />
              <span>Criação Segura by Heimdall</span>
            </div>
          </motion.div>
          
          <div className="mt-6 text-center bg-white/50 backdrop-blur-sm py-3 px-6 rounded-xl border border-white/50 shadow-sm inline-block mx-auto w-full">
            <p className="text-sm font-medium text-slate-600">
              Já tem uma conta?{' '}
              <Link to="/login" className="font-bold text-amber-600 hover:text-amber-700 transition-colors underline decoration-amber-300 underline-offset-4">
                Entrar
              </Link>
            </p>
          </div>
        </div>

      </div>
    </div>
  );
}
