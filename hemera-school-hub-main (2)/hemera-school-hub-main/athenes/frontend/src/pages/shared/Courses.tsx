import { useState } from 'react';
import { motion } from 'framer-motion';
import { PlayCircle, BookOpen, Plus, MoreVertical } from 'lucide-react';
import { GlassCard } from '../../components/ui/GlassCard';
import { useNavigate } from 'react-router-dom';

interface CoursesProps {
  view: 'student' | 'teacher';
}

export const Courses = ({ view }: CoursesProps) => {
  const navigate = useNavigate();
  const isStudent = view === 'student';

  const coursesList = [
    { id: 1, title: 'Cálculo Diferencial', instructor: 'Prof. Silva', progress: 75, total: 20, completed: 15, image: '🔢', color: 'sky' },
    { id: 2, title: 'Física Quântica', instructor: 'Profa. Santos', progress: 45, total: 16, completed: 7, image: '⚛️', color: 'indigo' },
    { id: 3, title: 'Python Avançado', instructor: 'Prof. Oliveira', progress: 90, total: 12, completed: 11, image: '🐍', color: 'purple' },
    { id: 4, title: 'Química Orgânica', instructor: 'Profa. Lima', progress: 30, total: 24, completed: 7, image: '⚗️', color: 'pink' },
  ];

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gradient mb-2">{isStudent ? 'Meus Cursos' : 'Gerenciar Cursos'}</h1>
          <p className="text-slate-600">{isStudent ? 'Continue sua jornada' : 'Gerencie seus cursos'}</p>
        </div>
        {!isStudent && (
          <button className="glass-button bg-alpine-500 text-white border-0 hover:bg-alpine-600 flex items-center gap-2">
            <Plus size={20} /> Novo Curso
          </button>
        )}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {coursesList.map((course, idx) => (
          <GlassCard key={idx} delay={idx * 0.1}>
            <div className={`h-32 rounded-xl bg-${course.color}-100 flex items-center justify-center text-6xl mb-4`}>
              {course.image}
            </div>
            <h3 className="font-bold text-slate-800 mb-1">{course.title}</h3>
            <p className="text-sm text-slate-500 mb-3">{course.instructor}</p>
            <div className="space-y-2">
              <div className="flex justify-between text-xs text-slate-600">
                <span>{course.completed}/{course.total} aulas</span>
                <span>{course.progress}%</span>
              </div>
              <div className="h-2 bg-slate-200 rounded-full">
                <div className={`h-full bg-${course.color}-500 rounded-full`} style={{ width: `${course.progress}%` }} />
              </div>
            </div>
          </GlassCard>
        ))}
      </div>
    </div>
  );
};