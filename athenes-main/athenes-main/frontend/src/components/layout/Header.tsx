import { Bell, Settings, Search } from 'lucide-react';

export const Header = () => {
  return (
    <header className="h-16 glass border-b border-white/40 flex items-center justify-between px-8 fixed top-0 right-0 left-72 z-40">
      <div className="flex items-center gap-4 flex-1">
        <div className="relative flex-1 max-w-md">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={20} />
          <input 
            type="text" 
            placeholder="Buscar..." 
            className="w-full glass-input pl-10"
          />
        </div>
      </div>
      <div className="flex items-center gap-4">
        <button className="p-2 rounded-xl hover:bg-white/60 transition-colors relative">
          <Bell size={20} className="text-slate-600" />
          <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full" />
        </button>
        <button className="p-2 rounded-xl hover:bg-white/60 transition-colors">
          <Settings size={20} className="text-slate-600" />
        </button>
      </div>
    </header>
  );
};