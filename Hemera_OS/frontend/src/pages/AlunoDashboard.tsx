import { Link } from "react-router-dom";
import { AppLayout } from "@/components/layout/AppLayout";

const disciplinasMock = [
  { id: 1, titulo: "Matemática Avançada", professor: "Prof. Silva", progresso: 68, imagem: "https://images.unsplash.com/photo-1635070041078-e363dbe005cb?auto=format&fit=crop&w=400&q=80" },
  { id: 2, titulo: "Física Quântica", professor: "Prof. Santos", progresso: 45, imagem: "https://images.unsplash.com/photo-1636466497217-26a8cbeaf0aa?auto=format&fit=crop&w=400&q=80" },
  { id: 3, titulo: "Literatura Brasileira", professor: "Profa. Costa", progresso: 82, imagem: "https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?auto=format&fit=crop&w=400&q=80" },
  { id: 4, titulo: "Biologia Molecular", professor: "Prof. Oliveira", progresso: 30, imagem: "https://images.unsplash.com/photo-1530026405186-ed1f139313f8?auto=format&fit=crop&w=400&q=80" },
];

const AlunoDashboard = () => {
  return (
    <AppLayout role="aluno">
      <div className="max-w-[1600px] mx-auto px-6 space-y-12 pb-20">
        {/* Hero Banner */}
        <section className="relative rounded-[2.5rem] overflow-hidden shadow-2xl h-[380px] group bg-foreground border border-foreground/80">
          <div className="absolute inset-0 overflow-hidden">
            <img
              src="https://images.unsplash.com/photo-1523050854058-8df90110c9f1?auto=format&fit=crop&w=1600&q=80"
              className="w-full h-full object-cover transition-transform duration-[5000ms] ease-in-out group-hover:scale-110 opacity-60"
              alt="Ambiente de Estudos"
            />
          </div>
          <div className="absolute inset-0 bg-gradient-aurora-hero" />
          <div className="absolute inset-0 bg-gradient-aurora-overlay" />

          <div className="absolute inset-0 flex items-center px-8 md:px-16 lg:px-20">
            <div className="relative z-10 max-w-3xl space-y-6">
              <div className="animate-fade-in-up" style={{ animationDelay: "0.1s" }}>
                <span className="inline-flex items-center gap-2 px-3 py-1.5 text-xs font-bold tracking-wider uppercase border rounded-full shadow-lg bg-card/10 backdrop-blur-md border-card/20 text-primary-foreground/80">
                  <span className="relative flex w-2 h-2">
                    <span className="absolute inline-flex w-full h-full rounded-full opacity-75 animate-ping bg-primary" />
                    <span className="relative inline-flex w-2 h-2 rounded-full bg-primary" />
                  </span>
                  Ambiente Escolar Online
                </span>
              </div>

              <div className="animate-fade-in-up" style={{ animationDelay: "0.2s" }}>
                <h1 className="text-5xl font-bold leading-tight md:text-6xl lg:text-7xl font-display drop-shadow-xl text-primary-foreground">
                  Olá, <span className="text-gradient-aurora">Estudante</span>.
                  <br />
                  <span className="text-4xl md:text-5xl opacity-90">Hora de evoluir! 🚀</span>
                </h1>
              </div>

              <div className="animate-fade-in-up" style={{ animationDelay: "0.3s" }}>
                <p className="max-w-xl text-lg font-medium leading-relaxed text-primary-foreground/80 drop-shadow-md">
                  Você tem <strong className="text-primary-foreground border-b-2 border-primary/50 px-1">4 disciplinas</strong> ativas.
                  Sua jornada de conhecimento continua agora.
                </p>
              </div>

              <div className="flex flex-wrap gap-4 pt-4 animate-fade-in-up" style={{ animationDelay: "0.4s" }}>
                <Link
                  to="/disciplinas"
                  className="flex items-center gap-3 px-8 py-4 font-bold transition-all shadow-xl bg-card text-foreground rounded-2xl hover:bg-muted hover:shadow-primary/30 hover:-translate-y-1 group/btn"
                >
                  <div className="flex items-center justify-center w-6 h-6 rounded-full bg-primary text-primary-foreground group-hover/btn:scale-110 transition-transform">
                    <i className="text-xs fas fa-play ml-0.5" />
                  </div>
                  Minhas Aulas
                </Link>
                <Link
                  to="/biblioteca"
                  className="flex items-center gap-3 px-8 py-4 font-bold transition-all border shadow-xl border-card/30 bg-card/10 backdrop-blur-md rounded-2xl hover:bg-card/20 hover:border-card/50 hover:-translate-y-1 text-primary-foreground"
                >
                  <i className="fas fa-book-reader" /> Biblioteca
                </Link>
              </div>
            </div>
          </div>
        </section>

        {/* Highlight + Recent */}
        <section className="grid grid-cols-1 gap-8 lg:grid-cols-3">
          <div className="lg:col-span-2 relative rounded-[2rem] bg-gradient-highlight p-10 text-primary-foreground overflow-hidden shadow-2xl flex flex-col justify-center min-h-[300px] group transition-all hover:shadow-secondary/40">
            <div className="absolute top-0 right-0 w-96 h-96 translate-x-1/3 -translate-y-1/3 rounded-full bg-card/10 blur-3xl group-hover:bg-card/20 transition-all duration-700" />
            <div className="absolute bottom-0 left-0 w-64 h-64 -translate-x-1/3 translate-y-1/3 rounded-full bg-primary/30 blur-3xl" />

            <div className="relative z-10 max-w-lg">
              <span className="inline-block px-3 py-1 mb-4 text-xs font-bold tracking-wide uppercase border rounded-lg bg-card/20 backdrop-blur-md border-card/20">
                <i className="mr-1 fas fa-star text-warning" /> Destaque da Semana
              </span>
              <h3 className="mb-3 text-3xl font-bold md:text-4xl font-display">Feira de Ciências 2025</h3>
              <p className="mb-8 text-lg leading-relaxed opacity-90">
                Prepare seu projeto! Confira o edital oficial, monte sua equipe e inove. O futuro começa na sua imaginação.
              </p>
              <a
                href="https://www.gov.br/mec/pt-br"
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-2 px-6 py-3 font-bold transition-all shadow-lg bg-card text-secondary rounded-xl hover:bg-muted hover:scale-105 hover:shadow-xl"
              >
                Ver Edital Oficial <i className="fas fa-external-link-alt text-xs opacity-50" />
              </a>
            </div>

            <i className="absolute transition-transform duration-500 opacity-20 fas fa-flask text-[12rem] -right-8 -bottom-12 rotate-12 group-hover:rotate-6 group-hover:scale-110" />
          </div>

          {/* Recent Activity */}
          <div className="flex flex-col justify-center p-8 glass-card rounded-[2rem] shadow-glass relative overflow-hidden">
            <div className="absolute top-0 right-0 w-32 h-32 rounded-full bg-primary/10 blur-3xl -mr-16 -mt-16" />

            <h4 className="flex items-center gap-3 mb-6 text-xl font-bold text-foreground">
              <div className="flex items-center justify-center w-8 h-8 rounded-lg bg-warning/20">
                <i className="text-warning fas fa-history" />
              </div>
              Últimas Aulas
            </h4>

            <div className="flex-1 space-y-4 overflow-y-auto max-h-[220px] custom-scrollbar pr-2">
              {disciplinasMock.slice(0, 3).map((mat, i) => (
                <Link
                  key={mat.id}
                  to={`/sala-de-aula/${mat.id}`}
                  className="flex items-center gap-4 p-3 transition-all border border-transparent cursor-pointer rounded-2xl bg-card/60 hover:bg-card hover:border-primary/20 hover:shadow-md group"
                >
                  <div className="flex items-center justify-center w-12 h-12 text-xl rounded-xl bg-gradient-to-br from-primary to-secondary shadow-md group-hover:scale-110 shrink-0 text-primary-foreground transition-transform">
                    <i className={`fas ${i === 0 ? "fa-play" : "fa-book-open"} text-xs`} />
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-bold truncate text-foreground group-hover:text-primary transition-colors">{mat.titulo}</p>
                    <p className="text-xs font-medium truncate text-muted-foreground">Continuar de onde parou</p>
                    <div className="w-full h-1 mt-2 rounded-full overflow-hidden bg-muted">
                      <div className="h-full rounded-full bg-primary" style={{ width: `${mat.progresso}%` }} />
                    </div>
                  </div>
                </Link>
              ))}
            </div>
          </div>
        </section>

        {/* Disciplines Grid */}
        <section>
          <div className="flex items-end justify-between mb-8 px-2">
            <div className="flex items-center gap-4">
              <div className="w-1.5 h-10 bg-gradient-to-b from-primary to-secondary rounded-full shadow-lg shadow-primary/30" />
              <div>
                <h3 className="text-3xl font-display font-bold text-foreground">Minhas Disciplinas</h3>
                <p className="text-sm text-muted-foreground font-medium">Acesse o conteúdo das suas matérias.</p>
              </div>
            </div>
            <Link
              to="/disciplinas"
              className="group flex items-center gap-2 text-sm font-bold text-primary transition-colors hover:text-primary/80 bg-card px-4 py-2 rounded-full shadow-sm hover:shadow-md border border-border"
            >
              Ver grade completa
              <i className="fas fa-arrow-right transition-transform group-hover:translate-x-1" />
            </Link>
          </div>

          <div className="grid grid-cols-1 gap-8 md:grid-cols-2 lg:grid-cols-4">
            {disciplinasMock.map((mat) => (
              <Link
                key={mat.id}
                to={`/sala-de-aula/${mat.id}`}
                className="relative flex flex-col p-4 transition-all duration-300 bg-card border border-card shadow-lg group rounded-[2rem] hover:shadow-2xl hover:-translate-y-2 hover:border-primary/20"
              >
                <div className="relative h-48 mb-4 overflow-hidden rounded-[1.5rem] bg-muted shadow-inner">
                  <img
                    src={mat.imagem}
                    alt={mat.titulo}
                    className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-foreground/60 via-transparent to-transparent" />
                  <div className="absolute bottom-3 left-3 right-3 flex justify-between items-end">
                    <span className="px-2 py-1 text-[10px] font-bold rounded-lg bg-card/90 backdrop-blur-sm text-foreground">
                      {mat.professor}
                    </span>
                  </div>
                </div>

                <div className="px-2 pb-2 flex-1 flex flex-col">
                  <h4 className="text-base font-bold text-foreground group-hover:text-primary transition-colors line-clamp-2 mb-2">
                    {mat.titulo}
                  </h4>

                  <div className="mt-auto">
                    <div className="flex justify-between items-center mb-1">
                      <span className="text-[10px] font-bold text-muted-foreground uppercase tracking-wider">Progresso</span>
                      <span className="text-xs font-bold text-primary">{mat.progresso}%</span>
                    </div>
                    <div className="w-full h-1.5 rounded-full overflow-hidden bg-muted">
                      <div
                        className="h-full rounded-full bg-gradient-to-r from-primary to-secondary transition-all duration-500"
                        style={{ width: `${mat.progresso}%` }}
                      />
                    </div>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        </section>
      </div>
    </AppLayout>
  );
};

export default AlunoDashboard;
