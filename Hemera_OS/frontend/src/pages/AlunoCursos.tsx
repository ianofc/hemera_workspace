import React, { useState } from 'react';
import { AppLayout } from '../components/layout/AppLayout';
import { useLyceum, Lesson } from '../contexts/LyceumContext';
import { GamificationStats } from '../components/lyceum/GamificationStats';
import { TrailMap } from '../components/lyceum/TrailMap';
import { LessonViewer } from '../components/lyceum/LessonViewer';
import { BookOpen, HelpCircle } from 'lucide-react';

const AlunoCursos: React.FC = () => {
  const { trails } = useLyceum();
  const [selectedCourseId, setSelectedCourseId] = useState<number>(trails[0]?.id || 1);
  const [activeModuleId, setActiveModuleId] = useState<number | null>(null);
  const [activeLesson, setActiveLesson] = useState<Lesson | null>(null);

  const currentTrail = trails.find(t => t.id === selectedCourseId) || trails[0];

  const handleSelectLesson = (moduleId: number, lesson: Lesson) => {
    setActiveModuleId(moduleId);
    setActiveLesson(lesson);
  };

  const handleLessonCompleted = () => {
    // Pode atualizar estado ou fazer scroll
    setActiveLesson(prev => prev ? { ...prev, completed: true } : null);
  };

  return (
    <AppLayout role="aluno">
      <div className="max-w-[1600px] mx-auto px-6 space-y-8 pb-20">
        
        {/* Progresso de XP e Nível no Topo */}
        <section>
          <GamificationStats />
        </section>

        {/* Corpo Principal da Trilha */}
        <section className="grid grid-cols-1 lg:grid-cols-3 gap-8 items-start">
          
          {/* Lado Esquerdo: Seletor de Curso e Mapa da Trilha */}
          <div className="lg:col-span-1 border bg-white/60 backdrop-blur-xl rounded-[2rem] shadow-xl border-glass-border p-6 space-y-6">
            <div className="flex items-center justify-between border-b border-gray-100 pb-4">
              <h3 className="flex items-center gap-2 text-base font-bold text-foreground">
                <BookOpen className="w-5 h-5 text-primary" /> Trilha de Cursos
              </h3>
              
              <select
                value={selectedCourseId}
                onChange={(e) => {
                  setSelectedCourseId(Number(e.target.value));
                  setActiveLesson(null);
                  setActiveModuleId(null);
                }}
                className="px-3 py-1.5 rounded-xl border border-border bg-card text-foreground font-bold text-xs focus:ring-2 focus:ring-primary/20 focus:outline-none"
              >
                {trails.map(t => (
                  <option key={t.id} value={t.id}>{t.title}</option>
                ))}
              </select>
            </div>

            <p className="text-xs text-muted-foreground leading-relaxed">
              {currentTrail?.description}
            </p>

            <div className="max-h-[500px] overflow-y-auto pr-2 custom-scrollbar">
              {currentTrail && (
                <TrailMap
                  trail={currentTrail}
                  activeLessonId={activeLesson?.id || null}
                  onSelectLesson={handleSelectLesson}
                />
              )}
            </div>
          </div>

          {/* Lado Direito: Visualizador de Lição */}
          <div className="lg:col-span-2 border bg-white/60 backdrop-blur-xl rounded-[2rem] shadow-xl border-glass-border p-6 md:p-8 min-h-[500px] flex flex-col">
            {activeLesson && activeModuleId !== null ? (
              <LessonViewer
                courseId={selectedCourseId}
                moduleId={activeModuleId}
                lesson={activeLesson}
                onLessonCompleted={handleLessonCompleted}
              />
            ) : (
              <div className="flex-1 flex flex-col items-center justify-center text-center p-8">
                <div className="flex items-center justify-center w-16 h-16 bg-primary/10 text-primary rounded-full mb-4">
                  <HelpCircle className="w-8 h-8 animate-pulse" />
                </div>
                <h4 className="text-lg font-bold text-foreground mb-1">Selecione uma Lição</h4>
                <p className="text-sm text-muted-foreground max-w-sm">
                  Escolha uma lição desbloqueada no mapa da trilha ao lado para começar seus estudos e acumular XP.
                </p>
              </div>
            )}
          </div>
        </section>

      </div>
    </AppLayout>
  );
};

export default AlunoCursos;
