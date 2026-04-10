import { useState } from 'react';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { GlassCard } from '../../components/ui/GlassCard';
import { useAuthStore } from '../../store/authStore';
import { BookOpen, Sparkles } from 'lucide-react';

export const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();
  const { login } = useAuthStore();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await login(email, password);
    navigate('/student');
  };

  return (
    <div className="w-full max-w-md px-4">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <div className="text-center mb-8">
          <div className="w-20 h-20 mx-auto mb-4 rounded-2xl bg-gradient-to-br from-alpine-400 to-zeus-primary flex items-center justify-center shadow-xl">
            <BookOpen size={40} className="text-white" />
          </div>
          <h1 className="text-4xl font-bold text-gradient mb-2">ATHENES</h1>
          <p className="text-slate-600">Ambiente Virtual de Aprendizagem</p>
        </div>

        <GlassCard className="p-8">
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">Email</label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full glass-input"
                placeholder="seu@email.com"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">Senha</label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full glass-input"
                placeholder="••••••••"
              />
            </div>

            <button
              type="submit"
              className="w-full glass-button bg-gradient-to-r from-alpine-500 to-zeus-primary text-white border-0 hover:opacity-90"
            >
              Entrar
            </button>
          </form>

          <div className="mt-6 pt-6 border-t border-white/40">
            <div className="flex items-center justify-center gap-2 text-sm text-slate-600">
              <Sparkles size={16} className="text-zeus-primary" />
              <span>Powered by Zeus AI</span>
            </div>
          </div>
        </GlassCard>
      </motion.div>
    </div>
  );
};