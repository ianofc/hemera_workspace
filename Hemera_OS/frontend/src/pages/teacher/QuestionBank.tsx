import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { GlassCard } from '../../components/ui/GlassCard';
import { Database, Search, Filter, Plus, FileText, CheckCircle, X, Sparkles, Loader2 } from 'lucide-react';

export const QuestionBank = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isGenerating, setIsGenerating] = useState(false);
  
  // Lista unificada misturando Mock velho com Geração I.A. Nova
  const [questoes, setQuestoes] = useState<any[]>([
    { id: 1, tema: 'Genética', nivel: 'Ensino Médio', tipo: 'Múltipla Escolha', bncc: 'EM13CNT301', adicionado: '2025-11-20', conteudo: '...' },
  ]);

  // Form states
  const [formTema, setFormTema] = useState('');
  const [formNivel, setFormNivel] = useState('Ensino Médio');
  const [formQtd, setFormQtd] = useState(3);
  const [formTipo, setFormTipo] = useState('multipla_escolha');

  const handleGenerateAI = async () => {
    if (!formTema) return alert("Passe o tema para o PentaIA.");
    setIsGenerating(true);
    
    try {
      const response = await fetch(`http://localhost:8001/v1/education/exam`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          tema: formTema,
          nivel: formNivel,
          qtd_questoes: formQtd,
          tipo_questoes: [formTipo],
          dificuldade: "medio",
          contexto_bncc: true
        })
      });
      
      const result = await response.json();
      
      if (response.ok) {
        // Pega a string gerada e insere no banco local da view (depois salvaremos no Django)
        const novaFornada = {
          id: Date.now(),
          tema: formTema,
          nivel: formNivel,
          tipo: formTipo.replace('_', ' ').toUpperCase(),
          bncc: 'GERADO POR IA',
          adicionado: new Date().toLocaleDateString(),
          html_conteudo: result.conteudo,
          gabarito: result.gabarito
        };
        setQuestoes([novaFornada, ...questoes]);
        setIsModalOpen(false);
      } else {
        alert("Erro no córtex da IA: " + JSON.stringify(result));
      }
    } catch(err) {
      console.error(err);
      alert("O Cérebro PentaIA (FastAPI) na porta 8001 parece estar offline.");
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* HEADER */}
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold text-slate-800 flex items-center gap-3">
            <Database className="text-zeus-primary" size={32} /> Banco de Questões
          </h1>
          <p className="text-slate-500">Repositório histórico e de I.A. para montagem de provas.</p>
        </div>
        
        <button 
          onClick={() => setIsModalOpen(true)}
          className="glass-button bg-zeus-primary/10 text-zeus-primary border border-zeus-primary/30 flex items-center gap-2 px-4 py-2 hover:bg-zeus-primary/20 transition-all font-semibold rounded-xl"
        >
          <Sparkles size={20} /> Nova Questão (I.A.)
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="md:col-span-1">
          <GlassCard className="p-4 space-y-4 stick top-6">
            <h3 className="font-semibold text-slate-700 flex items-center gap-2"><Filter size={18}/> Filtros</h3>
            {/* Same filters as mock */}
            <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={16} />
              <input type="text" placeholder="Buscar..." className="w-full pl-9 pr-4 py-2 rounded-xl border border-slate-200" />
            </div>
          </GlassCard>
        </div>

        <div className="md:col-span-3 space-y-4">
          {questoes.map((q, i) => (
            <motion.div
              initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.1 }}
              key={q.id}
            >
              <GlassCard className="p-4 hover:shadow-md transition-shadow">
                <div className="flex justify-between items-start">
                  <div className="flex items-start gap-4">
                    <div className="p-3 bg-blue-50 text-blue-600 rounded-xl"><FileText size={24} /></div>
                    <div>
                      <h4 className="text-lg font-bold text-slate-800">{q.tema}</h4>
                      <div className="flex flex-wrap gap-2 mt-2">
                        <span className="px-2 py-1 bg-slate-100 text-slate-600 text-xs rounded font-medium border border-slate-200">{q.nivel}</span>
                        <span className="px-2 py-1 bg-alpine-50 text-alpine-600 text-xs rounded font-medium border border-alpine-200">{q.tipo}</span>
                        <span className="px-2 py-1 bg-purple-50 text-purple-600 text-xs rounded font-medium border border-purple-200 flex items-center gap-1"><CheckCircle size={12} /> {q.bncc}</span>
                      </div>
                      
                      {q.html_conteudo && (
                        <div className="mt-4 p-4 bg-slate-50 border border-slate-200 rounded-lg text-sm max-h-64 overflow-y-auto">
                           <div dangerouslySetInnerHTML={{ __html: q.html_conteudo }} />
                           <div className="mt-4 pt-2 border-t border-slate-200 font-bold text-green-700">Gabarito: {q.gabarito}</div>
                        </div>
                      )}
                    </div>
                  </div>
                  <div className="text-xs text-slate-400">Criado em {q.adicionado}</div>
                </div>
              </GlassCard>
            </motion.div>
          ))}
        </div>
      </div>

      {/* MODAL DE GERAÇÃO IA */}
      <AnimatePresence>
        {isModalOpen && (
          <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/40 backdrop-blur-sm">
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.95 }}
              className="bg-white rounded-2xl shadow-xl w-full max-w-lg overflow-hidden border border-slate-200"
            >
              <div className="p-4 border-b border-slate-100 flex justify-between items-center bg-gradient-to-r from-indigo-50 to-purple-50">
                <h3 className="text-lg font-bold text-slate-800 flex items-center gap-2">
                  <Sparkles className="text-purple-600" size={20} /> Forja de Questões PentaIA
                </h3>
                <button onClick={() => setIsModalOpen(false)} className="text-slate-400 hover:text-slate-600"><X size={20}/></button>
              </div>
              
              <div className="p-6 space-y-4">
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">Tema da Aula</label>
                  <input type="text" value={formTema} onChange={e => setFormTema(e.target.value)} placeholder="Ex: Fotossíntese..." className="w-full px-4 py-2 rounded-xl border border-slate-300 focus:outline-none focus:ring-2 focus:ring-purple-500" />
                </div>
                
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-slate-700 mb-1">Nível de Ensino</label>
                    <select value={formNivel} onChange={e => setFormNivel(e.target.value)} className="w-full px-4 py-2 rounded-xl border border-slate-300">
                      <option>Ensino Médio (1º a 3º)</option>
                      <option>Ensino Fundamental II (6º a 9º)</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-slate-700 mb-1">Quantidade</label>
                    <input type="number" min="1" max="10" value={formQtd} onChange={e => setFormQtd(Number(e.target.value))} className="w-full px-4 py-2 rounded-xl border border-slate-300" />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">Formato</label>
                  <select value={formTipo} onChange={e => setFormTipo(e.target.value)} className="w-full px-4 py-2 rounded-xl border border-slate-300">
                    <option value="multipla_escolha">Múltipla Escolha (A, B, C, D)</option>
                    <option value="discursiva">Discursiva / Aberta</option>
                  </select>
                </div>
              </div>
              
              <div className="p-4 border-t border-slate-100 bg-slate-50 flex justify-end gap-3">
                <button onClick={() => setIsModalOpen(false)} className="px-4 py-2 text-slate-600 font-medium hover:bg-slate-200 rounded-lg transition-colors">Cancelar</button>
                <button 
                  onClick={handleGenerateAI}
                  disabled={isGenerating}
                  className="px-6 py-2 bg-gradient-to-r from-purple-600 to-indigo-600 text-white font-bold rounded-lg shadow-md hover:shadow-lg transition-all flex items-center gap-2 disabled:opacity-50"
                >
                  {isGenerating ? <><Loader2 className="animate-spin" size={18}/> Processando (AI)...</> : <><Sparkles size={18}/> Invocar Questões</>}
                </button>
              </div>
            </motion.div>
          </div>
        )}
      </AnimatePresence>
    </div>
  );
};
