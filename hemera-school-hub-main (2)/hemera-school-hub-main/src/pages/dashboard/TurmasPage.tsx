import { motion } from "framer-motion";
import { Users, Clock, MoreVertical } from "lucide-react";

const turmas = [
  { nome: "6º Ano A", disciplina: "Matemática", alunos: 32, horario: "Seg/Qua/Sex — 07:30", status: "Ativa" },
  { nome: "7º Ano A", disciplina: "Matemática", alunos: 28, horario: "Ter/Qui — 08:20", status: "Ativa" },
  { nome: "7º Ano B", disciplina: "Matemática", alunos: 31, horario: "Seg/Qua — 10:10", status: "Ativa" },
  { nome: "8º Ano C", disciplina: "Matemática", alunos: 29, horario: "Ter/Qui/Sex — 09:15", status: "Ativa" },
  { nome: "9º Ano A", disciplina: "Matemática", alunos: 35, horario: "Seg/Qua/Sex — 13:00", status: "Ativa" },
  { nome: "9º Ano B", disciplina: "Matemática", alunos: 32, horario: "Ter/Qui — 14:00", status: "Ativa" },
];

const item = {
  hidden: { opacity: 0, y: 14, filter: "blur(4px)" },
  show: { opacity: 1, y: 0, filter: "blur(0px)", transition: { duration: 0.5, ease: [0.16, 1, 0.3, 1] } },
};

const TurmasPage = () => (
  <div className="max-w-5xl mx-auto space-y-6">
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
    >
      <h1 className="text-2xl font-display text-foreground">Minhas Turmas</h1>
      <p className="text-muted-foreground mt-1">Gerencie suas turmas e acesse os diários de classe.</p>
    </motion.div>

    <motion.div
      initial="hidden"
      animate="show"
      variants={{ show: { transition: { staggerChildren: 0.06 } } }}
      className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4"
    >
      {turmas.map((t) => (
        <motion.div
          key={t.nome}
          variants={item}
          className="bg-card rounded-lg p-5 hemera-card-shadow group cursor-pointer active:scale-[0.97] transition-transform"
        >
          <div className="flex justify-between items-start mb-3">
            <div>
              <h3 className="font-semibold text-foreground">{t.nome}</h3>
              <p className="text-sm text-muted-foreground">{t.disciplina}</p>
            </div>
            <button className="p-1 rounded hover:bg-muted">
              <MoreVertical className="w-4 h-4 text-muted-foreground" />
            </button>
          </div>
          <div className="flex items-center gap-4 text-xs text-muted-foreground">
            <span className="flex items-center gap-1"><Users className="w-3.5 h-3.5" /> {t.alunos} alunos</span>
            <span className="flex items-center gap-1"><Clock className="w-3.5 h-3.5" /> {t.horario}</span>
          </div>
          <div className="mt-3 pt-3 border-t">
            <span className="text-xs font-medium text-hemera-sage">{t.status}</span>
          </div>
        </motion.div>
      ))}
    </motion.div>
  </div>
);

export default TurmasPage;
