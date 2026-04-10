import { motion } from "framer-motion";
import {
  BookOpen, Users, BarChart3, Calendar,
  Shield, MessageCircle, GraduationCap, Brain
} from "lucide-react";

const features = [
  {
    icon: BookOpen,
    title: "Sala de Aula Virtual",
    desc: "Materiais, videoaulas, atividades e submissão de trabalhos em um único ambiente.",
  },
  {
    icon: Users,
    title: "Diário de Classe Digital",
    desc: "Chamada rápida, lançamento de notas, frequência e ocorrências em poucos cliques.",
  },
  {
    icon: BarChart3,
    title: "Boletim & Analytics",
    desc: "Notas, médias automáticas e análise de desempenho por disciplina e competência.",
  },
  {
    icon: Calendar,
    title: "Planejamento Pedagógico",
    desc: "Plano de aula anual, trilhas de aprendizagem e alinhamento com a BNCC.",
  },
  {
    icon: Shield,
    title: "Secretaria Escolar",
    desc: "Matrículas, enturmação, transferências, históricos e documentação oficial.",
  },
  {
    icon: MessageCircle,
    title: "Comunicação Integrada",
    desc: "Chat seguro, mural de recados e canal direto entre escola e famílias.",
  },
  {
    icon: GraduationCap,
    title: "Avaliações & Provas",
    desc: "Criação de provas online com correção automática e banco de questões.",
  },
  {
    icon: Brain,
    title: "Tutor IA — ZIOS",
    desc: "Assistente inteligente para alunos e professores, com geração de questões e rubricas.",
  },
];

const container = {
  hidden: {},
  show: { transition: { staggerChildren: 0.08 } },
};
const item = {
  hidden: { opacity: 0, y: 16, filter: "blur(4px)" },
  show: { opacity: 1, y: 0, filter: "blur(0px)", transition: { duration: 0.55, ease: [0.16, 1, 0.3, 1] } },
};

const FeaturesSection = () => (
  <section id="funcionalidades" className="py-24 lg:py-32 bg-background">
    <div className="container mx-auto px-6 lg:px-8">
      <motion.div
        initial={{ opacity: 0, y: 16, filter: "blur(4px)" }}
        whileInView={{ opacity: 1, y: 0, filter: "blur(0px)" }}
        viewport={{ once: true, amount: 0.2 }}
        transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
        className="text-center max-w-2xl mx-auto mb-16"
      >
        <h2 className="text-3xl sm:text-4xl font-display text-foreground mb-4">
          Tudo que a escola precisa
        </h2>
        <p className="text-muted-foreground text-lg leading-relaxed">
          Do berçário ao vestibular, cada módulo foi desenhado para a realidade do chão de escola.
        </p>
      </motion.div>

      <motion.div
        variants={container}
        initial="hidden"
        whileInView="show"
        viewport={{ once: true, amount: 0.15 }}
        className="grid sm:grid-cols-2 lg:grid-cols-4 gap-6"
      >
        {features.map((f) => (
          <motion.div
            key={f.title}
            variants={item}
            className="group rounded-lg p-6 bg-card hemera-card-shadow cursor-default"
          >
            <div className="w-10 h-10 rounded-md hemera-gradient flex items-center justify-center mb-4">
              <f.icon className="w-5 h-5 text-primary-foreground" />
            </div>
            <h3 className="font-sans font-semibold text-foreground mb-2 text-base">{f.title}</h3>
            <p className="text-sm text-muted-foreground leading-relaxed">{f.desc}</p>
          </motion.div>
        ))}
      </motion.div>
    </div>
  </section>
);

export default FeaturesSection;
