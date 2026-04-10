import { motion } from "framer-motion";
import { Baby, Puzzle, BookMarked, Target } from "lucide-react";

const segments = [
  {
    icon: Baby,
    phase: "Educação Infantil",
    ages: "0–5 anos",
    desc: "Diário infantil com fotos, relatórios de rotina e comunicação direta com os responsáveis.",
    color: "bg-hemera-coral/10 text-hemera-coral",
  },
  {
    icon: Puzzle,
    phase: "Fundamental I",
    ages: "6–10 anos",
    desc: "Interface lúdica e gamificada com trilhas de aprendizagem e tarefas interativas.",
    color: "bg-hemera-gold/10 text-hemera-gold",
  },
  {
    icon: BookMarked,
    phase: "Fundamental II",
    ages: "11–14 anos",
    desc: "Feed social, calendário de provas, videoaulas de reforço e fóruns de dúvidas.",
    color: "bg-hemera-sage/10 text-hemera-sage",
  },
  {
    icon: Target,
    phase: "Ensino Médio",
    ages: "15–17 anos",
    desc: "Simulados cronometrados, análise de proficiência e rotas de estudo para o ENEM.",
    color: "bg-secondary/10 text-secondary",
  },
];

const SegmentsSection = () => (
  <section className="py-24 lg:py-32 bg-muted/50">
    <div className="container mx-auto px-6 lg:px-8">
      <motion.div
        initial={{ opacity: 0, y: 16, filter: "blur(4px)" }}
        whileInView={{ opacity: 1, y: 0, filter: "blur(0px)" }}
        viewport={{ once: true, amount: 0.2 }}
        transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
        className="text-center max-w-2xl mx-auto mb-16"
      >
        <h2 className="text-3xl sm:text-4xl font-display text-foreground mb-4">
          Adaptado para cada fase
        </h2>
        <p className="text-muted-foreground text-lg">
          A interface e os recursos se moldam ao estágio de desenvolvimento do aluno.
        </p>
      </motion.div>

      <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-8">
        {segments.map((s, i) => (
          <motion.div
            key={s.phase}
            initial={{ opacity: 0, y: 20, filter: "blur(4px)" }}
            whileInView={{ opacity: 1, y: 0, filter: "blur(0px)" }}
            viewport={{ once: true, amount: 0.2 }}
            transition={{ duration: 0.55, delay: i * 0.1, ease: [0.16, 1, 0.3, 1] }}
            className="text-center"
          >
            <div className={`w-14 h-14 rounded-xl ${s.color} flex items-center justify-center mx-auto mb-4`}>
              <s.icon className="w-7 h-7" />
            </div>
            <h3 className="font-sans font-semibold text-foreground mb-1">{s.phase}</h3>
            <p className="text-xs text-muted-foreground mb-3 tabular-nums">{s.ages}</p>
            <p className="text-sm text-muted-foreground leading-relaxed">{s.desc}</p>
          </motion.div>
        ))}
      </div>
    </div>
  </section>
);

export default SegmentsSection;
