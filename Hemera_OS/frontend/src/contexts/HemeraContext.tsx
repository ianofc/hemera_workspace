import React, { createContext, useContext, useState, useEffect } from 'react';

interface HemeraContextData {
  user: any;
  token: string | null;
  isAuthenticated: boolean;
  login: (username: string, token: string) => Promise<void>;
  logout: () => void;
}

const HemeraContext = createContext<HemeraContextData>({} as HemeraContextData);

export const HemeraProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<any>(null);
  const [token, setToken] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Carrega a sessão local se existir
    const storagedToken = localStorage.getItem('@Hemera:token');
    const storagedUser = localStorage.getItem('@Hemera:user');

    if (storagedToken && storagedUser) {
      setToken(storagedToken);
      setUser(JSON.parse(storagedUser));
    }
    setLoading(false);
  }, []);

  const login = async (username: string, newToken: string) => {
    const mockUser = {
      username,
      name: username.charAt(0).toUpperCase() + username.slice(1),
      role: username === 'professor' ? 'professor' : 'student',
    };
    
    setUser(mockUser);
    setToken(newToken);

    localStorage.setItem('@Hemera:user', JSON.stringify(mockUser));
    localStorage.setItem('@Hemera:token', newToken);
  };

  const logout = () => {
    setUser(null);
    setToken(null);
    localStorage.removeItem('@Hemera:user');
    localStorage.removeItem('@Hemera:token');
    window.location.replace('/login');
  };

  if (loading) {
    return <div className="flex items-center justify-center w-screen h-screen bg-[#FAF9FB]">Carregando módulo seguro...</div>;
  }

  return (
    <HemeraContext.Provider value={{ user, token, isAuthenticated: !!token, login, logout }}>
      {children}
    </HemeraContext.Provider>
  );
};

export const useHemera = () => {
  const context = useContext(HemeraContext);
  if (!context) {
    throw new Error('useHemera must be used within a HemeraProvider');
  }
  return context;
};
