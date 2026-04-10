import { motion } from "framer-motion";
import { useAuth } from "@/hooks/useAuth";
import {
  Users, BookOpen, ClipboardList, BarChart3,
  Calendar, TrendingUp, AlertTriangle, CheckCircle2
} from "lucide-react";

const stats = [
  { label: "Turmas Ativas", value: "6", icon: Users, change: "+2 este semestre" },
  { label: "Alunos Matriculados", value: "187", icon: BookOpen, change: "3 turmas lotadas" },
  { label: "Aulas Planejadas", value: "42", icon: Calendar, change: "87% realizadas" },
  { label: "Avaliações Pendentes", value: "3", icon: ClipboardList, change: "prazo: 5 dias" },
];

const quickActions = [
  { label: "Fazer Chamada", desc: "Registrar frequência da turma", icon: CheckCircle2, color: "bg-hemera-sage/10 text-hemera-sage" },
  { label: "Lançar Notas", desc: "Diário de classe digital", icon: BarChart3, color: "bg-hemera-gold/10 text-hemera-gold" },
  { label: "Alunos em Risco", desc: "4 alunos com baixa frequência", icon: AlertTriangle, color: "bg-hemera-coral/10 text-hemera-coral" },
  { label: "Novo Material", desc: "Publicar conteúdo para turma", icon: TrendingUp, color: "bg-secondary/10 text-secondary" },
];

const item = {
  hidden: { opacity: 0, y: 14, filter: "blur(4px)" },
  show: { opacity: 1, y: 0, filter: "blur(0px)", transition: { duration: 0.5, ease: [0.16, 1, 0.3, 1] } },
};

const DashboardHome = () => {
  const { user } = useAuth();
  const name = user?.user_metadata?.full_name || "Professor(a)";

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      <motion.div
        initial={{ opacity: 0, y: 12, filter: "blur(4px)" }}
        animate={{ opacity: 1, y: 0, filter: "blur(0px)" }}
        transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
      >
        <h1 className="text-2xl font-display text-foreground">
          Bom dia, {name.split(" ")[0]}
        </h1>
        <p className="text-muted-foreground mt-1">Aqui está o resumo da sua escola hoje.</p>
      </motion.div>

      {/* Stats */}
      <motion.div
        initial="hidden"
        animate="show"
        variants={{ show: { transition: { staggerChildren: 0.07 } } }}
        className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4"
      >
        {stats.map((s) => (
          <motion.div key={s.label} variants={item} className="bg-card rounded-lg p-5 hemera-card-shadow">
            <div className="flex items-center justify-between mb-3">
              <span className="text-sm text-muted-foreground">{s.label}</span>
              <s.icon className="w-4 h-4 text-muted-foreground" />
            </div>
            <p className="text-2xl font-semibold tabular-nums text-foreground">{s.value}</p>
            <p className="text-xs text-muted-foreground mt-1">{s.change}</p>
          </motion.div>
        ))}
      </motion.div>

      {/* Quick Actions */}
      <motion.div
        initial="hidden"
        animate="show"
        variants={{ show: { transition: { staggerChildren: 0.07, delayChildren: 0.3 } } }}
      >
        <h2 className="font-sans font-semibold text-foreground mb-4">Ações Rápidas</h2>
        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {quickActions.map((a) => (
            <motion.button
              key={a.label}
              variants={item}
              className="bg-card rounded-lg p-5 hemera-card-shadow text-left group active:scale-[0.97] transition-transform"
            >
              <div className={`w-10 h-10 rounded-md ${a.color} flex items-center justify-center mb-3`}>
                <a.icon className="w-5 h-5" />
              </div>
              <p className="font-medium text-foreground text-sm">{a.label}</p>
              <p className="text-xs text-muted-foreground mt-1">{a.desc}</p>
            </motion.button>
          ))}
        </div>
      </motion.div>

      {/* Recent Activity placeholder */}
      <motion.div
        initial={{ opacity: 0, y: 14, filter: "blur(4px)" }}
        animate={{ opacity: 1, y: 0, filter: "blur(0px)" }}
        transition={{ duration: 0.5, delay: 0.5, ease: [0.16, 1, 0.3, 1] }}
        className="bg-card rounded-lg p-6 hemera-card-shadow"
      >
        <h2 className="font-sans font-semibold text-foreground mb-4">Atividade Recente</h2>
        <div className="space-y-3">
          {[
            { text: "Prova de Matemática — 7º A corrigida", time: "Hoje, 14:32" },
            { text: "Novo material publicado — Ciências 6º B", time: "Hoje, 11:15" },
            { text: "Chamada realizada — 8º C", time: "Ontem, 08:20" },
            { text: "Reunião pedagógica agendada", time: "Ontem, 16:00" },
          ].map((act, i) => (
            <div key={i} className="flex items-center justify-between py-2 border-b last:border-0">
              <span className="text-sm text-foreground">{act.text}</span>
              <span className="text-xs text-muted-foreground tabular-nums">{act.time}</span>
            </div>
          ))}
        </div>
      </motion.div>
    </div>
  );
};

export default DashboardHome;
