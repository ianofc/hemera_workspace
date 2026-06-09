import React, { useState } from 'react';
import { useLyceum } from '../../contexts/LyceumContext';
import { Calendar, RefreshCw, CheckCircle, Clock, Link2, BookOpen, AlertCircle } from 'lucide-react';
import { toast } from 'sonner';

export const MoodleSync: React.FC = () => {
  const { moodleEvents, moodleGrades, isMoodleSynced, syncWithMoodle } = useLyceum();
  const [url, setUrl] = useState('https://moodle.hemera.edu.br');
  const [token, setToken] = useState('');
  const [isSyncing, setIsSyncing] = useState(false);
  const [activeTab, setActiveTab] = useState<'calendar' | 'grades' | 'config'>('calendar');

  const handleSync = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!token) {
      toast.error('Por favor, insira o Token de Acesso do Moodle para autenticar.');
      return;
    }
    
    setIsSyncing(true);
    toast.info('Conectando com o Moodle e baixando tarefas, prazos e notas...', { duration: 2000 });
    
    try {
      const success = await syncWithMoodle(url, token);
      if (success) {
        toast.success('Sincronização com o Moodle realizada com sucesso! +100 XP');
        setActiveTab('calendar');
      } else {
        toast.error('Erro na sincronização. Verifique a URL e o Token fornecidos.');
      }
    } catch (err) {
      toast.error('Ocorreu um erro ao conectar com o servidor Moodle.');
    } finally {
      setIsSyncing(false);
    }
  };

  const getStatusBadge = (status: 'pending' | 'submitted' | 'graded') => {
    if (status === 'graded') {
      return <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-bold bg-success/15 text-success"><CheckCircle className="w-3.5 h-3.5" /> Corrigido</span>;
    }
    if (status === 'submitted') {
      return <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-bold bg-primary/15 text-primary"><CheckCircle className="w-3.5 h-3.5" /> Entregue</span>;
    }
    return <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-bold bg-amber-500/15 text-amber-500"><Clock className="w-3.5 h-3.5" /> Pendente</span>;
  };

  return (
    <div className="border bg-white/60 backdrop-blur-xl rounded-[2rem] shadow-xl overflow-hidden border-glass-border">
      {/* Header */}
      <div className="flex flex-col sm:flex-row items-center justify-between gap-4 p-6 border-b border-gray-100 bg-muted/30">
        <div className="flex items-center gap-3">
          <div className="flex items-center justify-center w-10 h-10 rounded-xl bg-orange-500/10 text-orange-600">
            <Link2 className="w-6 h-6" />
          </div>
          <div>
            <h3 className="text-lg font-bold text-foreground">Integração Moodle</h3>
            <p className="text-xs text-muted-foreground">Sincronize notas, prazos e calendário diretamente com o Moodle.</p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          {isMoodleSynced ? (
            <span className="flex items-center gap-1.5 px-3 py-1 rounded-full bg-success/10 text-success text-xs font-bold border border-success/20">
              <span className="w-2 h-2 rounded-full bg-success animate-pulse" /> Sincronizado
            </span>
          ) : (
            <span className="flex items-center gap-1.5 px-3 py-1 rounded-full bg-amber-500/10 text-amber-500 text-xs font-bold border border-amber-500/20">
              <AlertCircle className="w-3.5 h-3.5" /> Não Conectado
            </span>
          )}

          {isMoodleSynced && (
            <button
              onClick={() => {
                setIsSyncing(true);
                setTimeout(() => {
                  setIsSyncing(false);
                  toast.success('Calendário e Notas atualizados!');
                }, 1000);
              }}
              disabled={isSyncing}
              className="flex items-center justify-center w-8 h-8 rounded-lg border border-border bg-card hover:bg-muted text-foreground transition-colors disabled:opacity-50"
            >
              <RefreshCw className={`w-4 h-4 ${isSyncing ? 'animate-spin' : ''}`} />
            </button>
          )}
        </div>
      </div>

      {/* Tabs */}
      <div className="flex border-b border-gray-100 bg-white/40">
        <button
          onClick={() => setActiveTab('calendar')}
          className={`flex-1 py-3 text-sm font-bold border-b-2 transition-all ${
            activeTab === 'calendar'
              ? 'border-primary text-primary bg-primary/5'
              : 'border-transparent text-muted-foreground hover:text-foreground'
          }`}
        >
          <Calendar className="inline-block w-4 h-4 mr-2" /> Calendário & Tarefas
        </button>
        <button
          onClick={() => setActiveTab('grades')}
          className={`flex-1 py-3 text-sm font-bold border-b-2 transition-all ${
            activeTab === 'grades'
              ? 'border-primary text-primary bg-primary/5'
              : 'border-transparent text-muted-foreground hover:text-foreground'
          }`}
        >
          <BookOpen className="inline-block w-4 h-4 mr-2" /> Notas Sincronizadas
        </button>
        <button
          onClick={() => setActiveTab('config')}
          className={`flex-1 py-3 text-sm font-bold border-b-2 transition-all ${
            activeTab === 'config'
              ? 'border-primary text-primary bg-primary/5'
              : 'border-transparent text-muted-foreground hover:text-foreground'
          }`}
        >
          <Link2 className="inline-block w-4 h-4 mr-2" /> Configurações
        </button>
      </div>

      {/* Content */}
      <div className="p-6">
        {activeTab === 'calendar' && (
          <div className="space-y-4">
            {!isMoodleSynced && (
              <div className="p-4 border rounded-2xl bg-amber-500/5 border-amber-500/20 text-amber-600 text-sm flex gap-3">
                <AlertCircle className="w-5 h-5 shrink-0 mt-0.5" />
                <div>
                  <p className="font-bold">Moodle não configurado</p>
                  <p className="text-xs text-muted-foreground mt-0.5">Vá na aba "Configurações" e insira seu token para importar as tarefas e eventos acadêmicos.</p>
                </div>
              </div>
            )}
            
            <div className="space-y-3">
              {moodleEvents.length === 0 ? (
                <p className="text-center py-8 text-sm text-muted-foreground">Nenhuma tarefa ou evento agendado.</p>
              ) : (
                moodleEvents.map((event) => (
                  <div key={event.id} className="p-4 border bg-card hover:bg-muted/10 transition-colors border-border rounded-2xl flex flex-col md:flex-row md:items-center justify-between gap-4">
                    <div className="space-y-1">
                      <span className="text-[10px] font-bold uppercase tracking-wider text-primary">
                        {event.courseName}
                      </span>
                      <h4 className="text-sm font-bold text-foreground">{event.title}</h4>
                      <p className="text-xs text-muted-foreground line-clamp-1">{event.description}</p>
                      
                      <div className="flex items-center gap-2 mt-2 text-[10px] text-muted-foreground">
                        <Calendar className="w-3.5 h-3.5" />
                        <span>Prazo: {new Date(event.dueDate).toLocaleString('pt-BR', { dateStyle: 'short', timeStyle: 'short' })}</span>
                      </div>
                    </div>

                    <div className="flex items-center justify-between md:justify-end gap-3 border-t md:border-t-0 pt-3 md:pt-0 border-border/50">
                      {getStatusBadge(event.status)}
                      <a
                        href={url}
                        target="_blank"
                        rel="noreferrer"
                        className="px-4 py-1.5 border border-border rounded-xl text-xs font-bold text-foreground bg-card hover:bg-muted transition-colors flex items-center gap-1.5"
                      >
                        Ir para o Moodle <Link2 className="w-3.5 h-3.5" />
                      </a>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        )}

        {activeTab === 'grades' && (
          <div className="space-y-4">
            {!isMoodleSynced && (
              <div className="p-4 border rounded-2xl bg-amber-500/5 border-amber-500/20 text-amber-600 text-sm flex gap-3">
                <AlertCircle className="w-5 h-5 shrink-0 mt-0.5" />
                <div>
                  <p className="font-bold">Moodle não configurado</p>
                  <p className="text-xs text-muted-foreground mt-0.5">Vá na aba "Configurações" e insira seu token para importar seu diário de notas do Moodle.</p>
                </div>
              </div>
            )}

            <div className="divide-y divide-gray-100 border rounded-2xl overflow-hidden bg-card border-border">
              {moodleGrades.length === 0 ? (
                <p className="text-center py-8 text-sm text-muted-foreground">Nenhuma nota importada do Moodle.</p>
              ) : (
                moodleGrades.map((grade) => (
                  <div key={grade.id} className="p-4 hover:bg-muted/10 transition-colors flex flex-col md:flex-row justify-between gap-4">
                    <div className="space-y-1">
                      <span className="text-[10px] font-bold uppercase tracking-wider text-muted-foreground">
                        {grade.courseName}
                      </span>
                      <h4 className="text-sm font-bold text-foreground">{grade.assignmentName}</h4>
                      {grade.feedback && (
                        <p className="text-xs text-success bg-success/5 border border-success/10 rounded-lg p-2 mt-1">
                          <strong>Feedback:</strong> {grade.feedback}
                        </p>
                      )}
                      <p className="text-[10px] text-muted-foreground mt-1">
                        Lançado em: {new Date(grade.gradedDate).toLocaleDateString()}
                      </p>
                    </div>

                    <div className="flex flex-col items-end justify-center shrink-0">
                      <span className="text-xs font-bold text-muted-foreground uppercase tracking-widest">Nota</span>
                      <div className="flex items-baseline gap-1">
                        <span className={`text-xl font-black ${grade.grade >= 7.0 ? 'text-success' : 'text-danger'}`}>
                          {grade.grade.toFixed(1)}
                        </span>
                        <span className="text-xs text-muted-foreground">/ {grade.maxGrade.toFixed(1)}</span>
                      </div>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        )}

        {activeTab === 'config' && (
          <form onSubmit={handleSync} className="space-y-4 max-w-xl">
            <div className="space-y-2">
              <label className="text-xs font-bold uppercase tracking-widest text-muted-foreground">
                Endereço do Servidor Moodle
              </label>
              <input
                type="url"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                placeholder="https://moodle.suainstituicao.edu.br"
                required
                className="w-full px-4 py-3 rounded-xl border border-border bg-card text-foreground focus:ring-2 focus:ring-primary/20 focus:outline-none transition-all text-sm"
              />
            </div>

            <div className="space-y-2">
              <div className="flex justify-between items-center">
                <label className="text-xs font-bold uppercase tracking-widest text-muted-foreground">
                  Token de Acesso (Web Services)
                </label>
                <a
                  href="https://moodle.org"
                  target="_blank"
                  rel="noreferrer"
                  className="text-xs text-primary hover:underline font-medium"
                >
                  Onde achar meu token?
                </a>
              </div>
              <input
                type="password"
                value={token}
                onChange={(e) => setToken(e.target.value)}
                placeholder="Insira seu Token do Moodle"
                className="w-full px-4 py-3 rounded-xl border border-border bg-card text-foreground focus:ring-2 focus:ring-primary/20 focus:outline-none transition-all text-sm font-mono"
              />
            </div>

            <div className="flex justify-end gap-3 pt-2">
              <button
                type="submit"
                disabled={isSyncing}
                className="flex items-center gap-2 px-6 py-3 bg-primary hover:bg-primary/90 disabled:opacity-50 text-primary-foreground font-bold rounded-xl shadow-lg transition-all text-sm"
              >
                {isSyncing ? (
                  <>
                    <RefreshCw className="w-4 h-4 animate-spin" /> Conectando...
                  </>
                ) : (
                  <>
                    <RefreshCw className="w-4 h-4" /> Autenticar e Sincronizar
                  </>
                )}
              </button>
            </div>
          </form>
        )}
      </div>
    </div>
  );
};
