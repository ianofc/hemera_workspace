import React, { useState } from 'react';
import { Home, Users, BookOpen, GraduationCap, Settings, LogOut } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

export const Sidebar = () => {
  const [isHovered, setIsHovered] = useState(false);
  const navigate = useNavigate();
  const role = localStorage.getItem('hemera_user_role') || 'professor';

  const handleLogout = () => {
    localStorage.removeItem('hemera_user_role');
    navigate('/auth/login');
  };

  // Itens dinâmicos baseados no papel do usuário (Professor vs Aluno)
  const menuItems = role === 'professor' ? [
    { icon: Home, label: 'Dashboard', path: '/professor' },
    { icon: Users, label: 'Turmas & Chamada', path: '/professor/turmas' },
    { icon: BookOpen, label: 'Diário de Classe', path: '/professor/diario' },
    { icon: Settings, label: 'Configurações', path: '/professor/settings' },
  ] : [
    { icon: Home, label: 'Meu Painel', path: '/aluno' },
    { icon: GraduationCap, label: 'Trilha de Cursos', path: '/aluno/cursos' },
    { icon: BookOpen, label: 'Minhas Notas', path: '/aluno/notas' },
  ];

  return (
    <div 
      className={`fixed left-4 top-1/2 -translate-y-1/2 z-50 transition-all duration-300 ease-in-out
        bg-white/40 backdrop-blur-xl border border-glass-border shadow-2xl rounded-2xl py-6 flex flex-col gap-6
        ${isHovered ? 'w-64 px-6' : 'w-16 px-0 items-center'}
      `}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      {/* Logo Area */}
      <div className="flex items-center gap-4 px-2 mb-4">
        <div className="w-10 h-10 rounded-full bg-gradient-to-br from-primary to-secondary flex items-center justify-center shrink-0">
          <span className="text-white font-bold text-xl">H</span>
        </div>
        <span className={`font-bold text-gray-800 text-lg transition-opacity duration-300 whitespace-nowrap ${isHovered ? 'opacity-100' : 'opacity-0 hidden'}`}>
          Hemera OS
        </span>
      </div>

      {/* Menu Links */}
      <nav className="flex-1 flex flex-col gap-2 w-full">
        {menuItems.map((item, index) => (
          <button
            key={index}
            onClick={() => navigate(item.path)}
            className={`flex items-center gap-4 px-3 py-3 rounded-xl hover:bg-white/60 transition-colors w-full group ${!isHovered && 'justify-center'}`}
          >
            <item.icon className="w-6 h-6 text-gray-600 group-hover:text-primary shrink-0" />
            <span className={`text-gray-700 font-medium transition-opacity duration-300 whitespace-nowrap ${isHovered ? 'opacity-100' : 'opacity-0 hidden'}`}>
              {item.label}
            </span>
          </button>
        ))}
      </nav>

      {/* Logout */}
      <div className="w-full mt-auto">
        <button
          onClick={handleLogout}
          className={`flex items-center gap-4 px-3 py-3 rounded-xl hover:bg-red-500/10 hover:text-red-600 transition-colors w-full group ${!isHovered && 'justify-center'}`}
        >
          <LogOut className="w-6 h-6 text-gray-500 group-hover:text-red-600 shrink-0" />
          <span className={`font-medium transition-opacity duration-300 whitespace-nowrap ${isHovered ? 'opacity-100' : 'opacity-0 hidden'}`}>
            Sair
          </span>
        </button>
      </div>
    </div>
  );
};