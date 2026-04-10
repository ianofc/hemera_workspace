import { create } from 'zustand';

interface User {
  id: string;
  name: string;
  email: string;
  role: 'student' | 'teacher';
}

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: {
    id: '1',
    name: 'João Silva',
    email: 'joao@email.com',
    role: 'student'
  },
  isAuthenticated: true,
  login: async (email, password) => {
    set({ 
      user: { id: '1', name: 'João Silva', email, role: 'student' },
      isAuthenticated: true 
    });
  },
  logout: () => set({ user: null, isAuthenticated: false }),
}));