import { motion } from 'framer-motion';
import { Users, BookOpen, Eye, Star, Plus, BarChart2 } from 'lucide-react';
import { GlassCard } from '../../components/ui/GlassCard';
import { useNavigate } from 'react-router-dom';

export const TeacherDashboard = () => {
  const navigate = useNavigate();

  const stats = [
    { icon: Users, label: 'Alunos Ativos', value: '45', change: '+12%', color: 'sky' },
    { icon: BookOpen, label: 'Cursos Criados', value: '8', change: 'Publicados', color: 'indigo' },
    { icon: Eye, label: 'Visualizações', value: '1.2k', change: '+28%', color: 'purple' },
    { icon: Star, label: 'Avaliação Média', value: '4.8', change: 'Excelente', color: 'pink' },
  ];

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-end">
        <div>
          <h1 className="text-3xl font-bold text-gradient mb-2">Painel do Professor</h1>
          <p className="text-slate-600">Gerencie seus cursos e acompanhe seus alunos</p>
        </div>
        <button 
          onClick={() => navigate('/teacher/upload')}
          className="glass-button bg-alpine-500 text-white border-0 hover:bg-alpine-600 flex items-center gap-2"
        >
          <Plus size={20} />
          Nova Aula
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat, idx) => (
          <GlassCard key={idx} delay={idx * 0.1}>
            <div className="flex items-center justify-between mb-4">
              <div className={`w-12 h-12 rounded-xl bg-${stat.color}-100 flex items-center justify-center`}>
                <stat.icon className={`w-6 h-6 text-${stat.color}-600`} />
              </div>
              <span className="text-xs font-medium text-green-600 bg-green-100 px-2 py-1 rounded-full">
                {stat.change}
              </span>
            </div>
            <h3 className="text-2xl font-bold text-slate-800">{stat.value}</h3>
            <p className="text-sm text-slate-500">{stat.label}</p>
          </GlassCard>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 glass-card p-6">
          <h3 className="text-lg font-semibold text-slate-800 mb-4">Desempenho dos Alunos</h3>
          <div className="h-64 flex items-end justify-around">
            {[65, 78, 82, 75, 88, 92, 85, 90].map((height, idx) => (
              <motion.div
                key={idx}
                initial={{ height: 0 }}
                animate={{ height: `${height}%` }}
                transition={{ delay: idx * 0.1, duration: 0.5 }}
                className="w-12 bg-gradient-to-t from-alpine-400 to-alpine-300 rounded-t-lg opacity-80 hover:opacity-100 transition-opacity"
              />
            ))}
          </div>
          <div className="flex justify-between mt-4 text-xs text-slate-500">
            <span>Seg</span><span>Ter</span><span>Qua</span><span>Qui</span><span>Sex</span><span>Sáb</span><span>Dom</span>
          </div>
        </div>

        <div className="space-y-4">
          <GlassCard className="cursor-pointer" onClick={() => navigate('/teacher/upload')}>
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 rounded-xl bg-sky-100 flex items-center justify-center">
                <Plus className="w-6 h-6 text-sky-600" />
              </div>
              <div>
                <h4 className="font-semibold text-slate-800">Enviar Nova Aula</h4>
                <p className="text-sm text-slate-500">Vídeo ou material</p>
              </div>
            </div>
          </GlassCard>

          <GlassCard>
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 rounded-xl bg-indigo-100 flex items-center justify-center">
                <Users className="w-6 h-6 text-indigo-600" />
              </div>
              <div>
                <h4 className="font-semibold text-slate-800">Gerenciar Alunos</h4>
                <p className="text-sm text-slate-500">45 alunos ativos</p>
              </div>
            </div>
          </GlassCard>

          <GlassCard>
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 rounded-xl bg-purple-100 flex items-center justify-center">
                <BarChart2 className="w-6 h-6 text-purple-600" />
              </div>
              <div>
                <h4 className="font-semibold text-slate-800">Relatórios</h4>
                <p className="text-sm text-slate-500">Desempenho da turma</p>
              </div>
            </div>
          </GlassCard>
        </div>
      </div>
    </div>
  );
};