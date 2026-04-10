import { useState } from 'react';
import { FileText, Download, Folder, Search, Filter } from 'lucide-react';
import { GlassCard } from '../../components/ui/GlassCard';

interface MaterialsProps {
  view: 'student' | 'teacher';
}

export const Materials = ({ view }: MaterialsProps) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedFolder, setSelectedFolder] = useState('all');

  const folders = [
    { id: 'all', name: 'Todos', count: 24 },
    { id: 'math', name: 'Matemática', count: 8 },
    { id: 'physics', name: 'Física', count: 6 },
    { id: 'cs', name: 'Computação', count: 10 },
  ];

  const materials = [
    { name: 'Apostila de Cálculo.pdf', size: '15.2 MB', type: 'pdf', date: '2024-01-15', folder: 'math' },
    { name: 'Lista de Exercícios 1.docx', size: '2.4 MB', type: 'doc', date: '2024-01-14', folder: 'math' },
    { name: 'Experimento Física Lab.pdf', size: '8.7 MB', type: 'pdf', date: '2024-01-13', folder: 'physics' },
    { name: 'Código Fonte - Aula 3.zip', size: '45.2 MB', type: 'zip', date: '2024-01-12', folder: 'cs' },
  ];

  const getIcon = (type: string) => {
    switch(type) {
      case 'pdf': return '📄';
      case 'doc': return '📝';
      case 'zip': return '📦';
      default: return '📎';
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gradient mb-2">Material de Apoio</h1>
          <p className="text-slate-600">Acesse documentos, apostilas e recursos complementares</p>
        </div>
        {view === 'teacher' && (
          <button className="glass-button bg-alpine-500 text-white border-0 hover:bg-alpine-600">
            Upload Material
          </button>
        )}
      </div>

      <div className="flex gap-4">
        <div className="flex-1 relative">
          <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400" size={20} />
          <input
            type="text"
            placeholder="Buscar materiais..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full glass-input pl-12"
          />
        </div>
        <button className="glass-button flex items-center gap-2">
          <Filter size={20} /> Filtrar
        </button>
      </div>

      <div className="flex gap-4 overflow-x-auto pb-2">
        {folders.map((folder) => (
          <button
            key={folder.id}
            onClick={() => setSelectedFolder(folder.id)}
            className={`flex items-center gap-2 px-4 py-2 rounded-xl whitespace-nowrap transition-colors ${
              selectedFolder === folder.id 
                ? 'bg-alpine-100 text-alpine-700 border border-alpine-200' 
                : 'glass-button'
            }`}
          >
            <Folder size={18} />
            <span>{folder.name}</span>
            <span className="text-xs bg-white/60 px-2 py-0.5 rounded-full">{folder.count}</span>
          </button>
        ))}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {materials.map((material, idx) => (
          <GlassCard key={idx} delay={idx * 0.05} className="flex items-center gap-4">
            <div className="text-4xl">{getIcon(material.type)}</div>
            <div className="flex-1 min-w-0">
              <h4 className="font-medium text-slate-800 truncate">{material.name}</h4>
              <p className="text-xs text-slate-500">{material.size} • {material.date}</p>
            </div>
            <button className="p-2 rounded-lg hover:bg-white/60 transition-colors">
              <Download size={18} className="text-slate-400" />
            </button>
          </GlassCard>
        ))}
      </div>
    </div>
  );
};