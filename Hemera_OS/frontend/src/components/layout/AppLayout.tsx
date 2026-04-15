import { ReactNode } from "react";
import Navbar from "./Navbar";
import Footer from "./Footer";
import AuroraBackground from "./AuroraBackground";

interface AppLayoutProps {
  children: ReactNode;
  role: "aluno" | "professor";
}

const AppLayout = ({ children, role }: AppLayoutProps) => (
  <div className="relative flex flex-col min-h-screen overflow-x-hidden selection:bg-primary selection:text-primary-foreground">
    <AuroraBackground />
    <Navbar role={role} />
    <div className="relative z-10 flex-grow pt-6 pb-10">
      {children}
    </div>
    <Footer />
  </div>
);

export default AppLayout;
