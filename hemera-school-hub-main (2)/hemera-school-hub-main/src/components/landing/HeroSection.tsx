import { motion } from "framer-motion";
import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";
import heroBg from "@/assets/hero-bg.jpg";

const HeroSection = () => {
  return (
    <section className="relative min-h-[90vh] flex items-center overflow-hidden">
      <img
        src={heroBg}
        alt=""
        className="absolute inset-0 w-full h-full object-cover"
        loading="eager"
      />
      <div className="absolute inset-0 bg-gradient-to-r from-secondary/30 via-secondary/60 to-secondary/95" />

      <div className="container relative z-10 mx-auto px-6 lg:px-8">
        <div className="ml-auto max-w-2xl lg:text-right">
          <motion.p
            initial={{ opacity: 0, y: 16, filter: "blur(4px)" }}
            animate={{ opacity: 1, y: 0, filter: "blur(0px)" }}
            transition={{ duration: 0.6, delay: 0.1, ease: [0.16, 1, 0.3, 1] }}
            className="text-sm font-medium tracking-widest uppercase text-hemera-gold-light mb-4"
          >
            Ambiente Virtual de Aprendizagem
          </motion.p>

          <motion.h1
            initial={{ opacity: 0, y: 20, filter: "blur(4px)" }}
            animate={{ opacity: 1, y: 0, filter: "blur(0px)" }}
            transition={{ duration: 0.7, delay: 0.25, ease: [0.16, 1, 0.3, 1] }}
            className="text-4xl sm:text-5xl lg:text-6xl font-display text-secondary-foreground leading-[1.1] mb-6"
          >
            Iluminando o caminho da educação
          </motion.h1>

          <motion.p
            initial={{ opacity: 0, y: 16, filter: "blur(4px)" }}
            animate={{ opacity: 1, y: 0, filter: "blur(0px)" }}
            transition={{ duration: 0.6, delay: 0.45, ease: [0.16, 1, 0.3, 1] }}
            className="text-base sm:text-lg text-secondary-foreground/80 max-w-lg ml-auto mb-8 leading-relaxed"
          >
            Da Educação Infantil ao Ensino Médio — o sistema nervoso central da sua escola. 
            Professores planejam, alunos aprendem, famílias acompanham.
          </motion.p>

          <motion.div
            initial={{ opacity: 0, y: 16, filter: "blur(4px)" }}
            animate={{ opacity: 1, y: 0, filter: "blur(0px)" }}
            transition={{ duration: 0.6, delay: 0.6, ease: [0.16, 1, 0.3, 1] }}
            className="flex gap-4 justify-end"
          >
            <Button asChild size="lg" variant="hemera">
              <Link to="/auth">Acessar Plataforma</Link>
            </Button>
            <Button asChild size="lg" variant="hemerOutline">
              <a href="#funcionalidades">Conhecer</a>
            </Button>
          </motion.div>
        </div>
      </div>
    </section>
  );
};

export default HeroSection;
