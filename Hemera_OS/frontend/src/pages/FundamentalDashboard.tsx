import { useState } from "react";
import { motion } from "framer-motion";
import AppLayout from "@/components/layout/AppLayout";
import { Progress } from "@/components/ui/progress";

const alunos = [
  { id: 1, nome: "Lucas Oliveira", matricula: "2026001", turma: "7ºA" },
  { id: 2, nome: "Maria Clara", matricula: "2026002", turma: "7ºA" },
  { id: 3, nome: "Pedro Santos", matricula: "2026003", turma: "7ºA" },
  { id: 4, nome: "Ana Beatriz", matricula: "2026004", turma: "7ºA" },
  { id: 5, nome: "João Victor", matricula: "2026005", turma: "7ºA" },
];

const disciplinas = ["Matemática", "Português", "Ciências", "História", "Geografia"];

const notas: Record<string, Record<string, { b1: number; b2: number; b3: number; b4: number }>> = {
  "Lucas Oliveira": {
    "Matemática": { b1: 8.5, b2: 7.0, b3: 9.0, b4: 0 },
    "Português": { b1: 7.0, b2: 8.0, b3: 7.5, b4: 0 },
    "Ciências": { b1: 9.0, b2: 8.5, b3: 9.5, b4: 0 },
    "História": { b1: 6.5, b2: 7.0, b3: 8.0, b4: 0 },
    "Geografia": { b1: 7.5, b2: 8.0, b3: 7.0, b4: 0 },
  },
  "Maria Clara": {
    "Matemática": { b1: 9.0, b2: 9.5, b3: 10, b4: 0 },
    "Português": { b1: 9.5, b2: 9.0, b3: 9.0, b4: 0 },
    "Ciências": { b1: 8.5, b2: 9.0, b3: 8.0, b4: 0 },
    "História": { b1: 9.0, b2: 8.5, b3: 9.5, b4: 0 },
    "Geografia": { b1: 8.0, b2: 9.0, b3: 8.5, b4: 0 },
  },
  "Pedro Santos": {
    "Matemática": { b1: 5.0, b2: 6.0, b3: 5.5, b4: 0 },
    "Português": { b1: 6.0, b2: 5.5, b3: 6.5, b4: 0 },
    "Ciências": { b1: 7.0, b2: 6.5, b3: 7.0, b4: 0 },
    "História": { b1: 5.5, b2: 6.0, b3: 5.0, b4: 0 },
    "Geografia": { b1: 6.0, b2: 5.5, b3: 6.0, b4: 0 },
  },
  "Ana Beatriz": {
    "Matemática": { b1: 8.0, b2: 7.5, b3: 8.5, b4: 0 },
    "Português": { b1: 9.0, b2: 8.5, b3: 9.0, b4: 0 },
    "Ciências": { b1: 7.5, b2: 8.0, b3: 7.0, b4: 0 },
    "História": { b1: 8.5, b2: 9.0, b3: 8.0, b4: 0 },
    "Geografia": { b1: 7.0, b2: 7.5, b3: 8.0, b4: 0 },
  },
  "João Victor": {
    "Matemática": { b1: 4.0, b2: 5.0, b3: 4.5, b4: 0 },
    "Português": { b1: 5.5, b2: 4.5, b3: 5.0, b4: 0 },
    "Ciências": { b1: 6.0, b2: 5.0, b3: 5.5, b4: 0 },
    "História": { b1: 4.5, b2: 5.0, b3: 4.0, b4: 0 },
    "Geografia": { b1: 5.0, b2: 4.5, b3: 5.5, b4: 0 },
  },
};

const frequencia: Record<string, { presencas: number; faltas: number; total: number }> = {
  "Lucas Oliveira": { presencas: 42, faltas: 3, total: 45 },
  "Maria Clara": { presencas: 44, faltas: 1, total: 45 },
  "Pedro Santos": { presencas: 38, faltas: 7, total: 45 },
  "Ana Beatriz": { presencas: 43, faltas: 2, total: 45 },
  "João Victor": { presencas: 35, faltas: 10, total: 45 },
};

type TabKey = "gradebook" | "chamada" | "frequencia";

const getNotaColor = (nota: number) => {
  if (nota >= 7) return "text-success";
  if (nota >= 5) return "text-warning";
  return "text-destructive";
};

const FundamentalDashboard = () => {
  const [activeTab, setActiveTab] = useState<TabKey>("gradebook");
  const [chamadaHoje, setChamadaHoje] = useState<Record<number, "P" | "F" | null>>(
    Object.fromEntries(alunos.map((a) => [a.id, null]))
  );

  const tabs = [
    { key: "gradebook" as const, icon: "fas fa-table", label: "Gradebook" },
    { key: "chamada" as const, icon: "fas fa-clipboard-check", label: "Chamada" },
    { key: "frequencia" as const, icon: "fas fa-chart-bar", label: "Frequência" },
  ];

  return (
    <AppLayout role="professor">
      <div className="max-w-7xl mx-auto px-6">
        {/* Header */}
        <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }} className="mb-6">
          <div className="flex items-center gap-3 mb-2">
            <div className="flex items-center justify-center w-12 h-12 rounded-2xl bg-gradient-to-br from-[hsl(160,70%,45%)] to-[hsl(190,80%,50%)] text-white shadow-lg">
              <i className="text-xl fas fa-pencil-ruler" />
            </div>
            <div>
              <h1 className="text-3xl font-black font-display text-foreground">Ensino Fundamental</h1>
              <p className="text-sm text-muted-foreground font-medium">Trindade Pedagógica · 7º Ano A</p>
            </div>
          </div>
        </motion.div>

        {/* Tabs */}
        <div className="flex p-1 mb-6 rounded-xl bg-muted/50 glass-card w-fit">
          {tabs.map((tab) => (
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

        {/* Gradebook */}
        {activeTab === "gradebook" && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="glass-card rounded-2xl shadow-float overflow-hidden">
            <div className="overflow-x-auto custom-scrollbar">
              <table className="w-full text-sm">
                <thead>
                  <tr className="bg-muted/40">
                    <th className="px-4 py-3 text-left text-xs font-bold uppercase tracking-wider text-muted-foreground">Aluno</th>
                    {disciplinas.map((d) => (
                      <th key={d} colSpan={4} className="px-2 py-3 text-center text-xs font-bold uppercase tracking-wider text-muted-foreground border-l border-border/50">
                        {d}
                      </th>
                    ))}
                    <th className="px-4 py-3 text-center text-xs font-bold uppercase tracking-wider text-muted-foreground border-l border-border/50">Média</th>
                  </tr>
                  <tr className="bg-muted/20">
                    <th className="px-4 py-2" />
                    {disciplinas.map((d) => (
                      ["B1", "B2", "B3", "B4"].map((b, i) => (
                        <th key={`${d}-${b}`} className={`px-2 py-2 text-center text-[10px] font-bold text-muted-foreground ${i === 0 ? "border-l border-border/50" : ""}`}>
                          {b}
                        </th>
                      ))
                    ))}
                    <th className="px-4 py-2 border-l border-border/50" />
                  </tr>
                </thead>
                <tbody className="divide-y divide-border/30">
                  {alunos.map((aluno) => {
                    const alunoNotas = notas[aluno.nome];
                    const allNotas = Object.values(alunoNotas).flatMap((d) => [d.b1, d.b2, d.b3].filter(Boolean));
                    const media = allNotas.reduce((s, n) => s + n, 0) / allNotas.length;
                    return (
                      <tr key={aluno.id} className="hover:bg-primary/5 transition">
                        <td className="px-4 py-3">
                          <div className="flex items-center gap-3">
                            <img
                              src={`https://ui-avatars.com/api/?name=${aluno.nome.split(" ").map(n => n[0]).join("")}&background=10b981&color=fff&size=32&rounded=true`}
                              alt={aluno.nome}
                              className="w-8 h-8 rounded-full"
                            />
                            <div>
                              <p className="font-bold text-foreground">{aluno.nome}</p>
                              <p className="text-[10px] text-muted-foreground">{aluno.matricula}</p>
                            </div>
                          </div>
                        </td>
                        {disciplinas.map((disc) => {
                          const n = alunoNotas[disc];
                          return [n.b1, n.b2, n.b3, n.b4].map((val, i) => (
                            <td key={`${disc}-${i}`} className={`px-2 py-3 text-center font-bold ${i === 0 ? "border-l border-border/30" : ""} ${val === 0 ? "text-muted-foreground/30" : getNotaColor(val)}`}>
                              {val === 0 ? "—" : val.toFixed(1)}
                            </td>
                          ));
                        })}
                        <td className={`px-4 py-3 text-center font-black text-lg border-l border-border/30 ${getNotaColor(media)}`}>
                          {media.toFixed(1)}
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </motion.div>
        )}

        {/* Chamada */}
        {activeTab === "chamada" && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="glass-card rounded-2xl p-6 shadow-float">
            <div className="flex items-center justify-between mb-6">
              <div>
                <h3 className="text-lg font-bold font-display text-foreground">Chamada do Dia</h3>
                <p className="text-sm text-muted-foreground"><i className="far fa-calendar mr-1" /> 15 de Abril, 2026 — Terça-feira</p>
              </div>
              <span className="px-3 py-1 text-xs font-bold rounded-full bg-warning/10 text-warning">
                <i className="fas fa-clock mr-1" /> Em andamento
              </span>
            </div>

            <div className="space-y-3">
              {alunos.map((aluno) => (
                <div key={aluno.id} className="flex items-center gap-4 p-4 rounded-2xl bg-muted/20 border border-border/30 hover:border-border transition">
                  <img
                    src={`https://ui-avatars.com/api/?name=${aluno.nome.split(" ").map(n => n[0]).join("")}&background=10b981&color=fff&size=40&rounded=true`}
                    alt={aluno.nome}
                    className="w-10 h-10 rounded-full"
                  />
                  <div className="flex-1">
                    <p className="font-bold text-foreground">{aluno.nome}</p>
                    <p className="text-xs text-muted-foreground">{aluno.matricula} · {aluno.turma}</p>
                  </div>
                  <div className="flex gap-2">
                    <button
                      onClick={() => setChamadaHoje((prev) => ({ ...prev, [aluno.id]: "P" }))}
                      className={`w-12 h-12 rounded-xl text-sm font-black transition-all ${
                        chamadaHoje[aluno.id] === "P"
                          ? "bg-success text-success-foreground shadow-lg scale-105"
                          : "bg-muted/30 text-muted-foreground hover:bg-success/10 hover:text-success border border-border"
                      }`}
                    >
                      P
                    </button>
                    <button
                      onClick={() => setChamadaHoje((prev) => ({ ...prev, [aluno.id]: "F" }))}
                      className={`w-12 h-12 rounded-xl text-sm font-black transition-all ${
                        chamadaHoje[aluno.id] === "F"
                          ? "bg-destructive text-destructive-foreground shadow-lg scale-105"
                          : "bg-muted/30 text-muted-foreground hover:bg-destructive/10 hover:text-destructive border border-border"
                      }`}
                    >
                      F
                    </button>
                  </div>
                </div>
              ))}
            </div>

            <div className="flex justify-between items-center mt-6 pt-4 border-t border-border/30">
              <p className="text-sm text-muted-foreground">
                <span className="font-bold text-success">{Object.values(chamadaHoje).filter((v) => v === "P").length}</span> presentes ·{" "}
                <span className="font-bold text-destructive">{Object.values(chamadaHoje).filter((v) => v === "F").length}</span> faltas ·{" "}
                <span className="font-bold">{Object.values(chamadaHoje).filter((v) => v === null).length}</span> pendentes
              </p>
              <button className="px-6 py-3 text-sm font-bold bg-primary text-primary-foreground rounded-xl shadow-lg hover:bg-primary/90 hover:-translate-y-0.5 transition-all">
                <i className="fas fa-save mr-2" /> Salvar Chamada
              </button>
            </div>
          </motion.div>
        )}

        {/* Frequência */}
        {activeTab === "frequencia" && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-4">
            {alunos.map((aluno) => {
              const freq = frequencia[aluno.nome];
              const pct = Math.round((freq.presencas / freq.total) * 100);
              const isAlert = pct < 80;
              return (
                <div key={aluno.id} className="glass-card rounded-2xl p-5 shadow-sm hover:shadow-float transition-shadow">
                  <div className="flex items-center gap-4">
                    <img
                      src={`https://ui-avatars.com/api/?name=${aluno.nome.split(" ").map(n => n[0]).join("")}&background=10b981&color=fff&size=40&rounded=true`}
                      alt={aluno.nome}
                      className="w-10 h-10 rounded-full"
                    />
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 mb-1">
                        <p className="font-bold text-foreground">{aluno.nome}</p>
                        {isAlert && (
                          <span className="px-2 py-0.5 text-[10px] font-bold rounded-full bg-destructive/10 text-destructive">
                            <i className="fas fa-exclamation-triangle mr-1" /> Atenção
                          </span>
                        )}
                      </div>
                      <Progress value={pct} className="h-2.5 rounded-full" />
                      <div className="flex justify-between mt-1.5">
                        <span className="text-xs text-muted-foreground">
                          <span className="font-bold text-success">{freq.presencas}</span> presenças · <span className="font-bold text-destructive">{freq.faltas}</span> faltas
                        </span>
                        <span className={`text-xs font-black ${isAlert ? "text-destructive" : "text-success"}`}>{pct}%</span>
                      </div>
                    </div>
                  </div>
                </div>
              );
            })}
          </motion.div>
        )}
      </div>
    </AppLayout>
  );
};

export default FundamentalDashboard;
