import logo from "@/assets/hemera-logo.png";

const FooterSection = () => (
  <footer className="py-12 bg-secondary text-secondary-foreground/60">
    <div className="container mx-auto px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-4">
      <div className="flex items-center gap-2">
        <img src={logo} alt="Hemera" className="w-6 h-6 opacity-70" />
        <span className="text-sm font-display text-secondary-foreground/80">Hemera</span>
      </div>
      <p className="text-xs">© {new Date().getFullYear()} Hemera — O AVA Escolar Universal</p>
    </div>
  </footer>
);

export default FooterSection;
