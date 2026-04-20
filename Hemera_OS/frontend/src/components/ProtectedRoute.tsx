import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useHemera } from '@/contexts/HemeraContext';

interface ProtectedRouteProps {
  children: React.ReactNode;
}

export const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children }) => {
  const { isAuthenticated } = useHemera();
  const location = useLocation();

  if (!isAuthenticated) {
    // Redireciona para login e guarda a página que ele tentou acessar
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  return <>{children}</>;
};
