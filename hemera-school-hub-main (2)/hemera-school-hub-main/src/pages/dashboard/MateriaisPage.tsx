import { motion } from "framer-motion";
import { BookOpen, FileText, Video, Download, Plus } from "lucide-react";
import { Button } from "@/components/ui/button";

const materiais = [
  { titulo: "Equações do 1º Grau", tipo: "PDF", turma: "7º A", data: "12/03/2026", icon: FileText },
  { titulo: "Videoaula — Frações", tipo: "Vídeo", turma: "6º A", data: "10/03/2026", icon: Video },
  { titulo: "Lista de Exercícios #4", tipo: "PDF", turma: "8º C", data: "08/03/2026", icon: FileText },
  { titulo: "Apresentação — Geometria Plana", tipo: "Slides", turma: "9º A", data: "05/03/2026", icon: BookOpen },
  { titulo: "Revisão para Prova — Álgebra", tipo: "PDF", turma: "9º B", data: "03/03/2026", icon: FileText },
];

const item = {
  hidden: { opacity: 0, y: 14, filter: "blur(4px)" },
  show: { opacity: 1, y: 0, filter: "blur(0px)", transition: { duration: 0.5, ease: [0.16, 1, 0.3, 1] } },
};

const MateriaisPage = () => (
  <div className="max-w-4xl mx-auto space-y-6">
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
      className="flex items-center justify-between"
    >
      <div>
        <h1 className="text-2xl font-display text-foreground">Materiais & Aulas</h1>
        <p className="text-muted-foreground mt-1">Publique e organize conteúdos para suas turmas.</p>
      </div>
      <Button className="gap-2">
        <Plus className="w-4 h-4" />
        Novo Material
      </Button>
    </motion.div>

    <motion.div
      initial="hidden"
      animate="show"
      variants={{ show: { transition: { staggerChildren: 0.06 } } }}
      className="bg-card rounded-lg hemera-card-shadow divide-y"
    >
      {materiais.map((m) => (
        <motion.div
          key={m.titulo}
          variants={item}
          className="flex items-center justify-between px-5 py-4 hover:bg-muted/30 transition-colors"
        >
          <div className="flex items-center gap-4">
            <div className="w-10 h-10 rounded-md bg-muted flex items-center justify-center">
              <m.icon className="w-5 h-5 text-muted-foreground" />
            </div>
            <div>
              <p className="font-medium text-sm text-foreground">{m.titulo}</p>
              <p className="text-xs text-muted-foreground">{m.turma} · {m.tipo} · {m.data}</p>
            </div>
          </div>
          <button className="p-2 rounded-md hover:bg-muted text-muted-foreground">
            <Download className="w-4 h-4" />
          </button>
        </motion.div>
      ))}
    </motion.div>
  </div>
);

export default MateriaisPage;
