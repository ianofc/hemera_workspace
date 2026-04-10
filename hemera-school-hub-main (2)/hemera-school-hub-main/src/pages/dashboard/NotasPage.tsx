import { motion } from "framer-motion";
import { BarChart3, TrendingDown, TrendingUp } from "lucide-react";

const disciplinas = [
  { nome: "Matemática", professor: "Prof. Ricardo", media: 7.8, status: "acima", faltas: 2 },
  { nome: "Português", professor: "Profa. Claudia", media: 6.2, status: "abaixo", faltas: 4 },
  { nome: "Ciências", professor: "Prof. André", media: 8.5, status: "acima", faltas: 1 },
  { nome: "História", professor: "Profa. Fernanda", media: 7.0, status: "media", faltas: 3 },
  { nome: "Geografia", professor: "Prof. Marcos", media: 5.8, status: "abaixo", faltas: 6 },
  { nome: "Inglês", professor: "Profa. Sarah", media: 9.1, status: "acima", faltas: 0 },
];

const item = {
  hidden: { opacity: 0, y: 14, filter: "blur(4px)" },
  show: { opacity: 1, y: 0, filter: "blur(0px)", transition: { duration: 0.5, ease: [0.16, 1, 0.3, 1] } },
};

const NotasPage = () => (
  <div className="max-w-4xl mx-auto space-y-6">
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
    >
      <h1 className="text-2xl font-display text-foreground">Notas & Boletim</h1>
      <p className="text-muted-foreground mt-1">Acompanhe seu desempenho em cada disciplina.</p>
    </motion.div>

    {/* Summary */}
    <div className="grid grid-cols-3 gap-4">
      <div className="bg-card rounded-lg p-5 hemera-card-shadow text-center">
        <p className="text-3xl font-semibold tabular-nums text-foreground">7.4</p>
        <p className="text-xs text-muted-foreground mt-1">Média Geral</p>
      </div>
      <div className="bg-card rounded-lg p-5 hemera-card-shadow text-center">
        <p className="text-3xl font-semibold tabular-nums text-hemera-sage">4</p>
        <p className="text-xs text-muted-foreground mt-1">Acima da Média</p>
      </div>
      <div className="bg-card rounded-lg p-5 hemera-card-shadow text-center">
        <p className="text-3xl font-semibold tabular-nums text-hemera-coral">2</p>
        <p className="text-xs text-muted-foreground mt-1">Atenção Necessária</p>
      </div>
    </div>

    {/* Per-subject */}
    <motion.div
      initial="hidden"
      animate="show"
      variants={{ show: { transition: { staggerChildren: 0.06 } } }}
      className="bg-card rounded-lg hemera-card-shadow divide-y"
    >
      {disciplinas.map((d) => (
        <motion.div
          key={d.nome}
          variants={item}
          className="flex items-center justify-between px-5 py-4"
        >
          <div className="flex items-center gap-4">
            <div className={`w-10 h-10 rounded-md flex items-center justify-center ${
              d.status === "acima" ? "bg-hemera-sage/10" : d.status === "abaixo" ? "bg-hemera-coral/10" : "bg-muted"
            }`}>
              {d.status === "acima" ? (
                <TrendingUp className="w-5 h-5 text-hemera-sage" />
              ) : d.status === "abaixo" ? (
                <TrendingDown className="w-5 h-5 text-hemera-coral" />
              ) : (
                <BarChart3 className="w-5 h-5 text-muted-foreground" />
              )}
            </div>
            <div>
              <p className="font-medium text-sm text-foreground">{d.nome}</p>
              <p className="text-xs text-muted-foreground">{d.professor} · {d.faltas} faltas</p>
            </div>
          </div>
          <span className={`text-lg font-semibold tabular-nums ${
            d.media >= 7 ? "text-hemera-sage" : d.media >= 6 ? "text-hemera-gold" : "text-hemera-coral"
          }`}>
            {d.media.toFixed(1)}
          </span>
        </motion.div>
      ))}
    </motion.div>
  </div>
);

export default NotasPage;
