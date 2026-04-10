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

  const fetchGradebook = async () => {
    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
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

  useEffect(() => {
    fetchGradebook();
  }, []);

  const handleNotaChange = async (alunoId: number, atividadeId: number, value: string) => {
    const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
    try {
      await fetch(`${apiUrl}/pedagogico/gradebook/update/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ aluno_id: alunoId, atividade_id: atividadeId, valor: value })
      });
      // Recarrega pro DB calcular a média nova
      fetchGradebook();
    } catch(err) {
      console.error(err);
    }
  };

  const handleAddAtividade = async () => {
    const titulo = prompt("Nome da Nova Avaliação/Atividade:");
    if (!titulo) return;
    
    const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
    try {
      if (!data) return;
      await fetch(`${apiUrl}/pedagogico/gradebook/add-activity/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ turma_id: data.turma_ativa.id, titulo })
      });
      fetchGradebook();
    } catch(err) {
      console.error(err);
    }
  };

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
      <div className="flex flex-col gap-2 mb-8 relative">
        <h1 className="text-3xl font-bold text-slate-800 flex items-center gap-3">
          <Calculator className="text-zeus-primary" /> Diário de Classe
        </h1>
        <p className="text-slate-500">Pressione TAB ou ENTER após digitar a nota para salvar - {data.turma_ativa.nome}</p>
        
        <button 
          onClick={handleAddAtividade}
          className="absolute right-0 top-0 glass-button text-xs bg-zeus-primary/10 border-zeus-primary/40 text-zeus-primary flex items-center gap-2 p-2 px-4 shadow-sm"
        >
          <Activity size={16} /> Nova Coluna de Nota
        </button>
      </div>

      <GlassCard className="p-0 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse min-w-[800px]">
            <thead>
              <tr className="border-b border-slate-200 bg-slate-50/50">
                <th className="p-4 font-semibold text-slate-600 sticky left-0 bg-white/90 glass z-10 w-64">Aluno</th>
                {data.atividades.map((atv) => (
                  <th key={atv.id} className="p-4 font-semibold text-center text-slate-600 border-l border-slate-200 min-w-[120px]">
                    <span className="block text-[10px] uppercase tracking-wider text-zeus-secondary mb-1">{atv.data}</span>
                    <div className="truncate text-xs" title={atv.titulo}>{atv.titulo}</div>
                  </th>
                ))}
                <th className="p-4 font-bold text-center text-slate-800 border-l border-slate-200 bg-blue-50">
                  Média Final
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
                  className="border-b border-slate-100 hover:bg-slate-50/50 transition-colors"
                >
                  <td className="p-4 sticky left-0 bg-white/90 z-10">
                    <div className="flex items-center gap-3">
                      <div className="w-8 h-8 rounded-full bg-gradient-to-br from-indigo-100 to-purple-100 flex items-center justify-center text-indigo-700 font-bold text-xs">
                        {linha.aluno_nome.charAt(0)}
                      </div>
                      <div className="flex flex-col">
                        <span className="font-medium text-sm text-slate-700 truncate w-48" title={linha.aluno_nome}>{linha.aluno_nome}</span>
                        <span className="text-[10px] text-slate-400">{linha.matricula}</span>
                      </div>
                    </div>
                  </td>
                  
                  {data.atividades.map((atv) => {
                    const nota = linha.notas[atv.id];
                    return (
                      <td key={atv.id} className="p-2 text-center border-l border-slate-100">
                        <input
                          type="number"
                          step="0.1"
                          min="0"
                          max="10"
                          defaultValue={nota !== null ? nota : ""}
                          onBlur={(e) => {
                            if(e.target.value !== String(nota)) {
                              handleNotaChange(linha.aluno_id, atv.id, e.target.value);
                            }
                          }}
                          onKeyDown={(e) => {
                            if(e.key === 'Enter') e.currentTarget.blur();
                          }}
                          className={`w-16 p-1 text-center font-semibold rounded outline-none ring-1 ring-transparent focus:ring-zeus-primary/50 transition-all ${nota && nota >= 6 ? 'bg-green-50 text-green-700 font-bold' : nota && nota < 6 ? 'bg-red-50 text-red-600 font-bold' : 'bg-slate-50 text-slate-400'}`}
                        />
                      </td>
                    );
                  })}
                  
                  <td className="p-4 flex justify-center text-center border-l border-slate-100 bg-blue-50/20 items-center h-full">
                    {linha.media !== null ? (
                      <span className={`text-md font-bold px-3 py-1 rounded-lg ${linha.media >= 6 ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-600'}`}>
                        {linha.media.toFixed(1)}
                      </span>
                    ) : (
                      <span className="text-slate-300">-</span>
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
