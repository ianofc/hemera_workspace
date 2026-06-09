import React, { createContext, useContext, useState, useEffect } from 'react';
import { moodleService, MoodleEvent, MoodleGrade } from '../services/moodleService';

export interface QuizQuestion {
  id: number;
  question: string;
  options: string[];
  correctOptionIndex: number;
}

export interface Lesson {
  id: number;
  title: string;
  type: 'VIDEO' | 'TEXTO' | 'EXERCICIO';
  completed: boolean;
  content: string;
  xpReward: number;
  videoUrl?: string;
  quiz?: QuizQuestion[];
}

export interface Module {
  id: number;
  title: string;
  lessons: Lesson[];
}

export interface CourseTrail {
  id: number;
  title: string;
  description: string;
  progress: number;
  modules: Module[];
}

export interface Badge {
  id: string;
  title: string;
  description: string;
  icon: string;
  unlocked: boolean;
  unlockedAt?: string;
  category: 'trail' | 'quiz' | 'moodle' | 'level';
}

interface LyceumContextType {
  xp: number;
  level: number;
  xpForNextLevel: number;
  badges: Badge[];
  trails: CourseTrail[];
  moodleEvents: MoodleEvent[];
  moodleGrades: MoodleGrade[];
  isMoodleSynced: boolean;
  completeLesson: (courseId: number, moduleId: number, lessonId: number) => void;
  unlockBadge: (badgeId: string) => void;
  syncWithMoodle: (url: string, token: string) => Promise<boolean>;
  updateTrail: (courseId: number, updatedModules: Module[]) => void;
  addXp: (amount: number) => void;
}

const INITIAL_TRAILS: CourseTrail[] = [
  {
    id: 1,
    title: "Matemática Avançada",
    description: "Desvende os segredos das derivadas, integrais e da geometria analítica tridimensional.",
    progress: 0,
    modules: [
      {
        id: 101,
        title: "Módulo 1 — Introdução aos Limites",
        lessons: [
          {
            id: 1001,
            title: "Conceito Intuitivo de Limite",
            type: "TEXTO",
            completed: false,
            xpReward: 50,
            content: "Um limite descreve o comportamento de uma função à medida que o argumento se aproxima de um determinado valor. Escrevemos lim_{x -> c} f(x) = L para dizer que f(x) fica arbitrariamente próximo de L à medida que x se aproxima de c. Este conceito é a base de todo o cálculo diferencial e integral."
          },
          {
            id: 1002,
            title: "Cálculo Limites por Fatoração",
            type: "VIDEO",
            completed: false,
            xpReward: 80,
            videoUrl: "https://www.youtube.com/embed/dQw4w9WgXcQ",
            content: "Neste vídeo, vamos abordar como resolver indeterminações matemáticas do tipo 0/0 simplificando expressões algébricas. A fatoração é a nossa ferramenta principal para remover as descontinuidades removíveis de funções racionais."
          },
          {
            id: 1003,
            title: "Quiz: Prática de Limites",
            type: "EXERCICIO",
            completed: false,
            xpReward: 120,
            quiz: [
              {
                id: 1,
                question: "Qual o limite de (x^2 - 4) / (x - 2) quando x tende a 2?",
                options: ["2", "4", "0", "Inexistente"],
                correctOptionIndex: 1
              },
              {
                id: 2,
                question: "Se lim f(x) = 5 e lim g(x) = -2, qual o valor de lim [2*f(x) - g(x)]?",
                options: ["8", "12", "3", "10"],
                correctOptionIndex: 1
              }
            ],
            content: "Coloque seus conhecimentos à prova resolvendo este quiz interativo de limites e ganhe XP bônus!"
          }
        ]
      },
      {
        id: 102,
        title: "Módulo 2 — Derivadas e Taxas de Variação",
        lessons: [
          {
            id: 1004,
            title: "A Reta Tangente",
            type: "TEXTO",
            completed: false,
            xpReward: 60,
            content: "A derivada de uma função em um ponto representa a inclinação da reta tangente ao gráfico da função nesse ponto. É o limite da taxa média de variação à medida que o intervalo de tempo ou espaço tende a zero."
          },
          {
            id: 1005,
            title: "Regras Básicas de Derivação",
            type: "EXERCICIO",
            completed: false,
            xpReward: 100,
            quiz: [
              {
                id: 3,
                question: "Qual a derivada de f(x) = 3x^2 + 5x - 7?",
                options: ["6x + 5", "3x + 5", "6x", "f'(x) = 0"],
                correctOptionIndex: 0
              }
            ],
            content: "Exercício de fixação das regras do tombo, soma e constante nas derivadas."
          }
        ]
      }
    ]
  },
  {
    id: 2,
    title: "Física Quântica",
    description: "Explore as propriedades bizarras das partículas subatômicas, superposição e o gato de Schrödinger.",
    progress: 0,
    modules: [
      {
        id: 201,
        title: "Módulo 1 — Dualidade Onda-Partícula",
        lessons: [
          {
            id: 2001,
            title: "O Efeito Fotoelétrico",
            type: "TEXTO",
            completed: false,
            xpReward: 60,
            content: "Einstein explicou o efeito fotoelétrico sugerindo que a luz é quantizada em pequenos pacotes de energia chamados fótons. A energia de cada fóton depende unicamente de sua frequência (E = h*f). Isso provou que a luz se comporta como partícula sob certas condições."
          },
          {
            id: 2002,
            title: "Experimento de Dupla Fenda",
            type: "VIDEO",
            completed: false,
            xpReward: 80,
            videoUrl: "https://www.youtube.com/embed/dQw4w9WgXcQ",
            content: "Uma demonstração impressionante de como elétrons criam padrões de interferência ao passar por duas fendas, agindo como ondas, a menos que sejam ativamente observados durante a passagem."
          }
        ]
      }
    ]
  }
];

const INITIAL_BADGES: Badge[] = [
  {
    id: 'badge-welcome',
    title: 'Primeiro Passo',
    description: 'Começou sua jornada acadêmica no Lyceum.',
    icon: '🏆',
    unlocked: true,
    unlockedAt: new Date().toISOString(),
    category: 'level'
  },
  {
    id: 'badge-first-lesson',
    title: 'Explorador',
    description: 'Concluiu a primeira lição com sucesso.',
    icon: '📖',
    unlocked: false,
    category: 'trail'
  },
  {
    id: 'badge-perfect-quiz',
    title: 'Cérebro de Aço',
    description: 'Acertou todas as perguntas de um quiz.',
    icon: '⚡',
    unlocked: false,
    category: 'quiz'
  },
  {
    id: 'badge-moodle-sync',
    title: 'Sincronizado',
    description: 'Integrou e sincronizou com sucesso as notas do Moodle.',
    icon: '🔄',
    unlocked: false,
    category: 'moodle'
  },
  {
    id: 'badge-level-2',
    title: 'Acadêmico Nível 2',
    description: 'Atingiu o nível 2 na trilha de conhecimento.',
    icon: '🌟',
    unlocked: false,
    category: 'level'
  },
  {
    id: 'badge-trail-blazer',
    title: 'Desbravador',
    description: 'Concluiu um módulo inteiro em qualquer disciplina.',
    icon: '🗺️',
    unlocked: false,
    category: 'trail'
  }
];

const LyceumContext = createContext<LyceumContextType | undefined>(undefined);

export const LyceumProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [xp, setXp] = useState<number>(() => {
    const saved = localStorage.getItem('lyceum_xp');
    return saved ? parseInt(saved, 10) : 0;
  });

  const [level, setLevel] = useState<number>(() => {
    const saved = localStorage.getItem('lyceum_level');
    return saved ? parseInt(saved, 10) : 1;
  });

  const [badges, setBadges] = useState<Badge[]>(() => {
    const saved = localStorage.getItem('lyceum_badges');
    return saved ? JSON.parse(saved) : INITIAL_BADGES;
  });

  const [trails, setTrails] = useState<CourseTrail[]>(() => {
    const saved = localStorage.getItem('lyceum_trails');
    return saved ? JSON.parse(saved) : INITIAL_TRAILS;
  });

  const [moodleEvents, setMoodleEvents] = useState<MoodleEvent[]>([]);
  const [moodleGrades, setMoodleGrades] = useState<MoodleGrade[]>([]);
  const [isMoodleSynced, setIsMoodleSynced] = useState<boolean>(false);

  const xpForNextLevel = level * 300;

  // Carrega eventos do Moodle no mount
  useEffect(() => {
    setMoodleEvents(moodleService.getSyncedEvents());
    setMoodleGrades(moodleService.getSyncedGrades());
    const config = moodleService.getConfig();
    if (config.token) {
      setIsMoodleSynced(true);
    }
  }, []);

  // Salva XP e level no localStorage sempre que mudar
  useEffect(() => {
    localStorage.setItem('lyceum_xp', xp.toString());
    localStorage.setItem('lyceum_level', level.toString());
  }, [xp, level]);

  // Salva badges no localStorage
  useEffect(() => {
    localStorage.setItem('lyceum_badges', JSON.stringify(badges));
  }, [badges]);

  // Salva trilhas no localStorage
  useEffect(() => {
    localStorage.setItem('lyceum_trails', JSON.stringify(trails));
  }, [trails]);

  const addXp = (amount: number) => {
    setXp((prevXp) => {
      let newXp = prevXp + amount;
      let currentLevel = level;
      let nextLevelXp = currentLevel * 300;

      while (newXp >= nextLevelXp) {
        newXp -= nextLevelXp;
        currentLevel += 1;
        nextLevelXp = currentLevel * 300;
        
        // Dispara Level Up!
        setTimeout(() => {
          setLevel(currentLevel);
          if (currentLevel >= 2) {
            unlockBadge('badge-level-2');
          }
        }, 100);
      }
      return newXp;
    });
  };

  const unlockBadge = (badgeId: string) => {
    setBadges((prevBadges) =>
      prevBadges.map((badge) => {
        if (badge.id === badgeId && !badge.unlocked) {
          return {
            ...badge,
            unlocked: true,
            unlockedAt: new Date().toISOString(),
          };
        }
        return badge;
      })
    );
  };

  const completeLesson = (courseId: number, moduleId: number, lessonId: number) => {
    let xpAwarded = 0;
    
    const updatedTrails = trails.map((trail) => {
      if (trail.id !== courseId) return trail;

      const updatedModules = trail.modules.map((mod) => {
        if (mod.id !== moduleId) return mod;

        const updatedLessons = mod.lessons.map((les) => {
          if (les.id !== lessonId) return les;
          if (les.completed) return les; // Já concluído

          xpAwarded = les.xpReward;
          return { ...les, completed: true };
        });

        // Verifica se completou o módulo inteiro
        const allCompleted = updatedLessons.every(l => l.completed);
        if (allCompleted) {
          setTimeout(() => unlockBadge('badge-trail-blazer'), 200);
        }

        return { ...mod, lessons: updatedLessons };
      });

      // Calcula novo progresso do curso
      const totalLessons = updatedModules.reduce((acc, m) => acc + m.lessons.length, 0);
      const completedLessons = updatedModules.reduce((acc, m) => acc + m.lessons.filter(l => l.completed).length, 0);
      const newProgress = Math.round((completedLessons / totalLessons) * 100);

      return { ...trail, modules: updatedModules, progress: newProgress };
    });

    setTrails(updatedTrails);

    if (xpAwarded > 0) {
      addXp(xpAwarded);
      unlockBadge('badge-first-lesson');
    }
  };

  const syncWithMoodle = async (url: string, token: string): Promise<boolean> => {
    const config = { url, token, autoSync: true };
    const res = await moodleService.syncMoodle(config);
    if (res.success) {
      setMoodleEvents(moodleService.getSyncedEvents());
      setMoodleGrades(moodleService.getSyncedGrades());
      setIsMoodleSynced(true);
      unlockBadge('badge-moodle-sync');
      addXp(100); // 100 XP por sincronizar com Moodle
      return true;
    }
    return false;
  };

  const updateTrail = (courseId: number, updatedModules: Module[]) => {
    const updatedTrails = trails.map((trail) => {
      if (trail.id !== courseId) return trail;

      const totalLessons = updatedModules.reduce((acc, m) => acc + m.lessons.length, 0);
      const completedLessons = updatedModules.reduce((acc, m) => acc + m.lessons.filter(l => l.completed).length, 0);
      const newProgress = totalLessons > 0 ? Math.round((completedLessons / totalLessons) * 100) : 0;

      return { ...trail, modules: updatedModules, progress: newProgress };
    });
    setTrails(updatedTrails);
  };

  return (
    <LyceumContext.Provider
      value={{
        xp,
        level,
        xpForNextLevel,
        badges,
        trails,
        moodleEvents,
        moodleGrades,
        isMoodleSynced,
        completeLesson,
        unlockBadge,
        syncWithMoodle,
        updateTrail,
        addXp,
      }}
    >
      {children}
    </LyceumContext.Provider>
  );
};

export const useLyceum = () => {
  const context = useContext(LyceumContext);
  if (context === undefined) {
    throw new Error('useLyceum must be used within a LyceumProvider');
  }
  return context;
};
