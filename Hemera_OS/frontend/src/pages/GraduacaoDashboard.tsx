import { useState } from "react";
import { motion } from "framer-motion";
import AppLayout from "@/components/layout/AppLayout";
import { Progress } from "@/components/ui/progress";

const trilhas = [
  {
    id: 1,
    titulo: "Engenharia de Software",
    progresso: 68,
    cursos: 12,
    concluidos: 8,
    certificados: 3,
    icon: "fas fa-code",
    cor: "from-primary to-secondary",
  },
  {
    id: 2,
    titulo: "Ciência de Dados",
    progresso: 42,
    cursos: 10,
    concluidos: 4,
    certificados: 1,
    icon: "fas fa-brain",
    cor: "from-secondary to-accent",
  },
  {
    id: 3,
    titulo: "Design UX/UI",
    progresso: 25,
    cursos: 8,
    concluidos: 2,
    certificados: 0,
    icon: "fas fa-palette",
    cor: "from-accent to-[hsl(25,90%,60%)]",
  },
];

const cursosRecentes = [
  { id: 1, titulo: "Algoritmos Avançados", professor: "Dr. Ricardo Lima", progresso: 85, aulas: 24, assistidas: 20, tipo: "Obrigatória" },
  { id: 2, titulo: "Machine Learning Aplicado", professor: "Dra. Camila Torres", progresso: 60, aulas: 18, assistidas: 11, tipo: "Eletiva" },
  { id: 3, titulo: "Banco de Dados NoSQL", professor: "Prof. André Costa", progresso: 30, aulas: 16, assistidas: 5, tipo: "Obrigatória" },
  { id: 4, titulo: "Prototipagem com Figma", professor: "Prof. Julia Mendes", progresso: 100, aulas: 12, assistidas: 12, tipo: "Extra" },
];

const certificados = [
  { id: 1, titulo: "Fundamentos de Python", emissao: "Mar 2026", carga: "40h", badge: "fas fa-medal" },
  { id: 2, titulo: "Introdução ao React", emissao: "Jan 2026", carga: "60h", badge: "fas fa-award" },
  { id: 3, titulo: "SQL para Análise de Dados", emissao: "Nov 2025", carga: "30h", badge: "fas fa-certificate" },
  { id: 4, titulo: "Design Thinking", emissao: "Set 2025", carga: "20h", badge: "fas fa-star" },
];

type TabKey = "trilhas" | "cursos" | "certificados";

const GraduacaoDashboard = () => {
  const [activeTab, setActiveTab] = useState<TabKey>("trilhas");

  // Aura calculation
  const auraAcademica = 72;
  const auraExtra = 45;
  const auraTotal = Math.round((auraAcademica * 0.7 + auraExtra * 0.3));

  return (
    <AppLayout role="aluno">
      <div className="max-w-7xl mx-auto px-6">
        {/* Header + Aura Bar */}
        <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }} className="mb-8">
          <div className="flex flex-col lg:flex-row lg:items-center gap-6">
            <div className="flex items-center gap-3">
              <div className="flex items-center justify-center w-12 h-12 rounded-2xl bg-gradient-to-br from-secondary to-accent text-white shadow-lg">
                <i className="text-xl fas fa-graduation-cap" />
              </div>
              <div>
                <h1 className="text-3xl font-black font-display text-foreground">Graduação</h1>
                <p className="text-sm text-muted-foreground font-medium">Autonomia Acadêmica · Ciência da Computação</p>
              </div>
            </div>

            {/* Aura Card */}
            <div className="lg:ml-auto glass-card rounded-2xl p-4 shadow-float flex items-center gap-5 min-w-[320px]">
              <div className="relative flex items-center justify-center w-16 h-16">
                <svg className="w-16 h-16 -rotate-90" viewBox="0 0 64 64">
                  <circle cx="32" cy="32" r="28" fill="none" stroke="hsl(var(--muted))" strokeWidth="4" />
                  <circle
                    cx="32" cy="32" r="28" fill="none"
                    stroke="url(#aura-grad)" strokeWidth="4" strokeLinecap="round"
                    strokeDasharray={`${auraTotal * 1.76} 176`}
                  />
                  <defs>
                    <linearGradient id="aura-grad" x1="0" y1="0" x2="1" y2="1">
                      <stop offset="0%" stopColor="hsl(var(--secondary))" />
                      <stop offset="100%" stopColor="hsl(var(--accent))" />
                    </linearGradient>
                  </defs>
                </svg>
                <span className="absolute text-lg font-black font-display text-foreground">{auraTotal}</span>
              </div>
              <div className="flex-1">
                <p className="text-xs font-bold uppercase tracking-widest text-muted-foreground mb-1">Aura de Progresso</p>
                <div className="flex items-center gap-3 text-xs">
                  <span className="text-muted-foreground">Acadêmica <span className="font-bold text-primary">{auraAcademica}%</span></span>
                  <span className="text-muted-foreground">Extra <span className="font-bold text-secondary">{auraExtra}%</span></span>
                </div>
                <p className="text-[10px] text-muted-foreground/60 mt-1">Experiência acumulada entre core + AVA</p>
              </div>
            </div>
          </div>
        </motion.div>

        {/* Tabs */}
        <div className="flex p-1 mb-6 rounded-xl bg-muted/50 glass-card w-fit">
          {[
            { key: "trilhas" as const, icon: "fas fa-route", label: "Trilhas" },
            { key: "cursos" as const, icon: "fas fa-play-circle", label: "Meus Cursos" },
            { key: "certificados" as const, icon: "fas fa-certificate", label: "Certificados" },
          ].map((tab) => (
            <button
              key={tab.key}
              onClick={() => setActiveTab(tab.key)}
              className={`flex items-center gap-2 px-5 py-2.5 text-sm font-bold rounded-lg transition-all ${
                activeTab === tab.key ? "bg-card text-primary shadow-sm" : "text-muted-foreground hover:text-foreground"
              }`}
            >
              <i className={tab.icon} /> {tab.label}
            </button>
          ))}
        </div>

        {/* Trilhas / Knowledge Map */}
        {activeTab === "trilhas" && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-6">
            {trilhas.map((trilha, i) => (
              <motion.div
                key={trilha.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.1 }}
                className="glass-card rounded-2xl p-6 shadow-float hover:shadow-neon transition-shadow group cursor-pointer"
              >
                <div className="flex items-start gap-5">
                  <div className={`flex items-center justify-center w-14 h-14 rounded-2xl bg-gradient-to-br ${trilha.cor} text-white shadow-lg shrink-0 group-hover:scale-110 transition-transform`}>
                    <i className={`${trilha.icon} text-xl`} />
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-3 mb-2">
                      <h3 className="text-xl font-bold font-display text-foreground group-hover:text-primary transition-colors">{trilha.titulo}</h3>
                      <span className="px-2.5 py-0.5 text-[10px] font-bold rounded-full bg-muted text-muted-foreground">
                        {trilha.certificados} certificados
                      </span>
                    </div>
                    <Progress value={trilha.progresso} className="h-3 rounded-full mb-2" />
                    <div className="flex items-center gap-4 text-xs text-muted-foreground">
                      <span><span className="font-bold text-foreground">{trilha.concluidos}</span>/{trilha.cursos} cursos</span>
                      <span className="font-bold text-primary">{trilha.progresso}% completo</span>
                    </div>
                  </div>
                  <i className="fas fa-chevron-right text-muted-foreground/30 group-hover:text-primary transition-colors mt-4" />
                </div>
              </motion.div>
            ))}
          </motion.div>
        )}

        {/* Cursos */}
        {activeTab === "cursos" && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="grid gap-4 md:grid-cols-2">
            {cursosRecentes.map((curso, i) => (
              <motion.div
                key={curso.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.08 }}
                className="glass-card rounded-2xl p-5 shadow-sm hover:shadow-float transition-all group cursor-pointer"
              >
                <div className="flex items-center justify-between mb-3">
                  <span className={`px-2.5 py-0.5 text-[10px] font-bold rounded-full ${
                    curso.tipo === "Obrigatória" ? "bg-primary/10 text-primary" :
                    curso.tipo === "Eletiva" ? "bg-secondary/10 text-secondary" :
                    "bg-success/10 text-success"
                  }`}>
                    {curso.tipo}
                  </span>
                  {curso.progresso === 100 && (
                    <span className="text-success text-sm"><i className="fas fa-check-circle" /></span>
                  )}
                </div>
                <h3 className="text-lg font-bold font-display text-foreground group-hover:text-primary transition-colors mb-1">{curso.titulo}</h3>
                <p className="text-xs text-muted-foreground mb-4">{curso.professor}</p>
                <Progress value={curso.progresso} className="h-2 rounded-full mb-2" />
                <div className="flex justify-between text-xs text-muted-foreground">
                  <span>{curso.assistidas}/{curso.aulas} aulas</span>
                  <span className="font-bold text-primary">{curso.progresso}%</span>
                </div>
              </motion.div>
            ))}
          </motion.div>
        )}

        {/* Certificados */}
        {activeTab === "certificados" && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            {certificados.map((cert, i) => (
              <motion.div
                key={cert.id}
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: i * 0.08 }}
                className="glass-card rounded-2xl p-5 shadow-sm hover:shadow-neon transition-all text-center group cursor-pointer"
              >
                <div className="flex items-center justify-center w-16 h-16 mx-auto mb-4 rounded-2xl bg-gradient-to-br from-secondary to-accent text-white shadow-lg group-hover:scale-110 transition-transform">
                  <i className={`${cert.badge} text-2xl`} />
                </div>
                <h3 className="text-sm font-bold font-display text-foreground mb-1 group-hover:text-primary transition-colors">{cert.titulo}</h3>
                <p className="text-[10px] text-muted-foreground mb-2">{cert.carga}</p>
                <span className="text-[10px] font-bold text-muted-foreground/60">{cert.emissao}</span>
              </motion.div>
            ))}
          </motion.div>
        )}
      </div>
    </AppLayout>
  );
};

export default GraduacaoDashboard;
