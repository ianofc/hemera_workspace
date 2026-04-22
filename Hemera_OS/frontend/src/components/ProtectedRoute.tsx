import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

interface ProtectedRouteProps {
  children: React.ReactNode;
  requireRole?: 'professor' | 'aluno';
}

export const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children, requireRole }) => {
  const { user } = useAuth();
  const location = useLocation();

  // Se não estiver logado, chuta para o login
  if (!user) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  // Se a rota exige um papel específico e o usuário não tem, manda para o dashboard dele
  if (requireRole && user.role !== requireRole) {
    return <Navigate to={`/${user.role}`} replace />;
  }

  // Passou na verificação, renderiza a tela envolvida no AppLayout (Aurora Glass)
  return <>{children}</>;
};