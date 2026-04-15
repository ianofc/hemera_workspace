import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import AuroraBackground from "@/components/layout/AuroraBackground";

const niveis = [
  {
    id: "creche",
    titulo: "Creche",
    subtitulo: "Diário de Bordo",
    desc: "Alimentação, sono, atividades e recados para os pais",
    icon: "fas fa-baby",
    path: "/creche",
    gradient: "from-[hsl(25,90%,60%)] to-[hsl(45,95%,55%)]",
    auraTone: "Tons quentes e acolhedores",
    badge: "0–3 anos",
  },
  {
    id: "fundamental",
    titulo: "Fundamental",
    subtitulo: "Trindade Pedagógica",
    desc: "Gradebook, chamada, frequência e acompanhamento integral",
    icon: "fas fa-pencil-ruler",
    path: "/fundamental",
    gradient: "from-[hsl(160,70%,45%)] to-[hsl(190,80%,50%)]",
    auraTone: "Tons verdes e frescos",
    badge: "6–14 anos",
  },
  {
    id: "medio",
    titulo: "Ensino Médio",
    subtitulo: "Trindade Pedagógica",
    desc: "Notas, frequência, simulados e preparação para vestibular",
    icon: "fas fa-flask",
    path: "/medio",
    gradient: "from-primary to-secondary",
    auraTone: "Tons azuis profundos",
    badge: "15–17 anos",
  },
  {
    id: "graduacao",
    titulo: "Graduação",
    subtitulo: "Autonomia Acadêmica",
    desc: "Cursos, certificados, trilhas de conhecimento e gestão autônoma",
    icon: "fas fa-graduation-cap",
    path: "/graduacao",
    gradient: "from-secondary to-accent",
    auraTone: "Tons vibrantes e maduros",
    badge: "18+ anos",
  },
];

const container = {
  hidden: { opacity: 0 },
  show: { opacity: 1, transition: { staggerChildren: 0.12 } },
};

const item = {
  hidden: { opacity: 0, y: 30, scale: 0.95 },
  show: { opacity: 1, y: 0, scale: 1, transition: { duration: 0.5, ease: "easeOut" as const } },
};

const Index = () => (
  <div className="relative flex flex-col items-center justify-center min-h-screen overflow-hidden selection:bg-primary selection:text-primary-foreground">
    <AuroraBackground />

    <div className="relative z-10 w-full max-w-6xl px-6 py-16">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="mb-16 text-center"
      >
        <div className="flex items-center justify-center gap-3 mb-6">
          <div className="flex items-center justify-center w-14 h-14 rounded-2xl bg-gradient-to-br from-primary to-secondary shadow-neon text-primary-foreground">
            <i className="text-2xl fas fa-atom" />
          </div>
        </div>
        <h1 className="mb-3 text-5xl font-black tracking-tight font-display text-foreground">
          Hemera <span className="text-gradient-aurora">OS</span>
        </h1>
        <p className="text-lg font-medium text-muted-foreground max-w-md mx-auto">
          Selecione o nível de ensino para acessar seu ambiente de aprendizado
        </p>
      </motion.div>

      {/* Level Cards Grid */}
      <motion.div
        variants={container}
        initial="hidden"
        animate="show"
        className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4"
      >
        {niveis.map((nivel) => (
          <motion.div key={nivel.id} variants={item}>
            <Link
              to={nivel.path}
              className="group relative flex flex-col h-full p-6 overflow-hidden glass-card rounded-3xl shadow-float hover:shadow-neon transition-all duration-500 hover:-translate-y-2"
            >
              {/* Gradient accent top */}
              <div className={`absolute inset-x-0 top-0 h-1.5 bg-gradient-to-r ${nivel.gradient} opacity-80 group-hover:opacity-100 transition-opacity`} />

              {/* Icon */}
              <div className={`flex items-center justify-center w-14 h-14 mb-5 rounded-2xl bg-gradient-to-br ${nivel.gradient} text-white shadow-lg group-hover:scale-110 transition-transform duration-300`}>
                <i className={`${nivel.icon} text-xl`} />
              </div>

              {/* Badge */}
              <span className="inline-block self-start px-2.5 py-0.5 mb-3 text-[10px] font-bold tracking-wider uppercase rounded-full bg-muted text-muted-foreground">
                {nivel.badge}
              </span>

              {/* Text */}
              <h2 className="mb-1 text-xl font-bold font-display text-foreground group-hover:text-primary transition-colors">
                {nivel.titulo}
              </h2>
              <p className="mb-2 text-xs font-bold uppercase tracking-widest text-muted-foreground">
                {nivel.subtitulo}
              </p>
              <p className="flex-1 text-sm leading-relaxed text-muted-foreground">
                {nivel.desc}
              </p>

              {/* Enter arrow */}
              <div className="flex items-center gap-2 mt-5 text-sm font-bold text-primary opacity-0 group-hover:opacity-100 transition-all duration-300 translate-x-[-8px] group-hover:translate-x-0">
                Entrar <i className="fas fa-arrow-right text-xs" />
              </div>
            </Link>
          </motion.div>
        ))}
      </motion.div>

      {/* Footer hint */}
      <motion.p
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.8 }}
        className="mt-12 text-center text-xs text-muted-foreground"
      >
        <i className="fas fa-shield-alt mr-1" /> Powered by Hemera OS · Terminal de Inteligência Pedagógica
      </motion.p>
    </div>
  </div>
);

export default Index;
