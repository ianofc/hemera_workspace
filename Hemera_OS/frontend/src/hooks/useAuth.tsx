import React, { createContext, useContext, useState, useEffect } from 'react';

interface User {
  id: string;
  email: string;
  role: 'professor' | 'aluno' | 'admin';
}

interface AuthContextType {
  user: User | null;
  role: 'professor' | 'aluno' | 'admin' | null; // Adicionado aqui
  login: (role: 'professor' | 'aluno' | 'admin') => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{children: React.ReactNode}> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);

  const role = user ? user.role : null;

  useEffect(() => {
    const storedRole = localStorage.getItem('hemera_user_role') as 'professor' | 'aluno' | 'admin';
    if (storedRole) {
      setUser({ id: '1', email: 'admin@hemera.os', role: storedRole });
    }
  }, []);

  const login = (role: 'professor' | 'aluno' | 'admin') => {
    localStorage.setItem('hemera_user_role', role);
    setUser({ id: '1', email: 'admin@hemera.os', role });
  };

  const logout = () => {
    localStorage.removeItem('hemera_user_role');
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, role, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

// eslint-disable-next-line react-refresh/only-export-components
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth deve ser usado dentro de um AuthProvider');
  }
  return context;
};