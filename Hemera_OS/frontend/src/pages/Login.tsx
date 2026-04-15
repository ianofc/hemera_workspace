import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Link } from "react-router-dom";
import { useLyv } from "@/contexts/LyvContext";
import { authService } from "@/services/api";
import { 
  Lock, User, ArrowRight, Loader2, AlertCircle, Eye, EyeOff, 
  ShieldCheck, Sparkles, Heart, MessageCircle, Repeat, Share2, 
  Bookmark, MoreHorizontal
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { toast } from "sonner";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";

// Ícone do Google
const GoogleIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" width="20px" height="20px">
    <path fill="#FFC107" d="M43.611,20.083H42V20H24v8h11.303c-1.649,4.657-6.08,8-11.303,8c-6.627,0-12-5.373-12-12c0-6.627,5.373-12,12-12c3.059,0,5.842,1.154,7.961,3.039l5.657-5.657C34.046,6.053,29.268,4,24,4C12.955,4,4,12.955,4,24c0,11.045,8.955,20,20,20C44,22.659,43.862,21.35,43.611,20.083z" />
    <path fill="#FF3D00" d="M6.306,14.691l6.571,4.819C14.655,15.108,18.961,12,24,12c3.059,0,5.842,1.154,7.961,3.039l5.657-5.657C34.046,6.053,29.268,4,24,4C16.318,4,9.656,8.337,6.306,14.691z" />
    <path fill="#4CAF50" d="M24,44c5.166,0,9.86-1.977,13.409-5.192l-6.19-5.238C29.211,35.091,26.715,36,24,36c-5.202,0-9.619-3.317-11.283-7.946l-6.522,5.025C9.505,39.556,16.227,44,24,44z" />
    <path fill="#1976D2" d="M43.611,20.083H42V20H24v8h11.303c-0.792,2.237-2.231,4.166-4.087,5.571c0.001-0.001,0.002-0.001,0.003-0.002l6.19,5.238C36.971,39.205,44,34,44,24C44,22.659,43.862,21.35,43.611,20.083z" />
  </svg>
);

const LyvIcon = ({ className }: { className?: string }) => (
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className}>
    <path d="M22 6c0-2.2-2-4-4-4-.8 0-2 .4-3 1-2-1-5-1-7 0a4 4 0 0 0-3-1 4 4 0 0 0-3 3 8 8 0 0 0 0 10c0 2.2 2 4 4 4 .8 0 2-.4 3-1 2 1 5 1 7 0a4 4 0 0 0 3-1 4 4 0 0 0 3-3V6z" />
    <path d="M14 9h.01" /><path d="M10 9h.01" /><path d="M12 14c1.5 0 2.5-.5 2.5-1.5" />
  </svg>
);

export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  const { login } = useLyv();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);

    try {
      const authData = await authService.login({ username, password });
      await login(username, authData.token);
      toast.success("Bem-vindo de volta!", { description: "Sessão iniciada com sucesso." });
      setTimeout(() => { window.location.replace("/"); }, 600);
    } catch (error: any) {
      let message = "Erro ao entrar";
      if (error.response?.status === 400 || error.response?.status === 401) message = "Usuário ou senha incorretos";
      else if (error.response?.status === 500) message = "Erro no servidor. Tente novamente.";
      else if (!error.response) message = "Servidor offline. Verifique se a API está rodando.";
      setError(message);
      setIsLoading(false);
    }
  };

  const handleGoogleLogin = () => { toast.info("Conectando ao Google Workspace..."); };

  return (
    <div className="relative flex items-center justify-center w-full min-h-screen p-4 overflow-hidden bg-[#FAF9FB]">
      
      {/* Background Aurora */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-40 -left-40 w-[600px] h-[600px] bg-cyan-200/40 rounded-full mix-blend-multiply filter blur-[100px] animate-pulse" />
        <div className="absolute top-1/4 -right-40 w-[500px] h-[500px] bg-blue-200/40 rounded-full mix-blend-multiply filter blur-[100px] animate-pulse delay-1000" />
        <div className="absolute -bottom-40 left-1/4 w-[600px] h-[600px] bg-purple-200/30 rounded-full mix-blend-multiply filter blur-[100px] animate-pulse delay-2000" />
        <div className="absolute inset-0 opacity-[0.02]" style={{ backgroundImage: `linear-gradient(#000 1px, transparent 1px), linear-gradient(90deg, #000 1px, transparent 1px)`, backgroundSize: '40px 40px' }} />
      </div>

      {/* CONTAINER CENTRALIZADO (Aproxima o Mockup do Login) */}
      <div className="relative z-10 flex flex-row items-center justify-center w-full max-w-[900px] gap-8 lg:gap-16">
        
        {/* LADO ESQUERDO: Mockup 3D Realista do Feed LYV */}
        <div className="hidden lg:flex shrink-0">
          <motion.div 
            initial={{ opacity: 0, y: 30, rotateY: -8 }} 
            animate={{ opacity: 1, y: 0, rotateY: 0 }} 
            transition={{ duration: 0.8, delay: 0.2 }}
            className="relative w-[340px] h-[680px] bg-slate-50/80 rounded-[3rem] shadow-[0_30px_60px_rgba(0,0,0,0.15),_inset_0_4px_10px_rgba(255,255,255,0.9),_inset_0_-4px_10px_rgba(0,0,0,0.05)] border-[8px] border-white overflow-hidden flex flex-col"
          >
             {/* Fundo do App */}
             <div className="absolute inset-0 bg-gradient-to-b from-slate-50 to-white/90 z-0"></div>

             {/* Notch Falso */}
             <div className="absolute top-2 left-1/2 -translate-x-1/2 w-28 h-6 bg-slate-900 rounded-full z-30 shadow-inner"></div>

             {/* Header do App */}
             <div className="relative z-10 pt-10 px-5 pb-3 flex items-center justify-between">
                <h2 className="font-black text-slate-800 text-xl tracking-tight flex items-center gap-1">
                  Lyv
                </h2>
                <div className="flex gap-3 text-slate-600">
                  <Heart className="w-5 h-5" />
                  <MessageCircle className="w-5 h-5" />
                </div>
             </div>

             <div className="relative z-10 flex-1 overflow-hidden flex flex-col">
                
                {/* Stories Bar Simulada */}
                <div className="flex gap-3 px-4 pb-3 border-b border-slate-100 overflow-hidden">
                  {[1, 2, 3, 4].map(i => (
                    <div key={i} className="shrink-0 flex flex-col items-center gap-1">
                      <div className="w-14 h-14 rounded-full p-0.5 bg-gradient-to-tr from-cyan-500 to-purple-600">
                        <div className="w-full h-full rounded-full border-[2px] border-white overflow-hidden bg-slate-200">
                          <img src={`https://i.pravatar.cc/150?u=${i}`} className="w-full h-full object-cover" alt="Story" />
                        </div>
                      </div>
                    </div>
                  ))}
                </div>

                {/* PostCard Simulado (Baseado no seu Print) */}
                <div className="p-4 mt-2">
                  <div className="bg-white/80 backdrop-blur-xl border border-white shadow-[0_4px_20px_rgba(0,0,0,0.05)] rounded-[2rem] p-4">
                    {/* Header do Post */}
                    <div className="flex items-center justify-between mb-3">
                      <div className="flex items-center gap-2">
                        <Avatar className="w-10 h-10 border border-slate-100">
                          <AvatarImage src="https://github.com/shadcn.png" />
                          <AvatarFallback>B</AvatarFallback>
                        </Avatar>
                        <div className="flex flex-col">
                          <span className="font-bold text-[13px] text-slate-900 flex items-center gap-1">
                            Sistema LYV <Sparkles className="w-3 h-3 text-amber-500 fill-amber-500" />
                          </span>
                          <span className="text-[10px] text-slate-500">@lyv_admin • Agora</span>
                        </div>
                      </div>
                      <MoreHorizontal className="w-4 h-4 text-slate-400" />
                    </div>
                    
                    {/* Texto */}
                    <p className="text-[13px] text-slate-700 leading-tight mb-3">
                      O sistema LYV está oficialmente operacional. Explorando as novas capacidades do layout em mosaico! 🦅 <span className="text-cyan-600 font-medium">#Soberania</span>
                    </p>

                    {/* Mosaico de Imagens */}
                    <div className="grid grid-cols-2 grid-rows-2 gap-1 rounded-xl overflow-hidden h-40 border border-slate-100">
                      <img src="https://images.unsplash.com/photo-1516483638261-f4dbaf036963?w=300&fit=crop" className="w-full h-full object-cover" />
                      <img src="https://images.unsplash.com/photo-1523906834658-6e24ef2386f9?w=300&fit=crop" className="w-full h-full object-cover" />
                      <img src="https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=300&fit=crop" className="w-full h-full object-cover" />
                      <img src="https://images.unsplash.com/photo-1470252649378-9c29740c9fa8?w=300&fit=crop" className="w-full h-full object-cover" />
                    </div>

                    {/* Rodapé do Post */}
                    <div className="flex items-center justify-between mt-3 pt-3 border-t border-slate-100">
                      <div className="flex items-center gap-4">
                        <div className="flex items-center gap-1 text-[11px] font-bold text-rose-500">
                          <Heart className="w-4 h-4 fill-rose-500" /> 150
                        </div>
                        <div className="flex items-center gap-1 text-[11px] font-bold text-slate-500">
                          <MessageCircle className="w-4 h-4" /> 12
                        </div>
                        <div className="flex items-center gap-1 text-[11px] font-bold text-slate-500">
                          <Repeat className="w-4 h-4" /> 8
                        </div>
                      </div>
                      <div className="flex gap-2 text-slate-400">
                        <Share2 className="w-4 h-4" />
                        <Bookmark className="w-4 h-4" />
                      </div>
                    </div>
                  </div>
                </div>

             </div>
          </motion.div>
        </div>

        {/* LADO DIREITO: Card de Login (Glassmorphism Soft) */}
        <div className="w-full max-w-[420px] flex-shrink-0">
          <motion.div 
            initial={{ opacity: 0, x: 20 }} 
            animate={{ opacity: 1, x: 0 }} 
            transition={{ duration: 0.5 }}
            className="relative w-full bg-white/70 backdrop-blur-2xl border border-white shadow-[0_8px_32px_rgba(0,0,0,0.06)] rounded-[2.5rem] overflow-hidden"
          >
            <div className="absolute opacity-40 -inset-1 bg-gradient-to-r from-cyan-400/20 via-purple-400/20 to-blue-400/20 rounded-[2rem] blur-xl -z-10" />

            <div className="px-8 pt-10 pb-6 text-center relative z-10">
              <div className="relative inline-flex items-center justify-center w-16 h-16 mb-6 shadow-xl rounded-2xl bg-gradient-to-br from-cyan-500 to-purple-600 shadow-cyan-500/30">
                <LyvIcon className="relative z-10 w-8 h-8 text-white" />
                <Sparkles className="absolute w-4 h-4 text-yellow-300 -top-1 -right-1 animate-pulse" />
              </div>
              <h1 className="mb-2 text-2xl font-black text-slate-800 tracking-tight">Bem-vindo ao Lyv</h1>
              <p className="text-sm font-medium text-slate-500">SISTEMA OPERATIVO DE VIDA</p>
            </div>

            <div className="px-8 pb-8 relative z-10">
              <form onSubmit={handleLogin} className="space-y-5">
                
                <AnimatePresence>
                  {error && (
                    <motion.div initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: 'auto' }} exit={{ opacity: 0, height: 0 }} className="flex items-start gap-3 p-4 text-sm text-rose-600 border border-rose-100 rounded-xl bg-rose-50/80 mb-4">
                      <AlertCircle className="w-5 h-5 shrink-0 mt-0.5" /> <span>{error}</span>
                    </motion.div>
                  )}
                </AnimatePresence>

                <div className="space-y-2">
                  <label className="ml-1 text-xs font-bold text-slate-600 uppercase tracking-wider">Nome de utilizador</label>
                  <div className="relative">
                     <User className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                    <input
                      type="text" placeholder="Utilizador ou e-mail" value={username} onChange={(e) => setUsername(e.target.value)} disabled={isLoading} required
                      className="w-full h-12 pl-12 pr-4 transition-all shadow-sm bg-white/80 border border-slate-200 rounded-xl text-slate-800 placeholder:text-slate-400 focus:outline-none focus:border-purple-400 focus:ring-4 focus:ring-purple-500/10 disabled:opacity-50 text-sm font-medium"
                    />
                  </div>
                </div>

                <div className="space-y-2">
                  <div className="flex items-center justify-between ml-1">
                    <label className="text-xs font-bold text-slate-600 uppercase tracking-wider">Palavra-chave</label>
                  </div>
                  <div className="relative">
                    <Lock className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                    <input
                      type={showPassword ? "text" : "password"} placeholder="••••••••" value={password} onChange={(e) => setPassword(e.target.value)} disabled={isLoading} required
                      className="w-full h-12 pl-12 pr-12 transition-all shadow-sm bg-white/80 border border-slate-200 rounded-xl text-slate-800 placeholder:text-slate-400 focus:outline-none focus:border-purple-400 focus:ring-4 focus:ring-purple-500/10 disabled:opacity-50 text-sm font-medium"
                    />
                    <button type="button" onClick={() => setShowPassword(!showPassword)} className="absolute p-2 transition-colors -translate-y-1/2 rounded-lg right-2 top-1/2 text-slate-400 hover:text-slate-600">
                      {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                    </button>
                  </div>
                </div>

                <Button type="submit" disabled={isLoading || !username || !password} className="w-full h-12 mt-2 font-bold text-white transition-all duration-300 shadow-lg bg-purple-600 hover:bg-purple-700 rounded-xl shadow-purple-500/30 disabled:opacity-50 disabled:cursor-not-allowed group border-0">
                  {isLoading ? <Loader2 className="w-5 h-5 animate-spin" /> : "Iniciar Sessão"}
                </Button>
              </form>

              <div className="relative my-6">
                <div className="absolute inset-0 flex items-center"><div className="w-full border-t border-slate-200"></div></div>
                <div className="relative flex justify-center text-xs"><span className="px-4 font-semibold text-slate-400 bg-white/80 backdrop-blur-sm">ou</span></div>
              </div>

              <button onClick={handleGoogleLogin} className="w-full flex items-center justify-center gap-3 py-3 bg-white border border-slate-200 hover:bg-slate-50 transition-colors rounded-xl text-sm font-bold text-slate-700 shadow-sm">
                <GoogleIcon /> Entrar com Google
              </button>

              <div className="mt-5 text-center">
                <Link to="/forgot-password" className="text-xs font-bold transition-colors text-purple-600 hover:text-purple-700">
                  Esqueceu-se da palavra-chave?
                </Link>
              </div>
            </div>
            
            <div className="flex items-center justify-center gap-2 px-8 py-4 text-xs font-medium border-t bg-slate-50/80 border-slate-100 text-slate-500">
              <ShieldCheck className="w-4 h-4 text-emerald-500" />
              <span>Protegido por criptografia AES-256</span>
            </div>
          </motion.div>
          
          <div className="mt-6 text-center bg-white/50 backdrop-blur-sm py-3 px-6 rounded-xl border border-white/50 shadow-sm inline-block mx-auto w-full">
            <p className="text-sm font-medium text-slate-600">
              Não tem uma conta?{' '}
              <Link to="/signup" className="font-bold text-purple-600 hover:text-purple-700 transition-colors underline decoration-purple-300 underline-offset-4">
                Registe-se
              </Link>
            </p>
          </div>
        </div>

      </div>
    </div>
  );
}