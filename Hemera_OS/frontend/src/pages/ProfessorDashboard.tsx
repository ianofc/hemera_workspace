import React, { useState } from "react";
import { Link } from "react-router-dom";
import { AppLayout } from "../components/layout/AppLayout"; // Caminho relativo para não quebrar o Vite
import { Layers, Users, Clock, Plus, Brain, Zap, Printer, MonitorUp, Lightbulb, ArrowRight, BarChart3, CalendarCheck, CheckCircle2, UserCheck, CalendarDays } from "lucide-react"; // Importação dos ícones reais da nossa obra

const diasSemana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"];
const horarios = ["07:30", "08:20", "09:10", "10:10", "11:00", "13:30", "14:20", "15:10"];

// Lógica local preservada do Cortex Educ
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
    <AppLayout>
      <div className="max-w-[1600px] mx-auto px-4 md:px-8 pb-20 space-y-8">
        
        {/* Hero */}
        <section className="relative rounded-[2.5rem] overflow-hidden shadow-2xl min-h-[320px] group border border-glass-border">
          <div className="absolute inset-0 bg-gradient-to-r from-primary to-secondary opacity-90" />
          
          <div className="absolute inset-0 flex items-center px-8 md:px-12 lg:px-16">
            <div className="relative z-10 flex flex-col items-end justify-between w-full gap-8 md:flex-row">
              <div className="max-w-2xl space-y-6">
                <span className="inline-flex items-center gap-2 px-3 py-1.5 text-xs font-bold tracking-wider uppercase border rounded-full shadow-lg bg-white/20 backdrop-blur-md border-white/20 text-white">
                  Ambiente Docente
                </span>
                <h1 className="text-4xl font-bold leading-tight md:text-5xl lg:text-6xl text-white">
                  Olá, <span className="text-yellow-300">Professor</span>.
                </h1>

                <div className="flex flex-wrap gap-4 mt-4">
                  {[
                    { icon: Layers, value: "6", label: "Turmas", colorClass: "bg-white/20 text-white" },
                    { icon: Users, value: "187", label: "Alunos", colorClass: "bg-white/20 text-white" },
                    { icon: Clock, value: "3", label: "Hoje", colorClass: "bg-white/20 text-white" },
                  ].map((stat) => (
                    <div key={stat.label} className="flex items-center gap-3 px-4 py-2 border bg-white/10 backdrop-blur-md rounded-xl border-white/20">
                      <div className={`flex items-center justify-center w-8 h-8 rounded-lg ${stat.colorClass}`}>
                        <stat.icon className="w-5 h-5" />
                      </div>
                      <div>
                        <p className="text-lg font-bold leading-none text-white">{stat.value}</p>
                        <p className="text-[10px] uppercase font-bold tracking-wider text-white/80">{stat.label}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              <div className="flex flex-wrap gap-3">
                <button className="flex items-center gap-3 px-6 py-3 font-bold transition-all shadow-xl bg-white text-primary rounded-2xl hover:bg-gray-50 hover:-translate-y-1">
                  <Plus className="w-5 h-5" /> Nova Turma
                </button>
              </div>
            </div>
          </div>
        </section>

        {/* ZIOS Proactive Alert Card */}
        <div className="relative overflow-hidden bg-white/60 backdrop-blur-xl rounded-[2rem] shadow-xl p-8 border border-glass-border transform transition-all hover:scale-[1.01]">
          <div className="absolute top-0 right-0 w-64 h-64 rounded-full bg-primary/10 blur-3xl -translate-y-1/2 translate-x-1/4 animate-pulse" />
          
          <div className="relative z-10 flex flex-col items-start gap-6 md:flex-row md:items-center">
            <div className="flex items-center justify-center shadow-inner w-14 h-14 rounded-2xl bg-gradient-to-br from-primary to-secondary text-white">
              <Brain className="w-8 h-8 animate-pulse" />
            </div>
            
            <div className="flex-1">
              <h3 className="flex items-center gap-3 text-xl font-bold text-gray-800">
                PentaIA
                <span className="flex items-center gap-1 px-2.5 py-0.5 rounded-full bg-primary/10 text-primary text-[10px] uppercase tracking-wider font-bold border border-primary/20">
                  <Zap className="w-3 h-3" /> ZIOS Ativo
                </span>
              </h3>
              <p className="mt-2 leading-relaxed text-gray-600">
                Bom dia, Professor. Identifiquei que você tem <strong className="text-gray-800">3 aulas hoje</strong>. 
                O material de revisão de <span className="text-primary font-bold">Matemática (9º Ano)</span> e <span className="text-secondary font-bold">Física (8º Ano)</span> já foi gerado na sua Oficina com base nas dificuldades do último teste.
              </p>
              
              <div className="flex flex-wrap gap-3 mt-5">
                <button className="flex items-center px-5 py-2.5 bg-primary text-white text-sm font-bold rounded-xl shadow-lg hover:bg-primary/90 transition-all">
                  <Printer className="w-4 h-4 mr-2" /> Imprimir Guiões
                </button>
                <button className="flex items-center px-5 py-2.5 bg-white text-gray-800 border border-gray-200 text-sm font-bold rounded-xl hover:bg-gray-50 transition-all">
                  <MonitorUp className="w-4 h-4 mr-2" /> Enviar para Lousa Digital
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Grade Horária */}
        <div className="bg-white/60 backdrop-blur-xl rounded-[2.5rem] shadow-xl overflow-hidden border border-glass-border">
          <div className="flex flex-col items-center justify-between gap-4 p-6 border-b border-gray-100 sm:flex-row">
            <h2 className="flex items-center gap-2 text-xl font-bold text-gray-800">
              <span className="w-2 h-6 bg-primary rounded-full" /> Grade Horária
            </h2>
            <div className="flex p-1 bg-gray-100 rounded-xl">
              {(["manha", "tarde"] as const).map((p) => (
                <button
                  key={p}
                  onClick={() => setPeriodo(p)}
                  className={`px-4 py-1.5 rounded-lg text-xs font-bold transition-all ${
                    periodo === p ? "bg-white text-primary shadow-sm" : "text-gray-500"
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
                <tr className="bg-gray-50/50">
                  <th className="w-32 px-6 py-4 text-xs font-bold text-left uppercase text-gray-500">Horário</th>
                  {diasSemana.map((dia) => (
                    <th key={dia} className="w-1/5 px-6 py-4 text-xs font-bold text-center uppercase text-gray-500">{dia}</th>
                  ))}
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {filteredHorarios.map((tempo) => (
                  <tr key={tempo} className="transition-colors hover:bg-gray-50/50">
                    <td className="px-6 py-4 text-xs font-bold border-r text-gray-500 border-gray-100 bg-gray-50/50">{tempo}</td>
                    {diasSemana.map((dia) => {
                      const item = gradeMock[tempo]?.[dia];
                      return (
                        <td key={dia} className="relative h-24 p-2 align-top border-r border-dashed border-gray-200 last:border-0 group">
                          {item ? (
                            <div className="relative block w-full h-full p-3 transition-all border shadow-sm rounded-2xl border-primary/20 bg-primary/5 hover:bg-primary/10 cursor-pointer">
                              <h4 className="text-sm font-bold truncate text-primary">{item.nome}</h4>
                              <div className="flex items-center gap-2 mt-2 opacity-70">
                                <Users className="w-3 h-3 text-gray-500" />
                                <span className="text-[10px] font-bold text-gray-600">{item.alunos}</span>
                              </div>
                            </div>
                          ) : (
                            <div className="flex items-center justify-center w-full h-full transition-all border-2 border-transparent opacity-0 cursor-pointer rounded-xl group-hover:opacity-100 hover:bg-gray-50 hover:border-dashed hover:border-gray-200">
                              <Plus className="w-4 h-4 text-gray-300" />
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
          <div className="lg:col-span-2 relative rounded-[2rem] bg-gradient-to-r from-primary to-secondary p-8 text-white overflow-hidden shadow-xl flex flex-col justify-center min-h-[260px]">
            <div className="relative z-10 max-w-lg">
              <span className="inline-flex items-center gap-1 px-3 py-1 mb-4 text-xs font-bold tracking-wide uppercase border rounded-lg bg-white/20 backdrop-blur-md border-white/20">
                <Lightbulb className="w-3 h-3 text-yellow-300" /> Dica Pedagógica
              </span>
              <h3 className="mb-3 text-2xl font-bold md:text-3xl">Planejamento Semanal</h3>
              <p className="mb-6 text-base leading-relaxed opacity-90">
                Organize suas aulas da semana, defina objetivos claros e acompanhe o progresso dos seus alunos em tempo real.
              </p>
              <Link
                to="/professor/planejamento"
                className="inline-flex items-center gap-2 px-6 py-3 font-bold transition-all shadow-lg bg-white text-primary rounded-xl hover:bg-gray-50 hover:scale-105"
              >
                Planejar Aulas <ArrowRight className="w-4 h-4" />
              </Link>
            </div>
          </div>

          {/* Quick stats */}
          <div className="bg-white/60 backdrop-blur-xl rounded-[2rem] shadow-xl p-8 border border-glass-border flex flex-col">
            <h4 className="flex items-center gap-3 mb-6 text-xl font-bold text-gray-800">
              <div className="flex items-center justify-center w-8 h-8 rounded-lg bg-success/20">
                <BarChart3 className="w-5 h-5 text-emerald-500" />
              </div>
              Resumo Rápido
            </h4>
            <div className="space-y-4 flex-1">
              {[
                { label: "Aulas esta semana", value: "18", icon: CalendarCheck, color: "text-primary" },
                { label: "Atividades pendentes", value: "5", icon: CalendarDays, color: "text-amber-500" },
                { label: "Avaliações corrigidas", value: "42", icon: CheckCircle2, color: "text-emerald-500" },
                { label: "Presença média", value: "94%", icon: UserCheck, color: "text-secondary" },
              ].map((item) => (
                <div key={item.label} className="flex items-center justify-between p-3 rounded-xl bg-white hover:bg-gray-50 transition-colors shadow-sm">
                  <div className="flex items-center gap-3">
                    <item.icon className={`w-4 h-4 ${item.color}`} />
                    <span className="text-sm font-medium text-gray-600">{item.label}</span>
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