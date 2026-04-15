const Footer = () => (
  <footer className="relative z-10 py-10 mt-auto border-t border-border/50 bg-card/40 backdrop-blur-md">
    <div className="max-w-[1600px] mx-auto px-6 flex flex-col md:flex-row justify-between items-center gap-4 opacity-80">
      <div className="flex items-center gap-3">
        <div className="flex items-center justify-center w-8 h-8 rounded-lg bg-foreground text-background">
          <i className="text-xs fas fa-bolt" />
        </div>
        <div>
          <p className="text-xs font-bold text-foreground">© 2025 NioCortex Lumenios.</p>
          <p className="text-[10px] text-muted-foreground">Plataforma de Educação Inteligente.</p>
        </div>
      </div>

      <div className="flex items-center gap-6">
        <a href="#" className="text-xs font-medium transition text-muted-foreground hover:text-primary">Ajuda</a>
        <a href="#" className="text-xs font-medium transition text-muted-foreground hover:text-primary">Privacidade</a>
        <div className="flex gap-3 pl-4 border-l border-border">
          <a href="#" className="transition text-muted-foreground hover:text-accent hover:scale-110"><i className="text-lg fab fa-instagram" /></a>
          <a href="#" className="transition text-muted-foreground hover:text-primary hover:scale-110"><i className="text-lg fab fa-twitter" /></a>
          <a href="#" className="transition text-muted-foreground hover:text-primary hover:scale-110"><i className="text-lg fab fa-linkedin" /></a>
        </div>
      </div>
    </div>
  </footer>
);

export default Footer;
