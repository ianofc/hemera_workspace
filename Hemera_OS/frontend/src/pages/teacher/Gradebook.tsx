import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { GlassCard } from '../../components/ui/GlassCard';
import { BookOpen, Users, Calculator, Activity } from 'lucide-react';

interface Atividade {
  id: number;
  titulo: string;
  data: string;
}

interface AlunoNotas {
  aluno_id: number;
  aluno_nome: string;
  matricula: string;
  notas: Record<string, number | null>;
  media: number | null;
}

interface GradebookData {
  turma_ativa: {
    id: number;
    nome: string;
    ano_letivo: number;
  };
  atividades: Atividade[];
  tabela_notas: AlunoNotas[];
}

export const Gradebook = () => {
  const [data, setData] = useState<GradebookData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchGradebook = async () => {
      try {
        const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
        // Buscando gradebook (sem ID pega a 1a turma por padrão do backend)
        const response = await fetch(`${apiUrl}/pedagogico/gradebook/`);
        const result = await response.json();
        if (response.ok) {
          setData(result);
        } else {
          console.error("Erro na API", result);
        }
      } catch (error) {
        console.error("Falha ao se conectar com o Gradebook API:", error);
      } finally {
        setLoading(false);
      }
    };
    fetchGradebook();
  }, []);

  if (loading) {
    return (
      <div className="p-8 flex justify-center items-center h-full">
        <div className="animate-spin text-zeus-primary"><Activity size={40} /></div>
        <p className="ml-4 text-slate-500 font-medium tracking-wide">Compilando matriz de notas do Niocortex...</p>
      </div>
    );
  }

  if (!data || !data.turma_ativa) {
    return <div className="p-8">Ocorreu um erro ao carregar o Diário de Classe.</div>;
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-2 mb-8">
        <h1 className="text-3xl font-bold text-slate-800 flex items-center gap-3">
          <Calculator className="text-zeus-primary" /> Gradebook Matrix
        </h1>
        <p className="text-slate-500">Gestão fluida de notas e comportamentos - {data.turma_ativa.nome}</p>
      </div>

      {/* Tabela Matricial de Notas (Shadcn / Glass Effect) */}
      <GlassCard className="p-0 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="border-b border-slate-200 bg-slate-50/50">
                <th className="p-4 font-semibold text-slate-600">Aluno</th>
                {data.atividades.map((atv) => (
                  <th key={atv.id} className="p-4 font-semibold text-center text-slate-600 border-l border-slate-200 min-w-[120px]">
                    <span className="block text-xs uppercase tracking-wider text-zeus-secondary mb-1">{atv.data}</span>
                    {atv.titulo.length > 15 ? atv.titulo.substring(0, 15) + '...' : atv.titulo}
                  </th>
                ))}
                <th className="p-4 font-bold text-center text-slate-800 border-l border-slate-200 bg-blue-50">
                  Média
                </th>
              </tr>
            </thead>
            <tbody>
              {data.tabela_notas.map((linha, index) => (
                <motion.tr 
                  key={linha.aluno_id}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.05 }}
                  className="border-b border-slate-100 hover:bg-white/40 transition-colors"
                >
                  <td className="p-4">
                    <div className="flex items-center gap-3">
                      <div className="w-8 h-8 rounded-full bg-gradient-to-br from-indigo-100 to-purple-100 flex items-center justify-center text-indigo-700 font-bold text-sm">
                        {linha.aluno_nome.charAt(0)}
                      </div>
                      <div>
                        <div className="font-medium text-slate-700">{linha.aluno_nome}</div>
                        <div className="text-xs text-slate-400">{linha.matricula}</div>
                      </div>
                    </div>
                  </td>
                  
                  {data.atividades.map((atv) => {
                    const nota = linha.notas[atv.id];
                    return (
                      <td key={atv.id} className="p-4 text-center border-l border-slate-100">
                        {nota !== null && nota !== undefined ? (
                          <span className={`px-2 py-1 rounded-md text-sm font-medium ${nota >= 7 ? 'bg-green-100 text-green-700' : nota >= 5 ? 'bg-yellow-100 text-yellow-700' : 'bg-red-100 text-red-700'}`}>
                            {nota.toFixed(1)}
                          </span>
                        ) : (
                          <span className="text-slate-300">-</span>
                        )}
                      </td>
                    );
                  })}
                  
                  <td className="p-4 flex justify-center text-center border-l border-slate-100 bg-blue-50/30">
                    {linha.media !== null ? (
                      <span className={`text-lg font-bold ${linha.media >= 7 ? 'text-green-600' : linha.media >= 5 ? 'text-yellow-600' : 'text-red-500'}`}>
                        {linha.media.toFixed(1)}
                      </span>
                    ) : (
                      <span className="text-slate-400">-</span>
                    )}
                  </td>
                </motion.tr>
              ))}
            </tbody>
          </table>
        </div>
      </GlassCard>
    </div>
  );
};
