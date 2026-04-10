import { motion } from "framer-motion";

const PlaceholderPage = ({ title, desc }: { title: string; desc: string }) => (
  <div className="max-w-4xl mx-auto">
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
    >
      <h1 className="text-2xl font-display text-foreground">{title}</h1>
      <p className="text-muted-foreground mt-1">{desc}</p>
    </motion.div>
    <motion.div
      initial={{ opacity: 0, y: 14, filter: "blur(4px)" }}
      animate={{ opacity: 1, y: 0, filter: "blur(0px)" }}
      transition={{ duration: 0.5, delay: 0.2, ease: [0.16, 1, 0.3, 1] }}
      className="mt-8 bg-card rounded-lg p-12 hemera-card-shadow flex items-center justify-center"
    >
      <p className="text-muted-foreground text-sm">Este módulo será implementado em breve.</p>
    </motion.div>
  </div>
);

export const AvaliacoesPage = () => <PlaceholderPage title="Avaliações" desc="Crie e gerencie provas e atividades avaliativas." />;
export const PlanejamentoPage = () => <PlaceholderPage title="Planejamento" desc="Organize o plano de ensino anual alinhado à BNCC." />;
export const MensagensPage = () => <PlaceholderPage title="Mensagens" desc="Comunique-se com alunos, responsáveis e equipe pedagógica." />;
export const AulasAlunoPage = () => <PlaceholderPage title="Minhas Aulas" desc="Acesse os materiais e atividades das suas turmas." />;
export const AtividadesPage = () => <PlaceholderPage title="Atividades" desc="Veja e submeta trabalhos e tarefas pendentes." />;
export const AvaliacoesAlunoPage = () => <PlaceholderPage title="Avaliações" desc="Realize provas online e simulados." />;
