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
  user: null,
  isAuthenticated: false,
  login: async (email, password) => {
    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
      const response = await fetch(`${apiUrl}/api/status/login/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      });
      
      const data = await response.json();
      
      if (response.ok && data.token) {
        // Armazenar o token localmente
        localStorage.setItem('hemera_auth_token', data.token);
        
        set({ 
          user: data.user,
          isAuthenticated: true 
        });
      } else {
        alert(data.error || "Erro no login, verifique suas credenciais.");
        throw new Error(data.error || "Erro de login");
      }
    } catch (error) {
      console.error("Falha ao se conectar à API de Autenticação", error);
      throw error;
    }
  },
  logout: () => {
    localStorage.removeItem('hemera_auth_token');
    set({ user: null, isAuthenticated: false });
  },
}));