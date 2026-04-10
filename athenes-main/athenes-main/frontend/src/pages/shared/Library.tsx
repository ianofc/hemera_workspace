import { useState } from 'react';
import { Search, BookOpen, Star, Filter } from 'lucide-react';
import { GlassCard } from '../../components/ui/GlassCard';

interface LibraryProps {
  view: 'student' | 'teacher';
}

export const Library = ({ view }: LibraryProps) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [filter, setFilter] = useState('all');

  const resources = [
    { title: 'Cálculo: Volume 1', author: 'James Stewart', type: 'book', source: 'Google Books', rating: 4.8 },
    { title: 'Física Quântica', author: 'David Griffiths', type: 'book', source: 'Open Library', rating: 4.9 },
    { title: 'Machine Learning', author: 'Andrew Ng', type: 'course', source: 'Coursera', rating: 4.7 },
    { title: 'Química Orgânica', author: 'Clayden', type: 'book', source: 'Google Books', rating: 4.6 },
  ];

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gradient mb-2">Biblioteca Digital</h1>
          <p className="text-slate-600">Acesse milhares de recursos educacionais integrados</p>
        </div>
      </div>

      <div className="flex gap-4">
        <div className="flex-1 relative">
          <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400" size={20} />
          <input
            type="text"
            placeholder="Buscar por título, autor ou assunto..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full glass-input pl-12"
          />
        </div>
        <button className="glass-button flex items-center gap-2">
          <Filter size={20} />
          Filtrar
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        {resources.map((resource, idx) => (
          <GlassCard key={idx} delay={idx * 0.1}>
            <div className="aspect-[3/4] rounded-xl bg-gradient-to-br from-slate-100 to-slate-200 mb-4 flex items-center justify-center text-6xl">
              📚
            </div>
            <h3 className="font-semibold text-slate-800 mb-1">{resource.title}</h3>
            <p className="text-sm text-slate-500 mb-3">{resource.author}</p>
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-1">
                <Star size={14} className="text-yellow-500 fill-yellow-500" />
                <span className="text-sm font-medium text-slate-700">{resource.rating}</span>
              </div>
              <span className="text-xs px-2 py-1 rounded-full bg-sky-50 text-sky-700">{resource.source}</span>
            </div>
          </GlassCard>
        ))}
      </div>
    </div>
  );
};