import React from 'react';
import { CourseTrail, Lesson } from '../../contexts/LyceumContext';
import { PlayCircle, FileText, CheckCircle2, Lock } from 'lucide-react';
import { motion } from 'framer-motion';

interface TrailMapProps {
  trail: CourseTrail;
  activeLessonId: number | null;
  onSelectLesson: (moduleId: number, lesson: Lesson) => void;
}

export const TrailMap: React.FC<TrailMapProps> = ({ trail, activeLessonId, onSelectLesson }) => {
  
  const getIcon = (type: 'VIDEO' | 'TEXTO' | 'EXERCICIO') => {
    if (type === 'VIDEO') return <PlayCircle className="w-5 h-5" />;
    if (type === 'TEXTO') return <FileText className="w-5 h-5" />;
    return <CheckCircle2 className="w-5 h-5" />;
  };

  // Determina se uma lição está liberada ou não
  // Regra simplificada: a primeira lição está liberada, e as próximas dependem da anterior estar concluída.
  const checkLessonStatus = (modules: CourseTrail['modules'], currentModIdx: number, currentLesIdx: number) => {
    // Primeira de todas está liberada
    if (currentModIdx === 0 && currentLesIdx === 0) {
      return 'unlocked';
    }

    // Acha a lição imediatamente anterior
    let prevLesson: Lesson | null = null;
    
    if (currentLesIdx > 0) {
      prevLesson = modules[currentModIdx].lessons[currentLesIdx - 1];
    } else if (currentModIdx > 0) {
      const prevMod = modules[currentModIdx - 1];
      prevLesson = prevMod.lessons[prevMod.lessons.length - 1];
    }

    if (prevLesson && prevLesson.completed) {
      return 'unlocked';
    }

    return 'locked';
  };

  return (
    <div className="space-y-12 py-6">
      {trail.modules.map((modulo, modIdx) => (
        <div key={modulo.id} className="relative">
          {/* Título do Módulo */}
          <div className="mb-8 text-center sm:text-left">
            <span className="text-[10px] font-extrabold text-primary uppercase tracking-widest bg-primary/10 border border-primary/20 px-3 py-1 rounded-full">
              Módulo {modIdx + 1}
            </span>
            <h3 className="text-xl font-bold font-display text-foreground mt-2">{modulo.title}</h3>
          </div>

          {/* Nós da Trilha do Módulo */}
          <div className="relative flex flex-col items-center sm:items-start gap-12 pl-0 sm:pl-12">
            
            {/* Linha vertical conectando os nós */}
            <div className="absolute left-1/2 sm:left-20 top-4 bottom-4 w-1 border-l-2 border-dashed border-gray-300 -translate-x-1/2" />

            {modulo.lessons.map((lesson, lesIdx) => {
              const status = lesson.completed 
                ? 'completed' 
                : checkLessonStatus(trail.modules, modIdx, lesIdx);
              
              const isActive = activeLessonId === lesson.id;
              
              // Alterna a margem dos nós horizontalmente para dar visual de "mapa sinuoso"
              const offsetClass = lesIdx % 2 === 0 
                ? 'sm:translate-x-4' 
                : 'sm:-translate-x-4';

              return (
                <div
                  key={lesson.id}
                  className={`relative z-10 flex flex-col sm:flex-row items-center gap-4 transition-all ${offsetClass}`}
                >
                  {/* Círculo do Nó */}
                  <motion.button
                    whileHover={status !== 'locked' ? { scale: 1.1 } : {}}
                    whileTap={status !== 'locked' ? { scale: 0.95 } : {}}
                    disabled={status === 'locked'}
                    onClick={() => onSelectLesson(modulo.id, lesson)}
                    className={`relative flex items-center justify-center w-16 h-16 rounded-full shadow-lg transition-all ${
                      status === 'completed'
                        ? 'bg-success text-white ring-4 ring-success/20'
                        : status === 'unlocked'
                          ? isActive
                            ? 'bg-primary text-white ring-4 ring-primary/30 animate-pulse'
                            : 'bg-card border-2 border-primary text-primary hover:bg-primary hover:text-white'
                          : 'bg-muted border-2 border-border text-muted-foreground cursor-not-allowed'
                    }`}
                  >
                    {status === 'locked' ? (
                      <Lock className="w-5 h-5" />
                    ) : (
                      getIcon(lesson.type)
                    )}

                    {/* Badge numérica indicativa no canto */}
                    <span className="absolute -top-1 -right-1 w-5 h-5 flex items-center justify-center text-[10px] font-bold rounded-full bg-foreground text-background border border-background shadow-sm">
                      {lesIdx + 1}
                    </span>
                  </motion.button>

                  {/* Informações ao Lado do Nó */}
                  <div className="text-center sm:text-left max-w-[200px]">
                    <h4 className={`text-xs font-bold leading-tight ${
                      isActive ? 'text-primary' : status === 'locked' ? 'text-muted-foreground' : 'text-foreground'
                    }`}>
                      {lesson.title}
                    </h4>
                    <span className="text-[10px] text-muted-foreground uppercase font-bold tracking-wider">
                      +{lesson.xpReward} XP
                    </span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      ))}
    </div>
  );
};
