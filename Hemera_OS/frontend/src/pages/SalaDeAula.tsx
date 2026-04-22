import { useState } from "react";
import { useParams } from "react-router-dom";
import { AppLayout } from "@/components/layout/AppLayout";

const modulosMock = [
  {
    titulo: "Módulo 1 — Introdução",
    conteudos: [
      { id: 1, titulo: "Bem-vindo ao Curso", tipo: "VIDEO" },
      { id: 2, titulo: "Fundamentos Teóricos", tipo: "TEXTO" },
      { id: 3, titulo: "Quiz de Revisão", tipo: "EXERCICIO" },
    ],
  },
  {
    titulo: "Módulo 2 — Aprofundamento",
    conteudos: [
      { id: 4, titulo: "Conceitos Avançados", tipo: "VIDEO" },
      { id: 5, titulo: "Material Complementar", tipo: "TEXTO" },
      { id: 6, titulo: "Prática Guiada", tipo: "EXERCICIO" },
    ],
  },
];

const SalaDeAula = () => {
  const { id } = useParams();
  const [sidebarTab, setSidebarTab] = useState<"aulas" | "conteudos" | "ferramentas">("aulas");
  const [selectedAula, setSelectedAula] = useState(1);
  const [openModules, setOpenModules] = useState<Record<string, boolean>>({ "Módulo 1 — Introdução": true, "Módulo 2 — Aprofundamento": true });

  const currentAula = modulosMock.flatMap((m) => m.conteudos).find((c) => c.id === selectedAula);

  const toggleModule = (titulo: string) => {
    setOpenModules((prev) => ({ ...prev, [titulo]: !prev[titulo] }));
  };

  const getIcon = (tipo: string) => {
    if (tipo === "EXERCICIO") return "fas fa-pencil-alt";
    if (tipo === "TEXTO") return "fas fa-file-alt";
    return "fas fa-play ml-0.5";
  };

  return (
    <AppLayout role="aluno">
      <div className="flex flex-col lg:flex-row h-[calc(100vh-200px)] max-w-[1800px] mx-auto gap-6 px-6 pb-6">
        {/* Main Content Area */}
        <div className="relative flex flex-col flex-1 min-w-0 overflow-hidden border shadow-2xl glass-card rounded-[2.5rem] group transition-all duration-300">
          {currentAula?.tipo === "VIDEO" ? (
            <div className="relative w-full overflow-hidden aspect-video bg-foreground">
              <div className="absolute inset-0 flex flex-col items-center justify-center text-muted-foreground">
                <i className="mb-4 text-6xl fas fa-play-circle text-card/20" />
                <p className="text-primary-foreground/60">Clique para reproduzir o vídeo</p>
              </div>
            </div>
          ) : currentAula?.tipo === "EXERCICIO" ? (
            <div className="flex flex-col w-full h-full p-10 overflow-y-auto bg-muted/30 custom-scrollbar">
              <div className="w-full max-w-3xl mx-auto">
                <span className="px-3 py-1 mb-4 text-xs font-bold rounded-full bg-primary text-primary-foreground inline-block">
                  <i className="mr-1 fas fa-pencil-alt" /> Prática
                </span>
                <h2 className="mb-6 text-3xl font-bold font-display text-foreground">{currentAula.titulo}</h2>

                <div className="p-8 mb-6 bg-card border shadow-sm border-border rounded-3xl">
                  <p className="mb-6 text-lg leading-relaxed text-foreground/80">Responda a questão abaixo:</p>
                  <div className="space-y-3">
                    {["Alternativa A", "Alternativa B", "Alternativa C", "Alternativa D"].map((alt) => (
                      <label
                        key={alt}
                        className="flex items-center gap-4 p-4 transition border cursor-pointer rounded-2xl bg-muted/30 hover:bg-primary/5 border-border hover:border-primary/30 group"
                      >
                        <input type="radio" name="resp" className="w-5 h-5 text-primary border-border focus:ring-primary" />
                        <span className="font-medium text-foreground group-hover:text-primary">{alt}</span>
                      </label>
                    ))}
                  </div>
                </div>
                <div className="flex justify-end">
                  <button className="px-8 py-3 font-bold transition transform shadow-lg bg-primary text-primary-foreground rounded-xl hover:bg-primary/90 hover:-translate-y-1">
                    Enviar
                  </button>
                </div>
              </div>
            </div>
          ) : (
            <>
              <div className="flex items-center justify-center w-full h-64 bg-gradient-to-br from-primary/10 to-secondary/10">
                <div className="text-center">
                  <div className="flex items-center justify-center w-20 h-20 mx-auto mb-4 bg-card shadow-lg rounded-2xl text-primary">
                    <i className="text-4xl fas fa-file-alt" />
                  </div>
                  <h2 className="text-2xl font-bold text-primary font-display">{currentAula?.titulo}</h2>
                </div>
              </div>
              <div className="flex-1 p-8 overflow-y-auto custom-scrollbar">
                <h1 className="text-3xl font-bold leading-tight font-display text-foreground mb-2">
                  {currentAula?.titulo || "Aula"}
                </h1>
                <p className="flex items-center gap-2 mt-1 text-sm text-muted-foreground mb-6">
                  <i className="far fa-clock" /> Módulo de Aprendizado
                </p>
                <div className="leading-relaxed text-foreground/80">
                  <p>Conteúdo da aula será exibido aqui. Este é o material de texto para estudo do aluno, com explicações detalhadas sobre o tema abordado.</p>
                  <br />
                  <p>O professor pode adicionar texto formatado, imagens, links e materiais complementares para enriquecer a experiência de aprendizado.</p>
                </div>
              </div>
            </>
          )}
        </div>

        {/* Sidebar */}
        <div className="w-full lg:w-[400px] flex flex-col glass-card rounded-[2.5rem] shadow-2xl overflow-hidden h-full shrink-0">
          <div className="p-4 border-b bg-muted/40 border-border">
            <div className="flex p-1 rounded-xl bg-muted/50">
              {(
                [
                  { key: "aulas", icon: "fas fa-list-ul", label: "Aulas", activeColor: "text-primary" },
                  { key: "conteudos", icon: "fas fa-folder-open", label: "Conteúdos", activeColor: "text-secondary" },
                  { key: "ferramentas", icon: "fas fa-toolbox", label: "Tools", activeColor: "text-success" },
                ] as const
              ).map((tab) => (
                <button
                  key={tab.key}
                  onClick={() => setSidebarTab(tab.key)}
                  className={`flex items-center justify-center flex-1 gap-2 py-2.5 text-sm font-bold transition-all rounded-lg ${
                    sidebarTab === tab.key
                      ? `bg-card ${tab.activeColor} shadow-sm`
                      : "text-muted-foreground hover:text-foreground"
                  }`}
                >
                  <i className={tab.icon} /> {tab.label}
                </button>
              ))}
            </div>
          </div>

          <div className="flex-1 px-4 py-4 space-y-4 overflow-y-auto custom-scrollbar">
            {sidebarTab === "aulas" && (
              <div className="space-y-3">
                {modulosMock.map((modulo) => (
                  <div key={modulo.titulo} className="overflow-hidden bg-card border shadow-sm border-border rounded-2xl">
                    <button
                      onClick={() => toggleModule(modulo.titulo)}
                      className="flex items-center justify-between w-full p-4 transition bg-muted/30 hover:bg-muted"
                    >
                      <span className="text-xs font-bold tracking-widest uppercase text-muted-foreground">{modulo.titulo}</span>
                      <i className={`text-xs fas fa-chevron-down text-muted-foreground transition-transform ${openModules[modulo.titulo] ? "rotate-180" : ""}`} />
                    </button>

                    {openModules[modulo.titulo] && (
                      <div className="divide-y divide-muted/50">
                        {modulo.conteudos.map((aula) => (
                          <button
                            key={aula.id}
                            onClick={() => setSelectedAula(aula.id)}
                            className={`flex items-center gap-3 p-3 transition border-l-4 hover:bg-primary/5 group w-full text-left ${
                              selectedAula === aula.id
                                ? "border-primary bg-primary/5"
                                : "border-transparent hover:border-primary/30"
                            }`}
                          >
                            <div className="flex items-center justify-center w-8 h-8 bg-card border rounded-full border-border text-[10px] text-muted-foreground group-hover:border-primary/40 group-hover:text-primary shadow-sm">
                              <i className={getIcon(aula.tipo)} />
                            </div>
                            <div className="flex-1 min-w-0">
                              <p className="text-sm font-medium leading-tight text-foreground group-hover:text-primary line-clamp-2">
                                {aula.titulo}
                              </p>
                              <p className="text-[10px] text-muted-foreground mt-0.5 capitalize">{aula.tipo.toLowerCase()}</p>
                            </div>
                          </button>
                        ))}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}

            {sidebarTab === "conteudos" && (
              <div className="flex flex-col items-center justify-center py-12 text-center">
                <i className="fas fa-folder-open text-4xl text-muted-foreground/40 mb-3" />
                <p className="text-sm text-muted-foreground">Materiais complementares aparecerão aqui.</p>
              </div>
            )}

            {sidebarTab === "ferramentas" && (
              <div className="space-y-3">
                {[
                  { icon: "fas fa-robot", label: "Assistente IA", desc: "Tire dúvidas com inteligência artificial" },
                  { icon: "fas fa-calculator", label: "Calculadora", desc: "Calculadora científica integrada" },
                  { icon: "fas fa-sticky-note", label: "Anotações", desc: "Salve suas notas de aula" },
                ].map((tool) => (
                  <button
                    key={tool.label}
                    className="flex items-center gap-4 w-full p-4 transition-all bg-card border border-border rounded-2xl hover:bg-primary/5 hover:border-primary/20 group"
                  >
                    <div className="flex items-center justify-center w-10 h-10 rounded-xl bg-primary/10 text-primary group-hover:bg-primary group-hover:text-primary-foreground transition-colors">
                      <i className={tool.icon} />
                    </div>
                    <div className="text-left">
                      <p className="text-sm font-bold text-foreground">{tool.label}</p>
                      <p className="text-xs text-muted-foreground">{tool.desc}</p>
                    </div>
                  </button>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </AppLayout>
  );
};

export default SalaDeAula;
