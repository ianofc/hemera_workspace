import { NavLink, useLocation } from 'react-router-dom';
import { motion } from 'framer-motion';
import { 
  BookOpen, Library, FileText, GraduationCap, 
  MessageCircle, LayoutDashboard, Upload, LogOut
} from 'lucide-react';
import { useAuthStore } from '../../store/authStore';

interface SidebarProps {
  userType: 'student' | 'teacher';
}

export const Sidebar = ({ userType }: SidebarProps) => {
  const location = useLocation();
  const { logout, user } = useAuthStore();

  const studentLinks = [
    { to: '/student', icon: LayoutDashboard, label: 'Dashboard' },
    { to: '/student/courses', icon: GraduationCap, label: 'Meus Cursos' },
    { to: '/student/library', icon: Library, label: 'Biblioteca' },
    { to: '/student/materials', icon: FileText, label: 'Materiais' },
    { to: '/student/zeus', icon: MessageCircle, label: 'Zeus AI' },
  ];

  const teacherLinks = [
    { to: '/teacher', icon: LayoutDashboard, label: 'Dashboard' },
    { to: '/teacher/courses', icon: BookOpen, label: 'Gerenciar Cursos' },
    { to: '/teacher/upload', icon: Upload, label: 'Enviar Aulas' },
    { to: '/teacher/library', icon: Library, label: 'Biblioteca' },
    { to: '/teacher/materials', icon: FileText, label: 'Materiais' },
  ];

  const links = userType === 'student' ? studentLinks : teacherLinks;

  return (
    <motion.aside 
      initial={{ x: -100, opacity: 0 }}
      animate={{ x: 0, opacity: 1 }}
      className="fixed left-0 top-0 h-screen w-72 glass border-r border-white/40 z-50 flex flex-col"
    >
      <div className="p-6 border-b border-white/30">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-alpine-400 to-zeus-primary flex items-center justify-center shadow-lg">
            <span className="text-white font-bold text-xl">A</span>
          </div>
          <div>
            <h1 className="text-xl font-bold text-gradient">ATHENES</h1>
            <p className="text-xs text-slate-500 uppercase tracking-wider">
              {userType === 'student' ? 'Área do Aluno' : 'Área do Professor'}
            </p>
          </div>
        </div>
      </div>

      <nav className="flex-1 p-4 space-y-2 overflow-y-auto scrollbar-hide">
        {links.map((link, index) => {
          const Icon = link.icon;
          const isActive = location.pathname === link.to;

          return (
            <NavLink
              key={link.to}
              to={link.to}
              className={`nav-item ${isActive ? 'active' : ''}`}
            >
              <motion.div
                initial={{ scale: 0.8, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                transition={{ delay: index * 0.1 }}
              >
                <Icon size={20} className={isActive ? 'text-zeus-primary' : ''} />
              </motion.div>
              <span>{link.label}</span>
              {isActive && (
                <motion.div
                  layoutId="activeIndicator"
                  className="absolute left-0 w-1 h-8 bg-gradient-to-b from-alpine-400 to-zeus-primary rounded-r-full"
                />
              )}
            </NavLink>
          );
        })}
      </nav>

      <div className="p-4 border-t border-white/30">
        <div className="glass-card p-4 mb-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-full bg-gradient-to-br from-zeus-secondary to-zeus-accent flex items-center justify-center text-white font-semibold">
              {user?.name?.charAt(0) || 'U'}
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-semibold text-slate-800 truncate">{user?.name}</p>
              <p className="text-xs text-slate-500 truncate">{user?.email}</p>
            </div>
          </div>
        </div>

        <button 
          onClick={logout}
          className="w-full glass-button flex items-center justify-center gap-2 text-red-600 hover:text-red-700"
        >
          <LogOut size={18} />
          <span>Sair</span>
        </button>
      </div>
    </motion.aside>
  );
};