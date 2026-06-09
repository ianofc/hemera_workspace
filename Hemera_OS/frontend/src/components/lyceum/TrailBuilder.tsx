import React, { useState } from 'react';
import { useLyceum, CourseTrail, Module, Lesson, QuizQuestion } from '../../contexts/LyceumContext';
import { Plus, Trash2, Save, FileText, PlayCircle, CheckCircle2, ChevronRight, Edit3, ArrowLeft } from 'lucide-react';
import { toast } from 'sonner';

export const TrailBuilder: React.FC = () => {
  const { trails, updateTrail } = useLyceum();
  const [selectedCourseId, setSelectedCourseId] = useState<number | null>(trails[0]?.id || null);
  
  // Estado de módulos carregados para edição
  const activeCourse = trails.find(t => t.id === selectedCourseId);
  const [modules, setModules] = useState<Module[]>([]);

  // Carrega os módulos do curso ativo quando mudado
  React.useEffect(() => {
    if (activeCourse) {
      setModules(activeCourse.modules);
    } else {
      setModules([]);
    }
  }, [selectedCourseId, activeCourse]);

  // Edição de Módulos
  const [newModuleTitle, setNewModuleTitle] = useState('');
  
  // Criação de Lição
  const [selectedModuleId, setSelectedModuleId] = useState<number | null>(null);
  const [lessonTitle, setLessonTitle] = useState('');
  const [lessonType, setLessonType] = useState<'VIDEO' | 'TEXTO' | 'EXERCICIO'>('TEXTO');
  const [lessonContent, setLessonContent] = useState('');
  const [lessonXp, setLessonXp] = useState(50);
  const [videoUrl, setVideoUrl] = useState('');
  
  // Criação de Quiz
  const [quizQuestions, setQuizQuestions] = useState<QuizQuestion[]>([]);
  const [questionText, setQuestionText] = useState('');
  const [options, setOptions] = useState<string[]>(['', '', '', '']);
  const [correctOptionIdx, setCorrectOptionIdx] = useState<number>(0);

  const handleAddModule = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newModuleTitle.trim()) return;

    const newModule: Module = {
      id: Date.now(),
      title: newModuleTitle,
      lessons: []
    };

    setModules(prev => [...prev, newModule]);
    setNewModuleTitle('');
    toast.success('Módulo adicionado! Não se esqueça de salvar as alterações.');
  };

  const handleRemoveModule = (moduleId: number) => {
    setModules(prev => prev.filter(m => m.id !== moduleId));
    toast.success('Módulo removido da lista temporária.');
  };

  const handleAddQuizQuestion = () => {
    if (!questionText.trim()) {
      toast.error('Preencha a pergunta do quiz.');
      return;
    }
    if (options.some(opt => !opt.trim())) {
      toast.error('Preencha todas as 4 alternativas.');
      return;
    }

    const newQuestion: QuizQuestion = {
      id: Date.now(),
      question: questionText,
      options: [...options],
      correctOptionIndex: correctOptionIdx
    };

    setQuizQuestions(prev => [...prev, newQuestion]);
    setQuestionText('');
    setOptions(['', '', '', '']);
    setCorrectOptionIdx(0);
    toast.success('Questão adicionada ao quiz!');
  };

  const handleAddLesson = (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedModuleId) {
      toast.error('Selecione um módulo para adicionar a lição.');
      return;
    }
    if (!lessonTitle.trim()) {
      toast.error('Digite o título da lição.');
      return;
    }

    if (lessonType === 'EXERCICIO' && quizQuestions.length === 0) {
      toast.error('Adicione pelo menos uma pergunta para o Quiz.');
      return;
    }

    const newLesson: Lesson = {
      id: Date.now(),
      title: lessonTitle,
      type: lessonType,
      completed: false,
      xpReward: lessonXp,
      content: lessonContent,
      videoUrl: lessonType === 'VIDEO' ? videoUrl : undefined,
      quiz: lessonType === 'EXERCICIO' ? [...quizQuestions] : undefined
    };

    setModules(prev => prev.map(m => {
      if (m.id === selectedModuleId) {
        return {
          ...m,
          lessons: [...m.lessons, newLesson]
        };
      }
      return m;
    }));

    // Reseta form de lição
    setLessonTitle('');
    setLessonContent('');
    setLessonXp(50);
    setVideoUrl('');
    setQuizQuestions([]);
    setSelectedModuleId(null);
    toast.success('Lição adicionada ao módulo com sucesso!');
  };

  const handleRemoveLesson = (moduleId: number, lessonId: number) => {
    setModules(prev => prev.map(m => {
      if (m.id === moduleId) {
        return {
          ...m,
          lessons: m.lessons.filter(l => l.id !== lessonId)
        };
      }
      return m;
    }));
    toast.success('Lição removida.');
  };

  const handleSaveTrail = () => {
    if (!selectedCourseId) return;
    updateTrail(selectedCourseId, modules);
    toast.success('Trilha de Aprendizagem salva e publicada com sucesso!');
  };

  return (
    <div className="space-y-8">
      {/* Seleção do Curso */}
      <div className="flex flex-col sm:flex-row items-center justify-between gap-4 p-6 border bg-white/60 backdrop-blur-xl rounded-[2rem] shadow-xl border-glass-border">
        <div>
          <h3 className="text-lg font-bold text-foreground">Construtor de Trilhas (Lyceum Builder)</h3>
          <p className="text-xs text-muted-foreground">Adicione módulos, lições e desafios interativos aos seus cursos.</p>
        </div>

        <div className="flex items-center gap-3">
          <select
            value={selectedCourseId || ''}
            onChange={(e) => setSelectedCourseId(Number(e.target.value))}
            className="px-4 py-2.5 rounded-xl border border-border bg-card text-foreground focus:ring-2 focus:ring-primary/20 text-sm font-bold"
          >
            {trails.map(t => (
              <option key={t.id} value={t.id}>{t.title}</option>
            ))}
          </select>

          <button
            onClick={handleSaveTrail}
            className="flex items-center gap-2 px-6 py-2.5 bg-success text-white hover:bg-success/95 font-bold rounded-xl shadow-lg transition-all text-sm shrink-0"
          >
            <Save className="w-4 h-4" /> Salvar Trilha
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Visualizador da Estrutura Atual */}
        <div className="lg:col-span-2 space-y-6">
          <div className="p-6 border bg-white/60 backdrop-blur-xl rounded-[2rem] shadow-xl border-glass-border">
            <h4 className="text-base font-bold text-foreground mb-4">Estrutura do Curso: {activeCourse?.title}</h4>
            
            {modules.length === 0 ? (
              <p className="text-sm text-muted-foreground py-8 text-center bg-card rounded-2xl border border-dashed">
                Nenhum módulo cadastrado. Adicione um novo módulo para começar.
              </p>
            ) : (
              <div className="space-y-4">
                {modules.map((modulo, mIdx) => (
                  <div key={modulo.id} className="p-4 border bg-card border-border rounded-2xl space-y-3">
                    <div className="flex items-center justify-between">
                      <h5 className="text-sm font-bold text-foreground">
                        Módulo {mIdx + 1}: {modulo.title}
                      </h5>
                      <div className="flex items-center gap-2">
                        <button
                          onClick={() => setSelectedModuleId(modulo.id)}
                          className="flex items-center gap-1.5 px-3 py-1 border border-primary/20 bg-primary/5 hover:bg-primary/10 text-primary rounded-lg text-xs font-bold transition-all"
                        >
                          <Plus className="w-3.5 h-3.5" /> Lição
                        </button>
                        <button
                          onClick={() => handleRemoveModule(modulo.id)}
                          className="p-1 hover:text-danger text-muted-foreground transition-colors"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </div>
                    </div>

                    {/* Lições deste módulo */}
                    <div className="space-y-2 pl-4 border-l-2 border-border/60">
                      {modulo.lessons.length === 0 ? (
                        <p className="text-xs text-muted-foreground py-2">Nenhuma lição adicionada.</p>
                      ) : (
                        modulo.lessons.map((les) => (
                          <div key={les.id} className="flex items-center justify-between p-2.5 bg-muted/30 border border-border rounded-xl">
                            <div className="flex items-center gap-2">
                              {les.type === 'VIDEO' && <PlayCircle className="w-4 h-4 text-primary" />}
                              {les.type === 'TEXTO' && <FileText className="w-4 h-4 text-secondary" />}
                              {les.type === 'EXERCICIO' && <CheckCircle2 className="w-4 h-4 text-success" />}
                              <div>
                                <span className="text-xs font-bold text-foreground">{les.title}</span>
                                <span className="text-[9px] uppercase ml-2 text-muted-foreground font-bold tracking-wider">
                                  {les.type} (+{les.xpReward} XP)
                                </span>
                              </div>
                            </div>
                            <button
                              onClick={() => handleRemoveLesson(modulo.id, les.id)}
                              className="p-1 hover:text-danger text-muted-foreground transition-colors"
                            >
                              <Trash2 className="w-3.5 h-3.5" />
                            </button>
                          </div>
                        ))
                      )}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Adicionar Módulo */}
          <form onSubmit={handleAddModule} className="p-6 border bg-white/60 backdrop-blur-xl rounded-[2rem] shadow-xl border-glass-border">
            <h4 className="text-base font-bold text-foreground mb-4">Adicionar Módulo</h4>
            <div className="flex gap-3">
              <input
                type="text"
                value={newModuleTitle}
                onChange={(e) => setNewModuleTitle(e.target.value)}
                placeholder="Ex: Módulo 3 — Aplicações Práticas das Derivadas"
                className="flex-1 px-4 py-2.5 rounded-xl border border-border bg-card text-foreground focus:ring-2 focus:ring-primary/20 text-sm focus:outline-none"
              />
              <button
                type="submit"
                className="px-6 py-2.5 bg-primary text-primary-foreground font-bold rounded-xl shadow-lg hover:bg-primary/95 text-sm shrink-0"
              >
                + Módulo
              </button>
            </div>
          </form>
        </div>

        {/* Form de Lição (se módulo selecionado) */}
        <div>
          {selectedModuleId ? (
            <div className="p-6 border bg-white/60 backdrop-blur-xl rounded-[2rem] shadow-xl border-glass-border space-y-4">
              <div className="flex justify-between items-center pb-2 border-b border-border">
                <h4 className="text-sm font-bold text-foreground">Nova Lição</h4>
                <button
                  onClick={() => setSelectedModuleId(null)}
                  className="text-xs text-muted-foreground hover:text-foreground flex items-center gap-1"
                >
                  <ArrowLeft className="w-3 h-3" /> Cancelar
                </button>
              </div>

              <form onSubmit={handleAddLesson} className="space-y-4 text-xs font-semibold">
                <div className="space-y-1">
                  <label className="text-muted-foreground uppercase tracking-widest text-[9px]">Título da Lição</label>
                  <input
                    type="text"
                    value={lessonTitle}
                    onChange={(e) => setLessonTitle(e.target.value)}
                    placeholder="Ex: Regra da Cadeia"
                    className="w-full px-3 py-2 rounded-lg border border-border bg-card text-foreground text-xs font-medium focus:outline-none"
                  />
                </div>

                <div className="space-y-1">
                  <label className="text-muted-foreground uppercase tracking-widest text-[9px]">Tipo de Aula</label>
                  <select
                    value={lessonType}
                    onChange={(e) => setLessonType(e.target.value as any)}
                    className="w-full px-3 py-2 rounded-lg border border-border bg-card text-foreground text-xs font-bold focus:outline-none"
                  >
                    <option value="TEXTO">Material Escrito (Texto)</option>
                    <option value="VIDEO">Vídeo Aula</option>
                    <option value="EXERCICIO">Quiz Interativo (Exercício)</option>
                  </select>
                </div>

                <div className="space-y-1">
                  <label className="text-muted-foreground uppercase tracking-widest text-[9px]">XP de Recompensa</label>
                  <input
                    type="number"
                    value={lessonXp}
                    onChange={(e) => setLessonXp(Number(e.target.value))}
                    min={10}
                    max={500}
                    className="w-full px-3 py-2 rounded-lg border border-border bg-card text-foreground text-xs font-medium focus:outline-none"
                  />
                </div>

                {lessonType === 'VIDEO' && (
                  <div className="space-y-1">
                    <label className="text-muted-foreground uppercase tracking-widest text-[9px]">URL do Vídeo (Embed)</label>
                    <input
                      type="url"
                      value={videoUrl}
                      onChange={(e) => setVideoUrl(e.target.value)}
                      placeholder="Ex: https://www.youtube.com/embed/..."
                      className="w-full px-3 py-2 rounded-lg border border-border bg-card text-foreground text-xs font-medium focus:outline-none"
                    />
                  </div>
                )}

                <div className="space-y-1">
                  <label className="text-muted-foreground uppercase tracking-widest text-[9px]">
                    {lessonType === 'EXERCICIO' ? 'Instruções do Quiz' : 'Conteúdo / Resumo'}
                  </label>
                  <textarea
                    rows={4}
                    value={lessonContent}
                    onChange={(e) => setLessonContent(e.target.value)}
                    placeholder="Escreva as explicações teóricas da aula aqui..."
                    className="w-full px-3 py-2 rounded-lg border border-border bg-card text-foreground text-xs font-medium focus:outline-none"
                  />
                </div>

                {/* Seção Quiz */}
                {lessonType === 'EXERCICIO' && (
                  <div className="p-3 border bg-muted/20 border-border rounded-xl space-y-3">
                    <h5 className="text-[10px] font-bold text-foreground uppercase tracking-wider">Perguntas do Quiz ({quizQuestions.length})</h5>
                    
                    {quizQuestions.map((q, idx) => (
                      <div key={q.id} className="text-[10px] p-2 border bg-card border-border rounded-lg flex items-center justify-between">
                        <span className="truncate max-w-[150px]">{idx + 1}. {q.question}</span>
                        <button
                          type="button"
                          onClick={() => setQuizQuestions(prev => prev.filter(item => item.id !== q.id))}
                          className="text-danger hover:underline"
                        >
                          Remover
                        </button>
                      </div>
                    ))}

                    <div className="space-y-2 border-t pt-2 border-border/60">
                      <input
                        type="text"
                        value={questionText}
                        onChange={(e) => setQuestionText(e.target.value)}
                        placeholder="Escreva a pergunta..."
                        className="w-full px-2 py-1.5 rounded border border-border bg-card text-xs font-medium focus:outline-none"
                      />

                      <div className="grid grid-cols-2 gap-2">
                        {options.map((opt, oIdx) => (
                          <input
                            key={oIdx}
                            type="text"
                            value={opt}
                            onChange={(e) => {
                              const newOpts = [...options];
                              newOpts[oIdx] = e.target.value;
                              setOptions(newOpts);
                            }}
                            placeholder={`Alt ${String.fromCharCode(65 + oIdx)}`}
                            className="px-2 py-1.5 rounded border border-border bg-card text-[10px] font-medium focus:outline-none"
                          />
                        ))}
                      </div>

                      <div className="flex items-center justify-between gap-2 mt-2">
                        <span className="text-[9px] text-muted-foreground font-bold">Alternativa Correta</span>
                        <select
                          value={correctOptionIdx}
                          onChange={(e) => setCorrectOptionIdx(Number(e.target.value))}
                          className="px-2 py-1 border border-border bg-card text-[10px] rounded focus:outline-none"
                        >
                          <option value={0}>Alternativa A</option>
                          <option value={1}>Alternativa B</option>
                          <option value={2}>Alternativa C</option>
                          <option value={3}>Alternativa D</option>
                        </select>
                      </div>

                      <button
                        type="button"
                        onClick={handleAddQuizQuestion}
                        className="w-full py-1.5 border border-primary/40 bg-primary/5 hover:bg-primary/10 text-primary text-[10px] font-bold rounded"
                      >
                        + Adicionar Questão
                      </button>
                    </div>
                  </div>
                )}

                <button
                  type="submit"
                  className="w-full py-3 bg-primary text-primary-foreground font-bold rounded-xl shadow-lg hover:bg-primary/95 transition-all text-xs"
                >
                  Confirmar e Adicionar Lição
                </button>
              </form>
            </div>
          ) : (
            <div className="p-6 border bg-white/60 backdrop-blur-xl rounded-[2rem] shadow-xl border-glass-border text-center">
              <Plus className="w-8 h-8 text-muted-foreground/30 mx-auto mb-2" />
              <h4 className="text-sm font-bold text-foreground">Nenhuma lição ativa</h4>
              <p className="text-xs text-muted-foreground mt-1 leading-relaxed">
                Clique no botão <strong>+ Lição</strong> de algum módulo ao lado para criar o conteúdo correspondente.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
