import { Outlet } from 'react-router-dom';
import { useLocation } from 'react-router-dom';
import { Sidebar } from './Sidebar';
import { Header } from './Header';

export const MainLayout = () => {
  const location = useLocation();
  const isStudent = location.pathname.startsWith('/student');
  const userType = isStudent ? 'student' : 'teacher';

  return (
    <div className="min-h-screen aurora-bg">
      <Sidebar userType={userType} />
      <div className="ml-72 min-h-screen">
        <Header />
        <main className="p-8 pt-24">
          <Outlet />
        </main>
      </div>
    </div>
  );
};