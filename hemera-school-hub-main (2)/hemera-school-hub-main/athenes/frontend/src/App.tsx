import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from 'react-query';
import { AnimatePresence } from 'framer-motion';

import { MainLayout } from './components/layout/MainLayout';
import { AuthLayout } from './components/layout/AuthLayout';

import { Login } from './pages/auth/Login';
import { StudentDashboard } from './pages/student/Dashboard';
import { TeacherDashboard } from './pages/teacher/Dashboard';
import { Library } from './pages/shared/Library';
import { VideoPlayer } from './pages/shared/VideoPlayer';
import { Materials } from './pages/shared/Materials';
import { Courses } from './pages/shared/Courses';
import { ZeusAI } from './pages/shared/ZeusAI';

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <AnimatePresence mode="wait">
          <Routes>
            <Route element={<AuthLayout />}>
              <Route path="/login" element={<Login />} />
            </Route>

            <Route element={<MainLayout />}>
              <Route path="/student" element={<StudentDashboard />} />
              <Route path="/student/courses" element={<Courses view="student" />} />
              <Route path="/student/library" element={<Library view="student" />} />
              <Route path="/student/materials" element={<Materials view="student" />} />
              <Route path="/student/watch/:lessonId" element={<VideoPlayer />} />
              <Route path="/student/zeus" element={<ZeusAI />} />

              <Route path="/teacher" element={<TeacherDashboard />} />
              <Route path="/teacher/courses" element={<Courses view="teacher" />} />
              <Route path="/teacher/library" element={<Library view="teacher" />} />
              <Route path="/teacher/materials" element={<Materials view="teacher" />} />
              <Route path="/teacher/upload" element={<VideoPlayer mode="upload" />} />
            </Route>

            <Route path="/" element={<Navigate to="/login" replace />} />
          </Routes>
        </AnimatePresence>
      </Router>
    </QueryClientProvider>
  );
}

export default App