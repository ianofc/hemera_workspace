import { useState } from "react";
import { Link } from "react-router-dom";
import AppLayout from "@/components/layout/AppLayout";

const diasSemana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"];
const horarios = ["07:30", "08:20", "09:10", "10:10", "11:00", "13:30", "14:20", "15:10"];

const gradeMock: Record<string, Record<string, { nome: string; alunos: number } | null>> = {
  "07:30": { Segunda: { nome: "Matemática 9A", alunos: 32 }, Terça: null, Quarta: { nome: "Física 8B", alunos: 28 }, Quinta: null, Sexta: { nome: "Matemática 7C", alunos: 35 } },
  "08:20": { Segunda: { nome: "Matemática 9A", alunos: 32 }, Terça: { nome: "Física 9A", alunos: 30 }, Quarta: { nome: "Física 8B", alunos: 28 }, Quinta: { nome: "Lab. Ciências", alunos: 25 }, Sexta: null },
  "09:10": { Segunda: null, Terça: { nome: "Física 9A", alunos: 30 }, Quarta: null, Quinta: { nome: "Lab. Ciências", alunos: 25 }, Sexta: { nome: "Reforço", alunos: 12 } },
  "10:10": { Segunda: { nome: "Matemática 8A", alunos: 34 }, Terça: null, Quarta: { nome: "Matemática 8A", alunos: 34 }, Quinta: null, Sexta: null },
  "11:00": { Segunda: { nome: "Matemática 8A", alunos: 34 }, Terça: null, Quarta: null, Quinta: null, Sexta: null },
  "13:30": { Segunda: null, Terça: { nome: "Física 7A", alunos: 29 }, Quarta: null, Quinta: { nome: "Física 7A", alunos: 29 }, Sexta: null },
  "14:20": { Segunda: null, Terça: { nome: "Física 7A", alunos: 29 }, Quarta: null, Quinta: null, Sexta: null },
  "15:10": { Segunda: null, Terça: null, Quarta: null, Quinta: null, Sexta: null },
};

const ProfessorDashboard = () => {
  const [periodo, setPeriodo] = useState<"manha" | "tarde">("manha");

  const filteredHorarios = horarios.filter((h) => {
    if (periodo === "manha") return h < "12:00";
    return h >= "12:00";
  });

  return (
    <AppLayout role="professor">
      <div className="max-w-[1600px] mx-auto px-4 md:px-8 pb-20 space-y-8">
        {/* Hero */}
        <section className="relative rounded-[2.5rem] overflow-hidden shadow-2xl min-h-[320px] group bg-foreground border border-foreground/80 animate-fade-in-down">
          <div className="absolute inset-0 overflow-hidden">
            <img
              src="https://images.unsplash.com/photo-1524178232363-1fb2b075b655?auto=format&fit=crop&w=1600&q=80"
              className="w-full h-full object-cover transition-transform duration-[5000ms] ease-in-out group-hover:scale-110 opacity-40"
              alt="Sala de Aula"
            />
          </div>
          <div className="absolute inset-0 bg-gradient-aurora-hero" />
          <div className="absolute inset-0 bg-gradient-aurora-overlay" />

          <div className="absolute inset-0 flex items-center px-8 md:px-12 lg:px-16">
            <div className="relative z-10 flex flex-col items-end justify-between w-full gap-8 md:flex-row">
              <div className="max-w-2xl space-y-6">
                <span className="inline-flex items-center gap-2 px-3 py-1.5 text-xs font-bold tracking-wider uppercase border rounded-full shadow-lg bg-card/10 backdrop-blur-md border-card/20 text-primary-foreground/80">
                  Ambiente Docente
                </span>
                <h1 className="text-4xl font-bold leading-tight md:text-5xl lg:text-6xl font-display drop-shadow-xl text-primary-foreground">
                  Olá, <span className="text-gradient-aurora">Professor</span>.
                </h1>

                <div className="flex flex-wrap gap-4 mt-4">
                  {[
                    { icon: "fas fa-layer-group", value: "6", label: "Turmas", colorClass: "bg-primary/20 text-primary-foreground/80" },
                    { icon: "fas fa-user-graduate", value: "187", label: "Alunos", colorClass: "bg-success/20 text-success-foreground/80" },
                    { icon: "fas fa-clock", value: "3", label: "Hoje", colorClass: "bg-warning/20 text-warning-foreground/80" },
                  ].map((stat) => (
                    <div key={stat.label} className="flex items-center gap-3 px-4 py-2 border bg-card/10 backdrop-blur-md rounded-xl border-card/10">
                      <div className={`flex items-center justify-center w-8 h-8 rounded-lg ${stat.colorClass}`}>
                        <i className={stat.icon} />
                      </div>
                      <div>
                        <p className="text-lg font-bold leading-none text-primary-foreground">{stat.value}</p>
                        <p className="text-[10px] uppercase font-bold tracking-wider text-primary-foreground/60">{stat.label}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              <div className="flex flex-wrap gap-3">
                <button className="flex items-center gap-3 px-6 py-3 font-bold transition-all shadow-xl bg-card text-foreground rounded-2xl hover:bg-muted hover:-translate-y-1">
                  <i className="fas fa-plus" /> Nova Turma
                </button>
              </div>
            </div>
          </div>
        </section>

        {/* Grade Horária */}
        <div className="glass-card rounded-[2.5rem] shadow-glass overflow-hidden">
          <div className="flex flex-col items-center justify-between gap-4 p-6 border-b border-primary/10 sm:flex-row">
            <h2 className="flex items-center gap-2 text-xl font-bold text-foreground">
              <span className="w-2 h-6 bg-primary rounded-full" /> Grade Horária
            </h2>
            <div className="flex p-1 bg-muted rounded-xl">
              {(["manha", "tarde"] as const).map((p) => (
                <button
                  key={p}
                  onClick={() => setPeriodo(p)}
                  className={`px-4 py-1.5 rounded-lg text-xs font-bold transition-all ${
                    periodo === p ? "bg-card text-primary shadow-sm" : "text-muted-foreground"
                  }`}
                >
                  {p === "manha" ? "Manhã" : "Tarde"}
                </button>
              ))}
            </div>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full min-w-[800px]">
              <thead>
                <tr className="bg-primary/5">
                  <th className="w-32 px-6 py-4 text-xs font-bold text-left uppercase text-primary/70">Horário</th>
                  {diasSemana.map((dia) => (
                    <th key={dia} className="w-1/5 px-6 py-4 text-xs font-bold text-center uppercase text-primary/70">{dia}</th>
                  ))}
                </tr>
              </thead>
              <tbody className="divide-y divide-muted">
                {filteredHorarios.map((tempo) => (
                  <tr key={tempo} className="transition-colors hover:bg-card/50">
                    <td className="px-6 py-4 text-xs font-bold border-r text-muted-foreground border-muted bg-muted/30">{tempo}</td>
                    {diasSemana.map((dia) => {
                      const item = gradeMock[tempo]?.[dia];
                      return (
                        <td key={dia} className="relative h-24 p-2 align-top border-r border-dashed border-muted last:border-0 group">
                          {item ? (
                            <div className="relative block w-full h-full p-3 transition-all border shadow-sm rounded-2xl border-primary/20 bg-primary/5 hover:bg-primary/10 cursor-pointer">
                              <h4 className="text-sm font-bold truncate text-primary">{item.nome}</h4>
                              <div className="flex items-center gap-2 mt-2 opacity-70">
                                <i className="fas fa-user-graduate text-[10px]" />
                                <span className="text-[10px] font-bold">{item.alunos}</span>
                              </div>
                            </div>
                          ) : (
                            <div className="flex items-center justify-center w-full h-full transition-all border-2 border-transparent opacity-0 cursor-pointer rounded-xl group-hover:opacity-100 hover:bg-muted hover:border-dashed hover:border-muted-foreground/30">
                              <i className="fas fa-plus text-muted-foreground/40" />
                            </div>
                          )}
                        </td>
                      );
                    })}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Bottom row */}
        <div className="grid grid-cols-1 gap-8 lg:grid-cols-3">
          {/* Highlight card */}
          <div className="lg:col-span-2 relative rounded-[2rem] bg-gradient-highlight p-8 text-primary-foreground overflow-hidden shadow-xl flex flex-col justify-center min-h-[260px] group">
            <div className="absolute top-0 right-0 w-80 h-80 translate-x-1/3 -translate-y-1/3 rounded-full bg-card/10 blur-3xl" />
            <div className="relative z-10 max-w-lg">
              <span className="inline-block px-3 py-1 mb-4 text-xs font-bold tracking-wide uppercase border rounded-lg bg-card/20 backdrop-blur-md border-card/20">
                <i className="mr-1 fas fa-lightbulb text-warning" /> Dica Pedagógica
              </span>
              <h3 className="mb-3 text-2xl font-bold md:text-3xl font-display">Planejamento Semanal</h3>
              <p className="mb-6 text-base leading-relaxed opacity-90">
                Organize suas aulas da semana, defina objetivos claros e acompanhe o progresso dos seus alunos em tempo real.
              </p>
              <Link
                to="/professor/planejamento"
                className="inline-flex items-center gap-2 px-6 py-3 font-bold transition-all shadow-lg bg-card text-secondary rounded-xl hover:bg-muted hover:scale-105"
              >
                Planejar Aulas <i className="fas fa-arrow-right text-xs" />
              </Link>
            </div>
            <i className="absolute transition-transform duration-500 opacity-20 fas fa-chalkboard text-[10rem] -right-6 -bottom-8 rotate-12 group-hover:rotate-6 group-hover:scale-110" />
          </div>

          {/* Quick stats */}
          <div className="glass-card rounded-[2rem] shadow-glass p-8 flex flex-col">
            <h4 className="flex items-center gap-3 mb-6 text-xl font-bold text-foreground">
              <div className="flex items-center justify-center w-8 h-8 rounded-lg bg-success/20">
                <i className="text-success fas fa-chart-bar" />
              </div>
              Resumo Rápido
            </h4>
            <div className="space-y-4 flex-1">
              {[
                { label: "Aulas esta semana", value: "18", icon: "fas fa-calendar-check", color: "text-primary" },
                { label: "Atividades pendentes", value: "5", icon: "fas fa-tasks", color: "text-warning" },
                { label: "Avaliações corrigidas", value: "42", icon: "fas fa-check-circle", color: "text-success" },
                { label: "Presença média", value: "94%", icon: "fas fa-user-check", color: "text-secondary" },
              ].map((item) => (
                <div key={item.label} className="flex items-center justify-between p-3 rounded-xl bg-card/60 hover:bg-card transition-colors">
                  <div className="flex items-center gap-3">
                    <i className={`${item.icon} ${item.color} text-sm`} />
                    <span className="text-sm font-medium text-foreground">{item.label}</span>
                  </div>
                  <span className={`text-lg font-bold ${item.color}`}>{item.value}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </AppLayout>
  );
};

export default ProfessorDashboard;
