import { useState } from "react";
import { motion } from "framer-motion";
import { AppLayout } from "@/components/layout/AppLayout";

const crianças = [
  { id: 1, nome: "Helena S.", avatar: "Helena", idade: "2 anos", turma: "Turma Girassol" },
  { id: 2, nome: "Miguel A.", avatar: "Miguel", idade: "1 ano", turma: "Turma Girassol" },
  { id: 3, nome: "Alice R.", avatar: "Alice", idade: "3 anos", turma: "Turma Estrela" },
  { id: 4, nome: "Arthur L.", avatar: "Arthur", idade: "2 anos", turma: "Turma Estrela" },
];

const registrosHoje = [
  { id: 1, crianca: "Helena S.", tipo: "alimentacao", hora: "08:30", desc: "Café da manhã — comeu bem (frutas e mingau)" },
  { id: 2, crianca: "Miguel A.", tipo: "sono", hora: "09:15", desc: "Dormiu por 1h30 — sono tranquilo" },
  { id: 3, crianca: "Alice R.", tipo: "atividade", hora: "10:00", desc: "Pintura com tinta guache — muito participativa" },
  { id: 4, crianca: "Helena S.", tipo: "recado", hora: "11:00", desc: "Mãe ligou pedindo troca de roupa extra" },
  { id: 5, crianca: "Arthur L.", tipo: "alimentacao", hora: "11:30", desc: "Almoço — comeu metade do prato, rejeitou legumes" },
  { id: 6, crianca: "Miguel A.", tipo: "saude", hora: "13:00", desc: "Temperatura normal, sem sinais de febre" },
];

const tipoConfig: Record<string, { icon: string; color: string; label: string }> = {
  alimentacao: { icon: "fas fa-utensils", color: "text-[hsl(25,90%,55%)]", label: "Alimentação" },
  sono: { icon: "fas fa-moon", color: "text-[hsl(250,70%,65%)]", label: "Sono" },
  atividade: { icon: "fas fa-palette", color: "text-[hsl(160,70%,45%)]", label: "Atividade" },
  recado: { icon: "fas fa-comment-dots", color: "text-primary", label: "Recado" },
  saude: { icon: "fas fa-heartbeat", color: "text-[hsl(0,70%,55%)]", label: "Saúde" },
};

const fadeUp = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0, transition: { duration: 0.4 } },
};

const CrecheDashboard = () => {
  const [selectedChild, setSelectedChild] = useState<number | null>(null);
  const [activeTab, setActiveTab] = useState<"timeline" | "novo">("timeline");

  const filteredRegistros = selectedChild
    ? registrosHoje.filter((r) => r.crianca === crianças.find((c) => c.id === selectedChild)?.nome)
    : registrosHoje;

  return (
    <AppLayout role="aluno">
      <div className="max-w-7xl mx-auto px-6">
        {/* Header */}
        <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }} className="mb-8">
          <div className="flex items-center gap-3 mb-2">
            <div className="flex items-center justify-center w-12 h-12 rounded-2xl bg-gradient-to-br from-[hsl(25,90%,60%)] to-[hsl(45,95%,55%)] text-white shadow-lg">
              <i className="text-xl fas fa-baby" />
            </div>
            <div>
              <h1 className="text-3xl font-black font-display text-foreground">Diário de Bordo</h1>
              <p className="text-sm text-muted-foreground font-medium">Creche · Turma Girassol & Estrela</p>
            </div>
          </div>
        </motion.div>

        <div className="grid gap-6 lg:grid-cols-[280px_1fr]">
          {/* Children Sidebar */}
          <motion.div variants={fadeUp} initial="hidden" animate="show" className="space-y-3">
            <div className="glass-card rounded-2xl p-4 shadow-float">
              <h3 className="text-xs font-bold uppercase tracking-widest text-muted-foreground mb-3">
                <i className="fas fa-child mr-1" /> Crianças
              </h3>
              <div className="space-y-2">
                <button
                  onClick={() => setSelectedChild(null)}
                  className={`w-full flex items-center gap-3 p-3 rounded-xl text-left transition-all text-sm font-bold ${
                    selectedChild === null ? "bg-primary/10 text-primary border border-primary/20" : "hover:bg-muted text-muted-foreground"
                  }`}
                >
                  <i className="fas fa-users w-5" /> Todas
                </button>
                {crianças.map((c) => (
                  <button
                    key={c.id}
                    onClick={() => setSelectedChild(c.id)}
                    className={`w-full flex items-center gap-3 p-3 rounded-xl text-left transition-all ${
                      selectedChild === c.id ? "bg-primary/10 border border-primary/20" : "hover:bg-muted"
                    }`}
                  >
                    <img
                      src={`https://ui-avatars.com/api/?name=${c.avatar}&background=f59e0b&color=fff&size=36&rounded=true`}
                      alt={c.nome}
                      className="w-9 h-9 rounded-full"
                    />
                    <div className="min-w-0">
                      <p className="text-sm font-bold text-foreground truncate">{c.nome}</p>
                      <p className="text-[10px] text-muted-foreground">{c.idade} · {c.turma}</p>
                    </div>
                  </button>
                ))}
              </div>
            </div>

            {/* Quick Stats */}
            <div className="glass-card rounded-2xl p-4 shadow-float">
              <h3 className="text-xs font-bold uppercase tracking-widest text-muted-foreground mb-3">
                <i className="fas fa-chart-pie mr-1" /> Resumo do Dia
              </h3>
              <div className="grid grid-cols-2 gap-2">
                {[
                  { icon: "fas fa-utensils", val: "3", label: "Refeições", bg: "bg-[hsl(25,90%,60%)]/10 text-[hsl(25,90%,55%)]" },
                  { icon: "fas fa-moon", val: "1", label: "Sonecas", bg: "bg-secondary/10 text-secondary" },
                  { icon: "fas fa-palette", val: "1", label: "Atividades", bg: "bg-success/10 text-success" },
                  { icon: "fas fa-comment-dots", val: "1", label: "Recados", bg: "bg-primary/10 text-primary" },
                ].map((s) => (
                  <div key={s.label} className="flex flex-col items-center p-3 rounded-xl bg-muted/30">
                    <div className={`flex items-center justify-center w-8 h-8 rounded-lg ${s.bg} mb-1`}>
                      <i className={`${s.icon} text-xs`} />
                    </div>
                    <span className="text-lg font-black font-display text-foreground">{s.val}</span>
                    <span className="text-[10px] text-muted-foreground font-medium">{s.label}</span>
                  </div>
                ))}
              </div>
            </div>
          </motion.div>

          {/* Main Timeline */}
          <motion.div variants={fadeUp} initial="hidden" animate="show" transition={{ delay: 0.1 }}>
            {/* Tab bar */}
            <div className="flex items-center gap-2 mb-4">
              <div className="flex p-1 rounded-xl bg-muted/50 glass-card">
                {[
                  { key: "timeline" as const, icon: "fas fa-stream", label: "Timeline" },
                  { key: "novo" as const, icon: "fas fa-plus", label: "Novo Registro" },
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
              <div className="flex-1" />
              <span className="text-xs font-bold text-muted-foreground">
                <i className="far fa-calendar mr-1" /> 15 Abr 2026
              </span>
            </div>

            {activeTab === "timeline" ? (
              <div className="space-y-3">
                {filteredRegistros.map((reg, i) => {
                  const cfg = tipoConfig[reg.tipo];
                  return (
                    <motion.div
                      key={reg.id}
                      initial={{ opacity: 0, x: -10 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: i * 0.05 }}
                      className="flex gap-4 p-4 glass-card rounded-2xl shadow-sm hover:shadow-float transition-shadow group"
                    >
                      <div className={`flex items-center justify-center w-10 h-10 rounded-xl bg-card border border-border shadow-sm ${cfg.color} shrink-0`}>
                        <i className={cfg.icon} />
                      </div>
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-2 mb-1">
                          <span className="text-sm font-bold text-foreground">{reg.crianca}</span>
                          <span className={`text-[10px] font-bold uppercase tracking-wider ${cfg.color}`}>{cfg.label}</span>
                        </div>
                        <p className="text-sm text-muted-foreground leading-relaxed">{reg.desc}</p>
                      </div>
                      <span className="text-xs font-bold text-muted-foreground shrink-0">{reg.hora}</span>
                    </motion.div>
                  );
                })}
              </div>
            ) : (
              <div className="glass-card rounded-2xl p-6 shadow-float">
                <h3 className="text-lg font-bold font-display text-foreground mb-4">Novo Registro</h3>
                <div className="space-y-4">
                  <div>
                    <label className="block text-xs font-bold text-muted-foreground mb-1.5">Criança</label>
                    <select className="w-full px-4 py-3 text-sm bg-muted/30 border border-border rounded-xl text-foreground focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none transition">
                      {crianças.map((c) => (
                        <option key={c.id}>{c.nome}</option>
                      ))}
                    </select>
                  </div>
                  <div>
                    <label className="block text-xs font-bold text-muted-foreground mb-1.5">Tipo</label>
                    <div className="flex flex-wrap gap-2">
                      {Object.entries(tipoConfig).map(([key, cfg]) => (
                        <button key={key} className="flex items-center gap-2 px-4 py-2 text-sm font-bold border border-border rounded-xl bg-muted/20 hover:bg-primary/5 hover:border-primary/30 transition text-foreground">
                          <i className={`${cfg.icon} ${cfg.color}`} /> {cfg.label}
                        </button>
                      ))}
                    </div>
                  </div>
                  <div>
                    <label className="block text-xs font-bold text-muted-foreground mb-1.5">Descrição</label>
                    <textarea
                      rows={3}
                      placeholder="Descreva o registro..."
                      className="w-full px-4 py-3 text-sm bg-muted/30 border border-border rounded-xl text-foreground placeholder:text-muted-foreground/50 focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none transition resize-none"
                    />
                  </div>
                  <button className="px-6 py-3 text-sm font-bold bg-gradient-to-r from-[hsl(25,90%,60%)] to-[hsl(45,95%,55%)] text-white rounded-xl shadow-lg hover:shadow-neon hover:-translate-y-0.5 transition-all">
                    <i className="fas fa-paper-plane mr-2" /> Enviar Registro
                  </button>
                </div>
              </div>
            )}
          </motion.div>
        </div>
      </div>
    </AppLayout>
  );
};

export default CrecheDashboard;
