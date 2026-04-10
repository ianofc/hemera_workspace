import { motion } from "framer-motion";
import { Search, BookOpen, FileText, Video, Headphones } from "lucide-react";
import { Input } from "@/components/ui/input";

const acervo = [
  { titulo: "Matemática — Fundamentos de Álgebra", tipo: "Livro Digital", icon: BookOpen, categoria: "Exatas" },
  { titulo: "Interpretação de Texto — Exercícios", tipo: "PDF", icon: FileText, categoria: "Linguagens" },
  { titulo: "A Revolução Francesa — Documentário", tipo: "Vídeo", icon: Video, categoria: "Humanas" },
  { titulo: "Gramática Aplicada — Vol. 2", tipo: "Livro Digital", icon: BookOpen, categoria: "Linguagens" },
  { titulo: "Podcast — Curiosidades de Ciências", tipo: "Áudio", icon: Headphones, categoria: "Natureza" },
  { titulo: "Geometria Espacial — Apostila", tipo: "PDF", icon: FileText, categoria: "Exatas" },
  { titulo: "English for Teens — Level B1", tipo: "Livro Digital", icon: BookOpen, categoria: "Linguagens" },
  { titulo: "Biomas Brasileiros — Atlas Interativo", tipo: "Interativo", icon: BookOpen, categoria: "Natureza" },
];

const item = {
  hidden: { opacity: 0, y: 14, filter: "blur(4px)" },
  show: { opacity: 1, y: 0, filter: "blur(0px)", transition: { duration: 0.5, ease: [0.16, 1, 0.3, 1] } },
};

const BibliotecaPage = () => (
  <div className="max-w-5xl mx-auto space-y-6">
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
    >
      <h1 className="text-2xl font-display text-foreground">Biblioteca</h1>
      <p className="text-muted-foreground mt-1">Explore o acervo digital da escola.</p>
    </motion.div>

    <div className="relative max-w-md">
      <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
      <Input placeholder="Buscar por título, disciplina ou tema..." className="pl-9" />
    </div>

    <motion.div
      initial="hidden"
      animate="show"
      variants={{ show: { transition: { staggerChildren: 0.05 } } }}
      className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4"
    >
      {acervo.map((item_data) => (
        <motion.div
          key={item_data.titulo}
          variants={item}
          className="bg-card rounded-lg p-5 hemera-card-shadow cursor-pointer active:scale-[0.97] transition-transform"
        >
          <div className="w-10 h-10 rounded-md bg-muted flex items-center justify-center mb-3">
            <item_data.icon className="w-5 h-5 text-muted-foreground" />
          </div>
          <p className="font-medium text-sm text-foreground mb-1 line-clamp-2">{item_data.titulo}</p>
          <div className="flex items-center gap-2 text-xs text-muted-foreground">
            <span>{item_data.tipo}</span>
            <span>·</span>
            <span>{item_data.categoria}</span>
          </div>
        </motion.div>
      ))}
    </motion.div>
  </div>
);

export default BibliotecaPage;
