export interface MoodleConfig {
  url: string;
  token: string;
  autoSync: boolean;
}

export interface MoodleEvent {
  id: string;
  title: string;
  description: string;
  dueDate: string;
  courseName: string;
  type: 'assignment' | 'exam' | 'event';
  status: 'pending' | 'submitted' | 'graded';
}

export interface MoodleGrade {
  id: string;
  assignmentName: string;
  courseName: string;
  grade: number;
  maxGrade: number;
  feedback?: string;
  gradedDate: string;
}

const DEFAULT_EVENTS: MoodleEvent[] = [
  {
    id: 'm-1',
    title: 'Entrega do Projeto 1: Geometria Espacial',
    description: 'Enviar relatório PDF contendo os cálculos dos sólidos geométricos e modelos em 3D.',
    dueDate: new Date(Date.now() + 2 * 24 * 60 * 60 * 1000).toISOString(), // 2 dias no futuro
    courseName: 'Matemática Avançada',
    type: 'assignment',
    status: 'pending',
  },
  {
    id: 'm-2',
    title: 'Questionário sobre Teoria da Relatividade',
    description: 'Responder ao questionário online no ambiente do Moodle.',
    dueDate: new Date(Date.now() + 5 * 24 * 60 * 60 * 1000).toISOString(), // 5 dias no futuro
    courseName: 'Física Quântica',
    type: 'assignment',
    status: 'pending',
  },
  {
    id: 'm-3',
    title: 'Avaliação Presencial: Literatura do Romantismo',
    description: 'Prova em sala de aula abrangendo a primeira e segunda geração romântica.',
    dueDate: new Date(Date.now() + 8 * 24 * 60 * 60 * 1000).toISOString(), // 8 dias no futuro
    courseName: 'Literatura Brasileira',
    type: 'exam',
    status: 'pending',
  },
  {
    id: 'm-4',
    title: 'Estudo de Caso: Divisão Celular e Mitose',
    description: 'Enviar o artigo resumido de biologia celular.',
    dueDate: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000).toISOString(), // 1 dia no passado
    courseName: 'Biologia Molecular',
    type: 'assignment',
    status: 'submitted',
  }
];

const DEFAULT_GRADES: MoodleGrade[] = [
  {
    id: 'g-1',
    assignmentName: 'Exercícios Vetores e Matrizes',
    courseName: 'Matemática Avançada',
    grade: 9.5,
    maxGrade: 10.0,
    feedback: 'Excelente raciocínio lógico demonstrado no exercício 4. Continue assim!',
    gradedDate: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000).toISOString()
  },
  {
    id: 'g-2',
    assignmentName: 'Relatório de Experimento do Prisma',
    courseName: 'Física Quântica',
    grade: 8.0,
    maxGrade: 10.0,
    feedback: 'Bom relatório, mas faltou detalhar a incerteza de medição.',
    gradedDate: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString()
  }
];

export const moodleService = {
  getConfig: (): MoodleConfig => {
    const config = localStorage.getItem('lyceum_moodle_config');
    if (config) {
      return JSON.parse(config);
    }
    return {
      url: 'https://moodle.hemera.edu.br',
      token: '',
      autoSync: true
    };
  },

  saveConfig: (config: MoodleConfig): void => {
    localStorage.setItem('lyceum_moodle_config', JSON.stringify(config));
  },

  getSyncedEvents: (): MoodleEvent[] => {
    const events = localStorage.getItem('lyceum_moodle_events');
    if (events) {
      return JSON.parse(events);
    }
    // Inicializa com dados iniciais mocks
    localStorage.setItem('lyceum_moodle_events', JSON.stringify(DEFAULT_EVENTS));
    return DEFAULT_EVENTS;
  },

  getSyncedGrades: (): MoodleGrade[] => {
    const grades = localStorage.getItem('lyceum_moodle_grades');
    if (grades) {
      return JSON.parse(grades);
    }
    // Inicializa com dados iniciais mocks
    localStorage.setItem('lyceum_moodle_grades', JSON.stringify(DEFAULT_GRADES));
    return DEFAULT_GRADES;
  },

  syncMoodle: async (config: MoodleConfig): Promise<{ success: boolean; eventsCount: number; gradesCount: number }> => {
    // Simula uma requisição de rede para sincronizar com o Moodle
    await new Promise((resolve) => setTimeout(resolve, 2000));
    
    // Atualiza configurações salvas
    moodleService.saveConfig(config);
    
    // Simula novos dados vindos do Moodle (caso o token seja preenchido)
    let events = moodleService.getSyncedEvents();
    let grades = moodleService.getSyncedGrades();
    
    if (config.token) {
      // Se houver token, simula a importação/sincronização bem sucedida com novas adições
      // Por exemplo, marcar a entrega de Matemática Avançada pendente como concluída ou atualizar notas
      events = events.map(ev => {
        if (ev.id === 'm-1' && ev.status === 'pending') {
          return { ...ev, status: 'submitted' };
        }
        return ev;
      });

      // Adiciona uma nova nota simulada
      if (!grades.some(g => g.id === 'g-3')) {
        grades = [
          ...grades,
          {
            id: 'g-3',
            assignmentName: 'Estudo de Caso: Divisão Celular',
            courseName: 'Biologia Molecular',
            grade: 9.0,
            maxGrade: 10.0,
            feedback: 'Excelente trabalho na modelagem da prófase.',
            gradedDate: new Date().toISOString()
          }
        ];
      }
    }
    
    localStorage.setItem('lyceum_moodle_events', JSON.stringify(events));
    localStorage.setItem('lyceum_moodle_grades', JSON.stringify(grades));

    return {
      success: true,
      eventsCount: events.length,
      gradesCount: grades.length
    };
  }
};
