import { useState } from "react";
import { motion } from "framer-motion";
import { Check, X, Minus } from "lucide-react";
import { Button } from "@/components/ui/button";
import { toast } from "sonner";

const alunos = [
  "Ana Beatriz Oliveira", "Bruno Carvalho", "Camila Ferreira", "Daniel Souza",
  "Elena Machado", "Felipe Rocha", "Gabriela Costa", "Henrique Lima",
  "Isabela Santos", "João Pedro Alves", "Karen Nascimento", "Leonardo Barbosa",
  "Mariana Dias", "Nicolas Ribeiro", "Olívia Martins", "Paulo Henrique Gomes",
];

type Status = "presente" | "ausente" | "justificado" | null;

const DiarioPage = () => {
  const [frequencia, setFrequencia] = useState<Record<string, Status>>(
    Object.fromEntries(alunos.map((a) => [a, null]))
  );

  const setStatus = (nome: string, status: Status) => {
    setFrequencia((prev) => ({ ...prev, [nome]: status }));
  };

  const total = alunos.length;
  const presentes = Object.values(frequencia).filter((s) => s === "presente").length;
  const ausentes = Object.values(frequencia).filter((s) => s === "ausente").length;

  const salvar = () => {
    toast.success(`Chamada salva! ${presentes} presentes, ${ausentes} ausentes.`);
  };

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      <motion.div
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
      >
        <h1 className="text-2xl font-display text-foreground">Diário de Classe</h1>
        <p className="text-muted-foreground mt-1">7º Ano A — Matemática — {new Date().toLocaleDateString("pt-BR")}</p>
      </motion.div>

      {/* Stats bar */}
      <div className="flex gap-4 text-sm">
        <span className="bg-hemera-sage/10 text-hemera-sage px-3 py-1 rounded-md tabular-nums">{presentes} presentes</span>
        <span className="bg-hemera-coral/10 text-hemera-coral px-3 py-1 rounded-md tabular-nums">{ausentes} ausentes</span>
        <span className="bg-muted text-muted-foreground px-3 py-1 rounded-md tabular-nums">{total - presentes - ausentes} pendentes</span>
      </div>

      {/* Student list */}
      <div className="bg-card rounded-lg hemera-card-shadow divide-y">
        {alunos.map((nome, i) => {
          const status = frequencia[nome];
          return (
            <motion.div
              key={nome}
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.3, delay: i * 0.02, ease: [0.16, 1, 0.3, 1] }}
              className="flex items-center justify-between px-5 py-3"
            >
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 rounded-full bg-muted flex items-center justify-center text-xs font-medium text-muted-foreground">
                  {nome.split(" ").map((n) => n[0]).slice(0, 2).join("")}
                </div>
                <span className="text-sm text-foreground">{nome}</span>
              </div>

              <div className="flex gap-1">
                <button
                  onClick={() => setStatus(nome, "presente")}
                  className={`p-2 rounded-md transition-colors ${
                    status === "presente" ? "bg-hemera-sage/20 text-hemera-sage" : "hover:bg-muted text-muted-foreground"
                  }`}
                  title="Presente"
                >
                  <Check className="w-4 h-4" />
                </button>
                <button
                  onClick={() => setStatus(nome, "ausente")}
                  className={`p-2 rounded-md transition-colors ${
                    status === "ausente" ? "bg-hemera-coral/20 text-hemera-coral" : "hover:bg-muted text-muted-foreground"
                  }`}
                  title="Ausente"
                >
                  <X className="w-4 h-4" />
                </button>
                <button
                  onClick={() => setStatus(nome, "justificado")}
                  className={`p-2 rounded-md transition-colors ${
                    status === "justificado" ? "bg-hemera-gold/20 text-hemera-gold" : "hover:bg-muted text-muted-foreground"
                  }`}
                  title="Justificado"
                >
                  <Minus className="w-4 h-4" />
                </button>
              </div>
            </motion.div>
          );
        })}
      </div>

      <div className="flex justify-end">
        <Button onClick={salvar}>Salvar Chamada</Button>
      </div>
    </div>
  );
};

export default DiarioPage;
