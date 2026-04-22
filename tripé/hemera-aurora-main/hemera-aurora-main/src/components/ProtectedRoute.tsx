import { Navigate, useLocation } from "react-router-dom";
import { useAuth, AppRole } from "@/hooks/useAuth";
import { HemeraSun } from "./HemeraSun";

interface ProtectedRouteProps {
  children: React.ReactNode;
  requireRole?: AppRole;
}

export const ProtectedRoute = ({ children, requireRole }: ProtectedRouteProps) => {
  const { user, role, loading } = useAuth();
  const location = useLocation();

  if (loading) {
    return (
      <div className="min-h-screen grid place-items-center">
        <HemeraSun size={56} animated />
      </div>
    );
  }

  if (!user) {
    return <Navigate to="/auth/login" replace state={{ from: location.pathname }} />;
  }

  if (requireRole && role && role !== requireRole && role !== "admin") {
    // Wrong role → send to their proper dashboard
    return <Navigate to={role === "professor" ? "/professor" : "/aluno"} replace />;
  }

  return <>{children}</>;
};
