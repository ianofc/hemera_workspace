import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { AuroraBackground, HemeraHeader } from "@/components/HemeraChrome";
import { HemeraSun } from "@/components/HemeraSun";
import { GraduationCap, BookOpen, Sparkles, Shield, Library, ChartPie } from "lucide-react";

const features = [
  { icon: GraduationCap, title: "Regência do Professor", desc: "Diário, notas, frequência, BNCC e DCRB num só lugar." },
  { icon: BookOpen, title: "Vivência do Aluno", desc: "Disciplinas, atividades e cursos AVA num fluxo Udemy-like." },
  { icon: Sparkles, title: "PentaIA integrada", desc: "ZIOS, TAS, IRIS, Mercúrio e Heimdall sob a mesma alma." },
  { icon: Library, title: "Biblioteca inteligente", desc: "APIs públicas + resumos automáticos pelo ZIOS." },
  { icon: ChartPie, title: "Dashboards evolutivos", desc: "Da creche à graduação — a interface se adapta à idade." },
  { icon: Shield, title: "Heimdall · privacidade", desc: "Mascaramento AES-256 antes de qualquer chamada à IA." },
];

const Index = () => {
  return (
    <div className="min-h-screen relative">
      <AuroraBackground />
      <HemeraHeader>
        <nav className="hidden md:flex items-center gap-6 text-sm text-muted-foreground">
          <a href="#features" className="hover:text-primary transition-colors">Diferenciais</a>
          <a href="#pentaia" className="hover:text-primary transition-colors">PentaIA</a>
          <Link to="/auth/login"><Button variant="outline" className="border-primary/30">Acessar</Button></Link>
        </nav>
      </HemeraHeader>

      {/* Hero */}
      <section className="px-6 pt-12 pb-24 max-w-6xl mx-auto grid md:grid-cols-2 gap-12 items-center">
        <div className="animate-fade-in">
          <span className="inline-flex items-center gap-2 text-xs uppercase tracking-[0.25em] text-primary/80 mb-6">
            <span className="w-8 h-px bg-primary/40" /> Sistema operacional educacional
          </span>
          <h1 className="font-display text-5xl md:text-7xl leading-[1.05] text-foreground mb-6">
            A <span className="text-gradient-sun">aurora</span> da<br/>educação fim-a-fim.
          </h1>
          <p className="text-lg text-muted-foreground mb-8 max-w-lg">
            Hemera OS substitui cadernetas, painéis estáticos e diários arcaicos por um
            ecossistema imersivo — com a PentaIA pulsando no centro de tudo.
          </p>
          <div className="flex flex-wrap gap-3">
            <Link to="/auth/login">
              <Button size="lg" className="bg-primary hover:bg-primary/90 shadow-[var(--shadow-elegant)] gap-2">
                Entrar no Hemera <span aria-hidden>→</span>
              </Button>
            </Link>
            <Link to="/professor">
              <Button size="lg" variant="outline" className="border-primary/30">Ver demo professor</Button>
            </Link>
          </div>

          <div className="flex items-center gap-6 mt-12 text-xs text-muted-foreground">
            <div><div className="font-display text-2xl text-primary">+500</div>escolas</div>
            <div className="w-px h-8 bg-border" />
            <div><div className="font-display text-2xl text-primary">98%</div>aprovação MEC</div>
            <div className="w-px h-8 bg-border" />
            <div><div className="font-display text-2xl text-primary">24/7</div>PentaIA ativa</div>
          </div>
        </div>

        <div className="relative animate-scale-in">
          <div className="glass-strong rounded-[2rem] p-10 grid place-items-center aspect-square">
            <HemeraSun size={280} />
          </div>
          <div className="absolute -bottom-6 -left-6 glass rounded-2xl px-4 py-3 text-xs">
            <div className="text-muted-foreground">ZIOS sugere</div>
            <div className="font-medium">Reforço de Geografia · 3º ano</div>
          </div>
          <div className="absolute -top-4 -right-4 glass rounded-2xl px-4 py-3 text-xs">
            <div className="text-muted-foreground">Heimdall</div>
            <div className="font-medium text-primary">● Privacidade ativa</div>
          </div>
        </div>
      </section>

      {/* Features */}
      <section id="features" className="px-6 pb-24 max-w-6xl mx-auto">
        <h2 className="font-display text-4xl md:text-5xl text-center mb-3">Tudo que sua escola precisa</h2>
        <p className="text-center text-muted-foreground mb-12">Da creche à graduação — uma única identidade evolutiva.</p>
        <div className="grid md:grid-cols-3 gap-5">
          {features.map((f) => (
            <div key={f.title} className="glass rounded-2xl p-6 hover:-translate-y-1 transition-transform duration-500">
              <div className="w-11 h-11 rounded-xl bg-primary/10 grid place-items-center text-primary mb-4">
                <f.icon className="h-5 w-5" />
              </div>
              <h3 className="font-display text-2xl mb-1">{f.title}</h3>
              <p className="text-sm text-muted-foreground">{f.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* PentaIA */}
      <section id="pentaia" className="px-6 pb-24 max-w-6xl mx-auto">
        <div className="glass-strong rounded-3xl p-10 md:p-14 text-center relative overflow-hidden">
          <HemeraSun size={120} className="mx-auto mb-6" />
          <h2 className="font-display text-4xl md:text-5xl mb-4">A PentaIA pulsa no Hemera</h2>
          <p className="text-muted-foreground max-w-2xl mx-auto mb-8">
            ZIOS pensa. TAS recomenda. IRIS observa. Mercúrio entrega. Heimdall protege.
            Cinco agentes, uma única alma pedagógica.
          </p>
          <Link to="/auth/login">
            <Button size="lg" className="bg-primary hover:bg-primary/90">Começar agora</Button>
          </Link>
        </div>
      </section>

      <footer className="px-6 py-10 text-center text-xs text-muted-foreground">
        © 2026 Hemera OS · Feito com <span className="text-primary">aurora</span>.
      </footer>
    </div>
  );
};

export default Index;
