import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";
import logo from "@/assets/hemera-logo.png";

const LandingNav = () => (
  <nav className="absolute top-0 left-0 right-0 z-20 py-4">
    <div className="container mx-auto px-6 lg:px-8 flex items-center justify-between">
      <Link to="/" className="flex items-center gap-2">
        <img src={logo} alt="Hemera" className="w-8 h-8" />
        <span className="font-display text-xl text-secondary-foreground">Hemera</span>
      </Link>

      <div className="hidden md:flex items-center gap-8 text-sm text-secondary-foreground/70">
        <a href="#funcionalidades" className="hover:text-secondary-foreground transition-colors">Funcionalidades</a>
        <a href="#segmentos" className="hover:text-secondary-foreground transition-colors">Segmentos</a>
      </div>

      <Button asChild variant="hemera" size="sm">
        <Link to="/auth">Entrar</Link>
      </Button>
    </div>
  </nav>
);

export default LandingNav;
