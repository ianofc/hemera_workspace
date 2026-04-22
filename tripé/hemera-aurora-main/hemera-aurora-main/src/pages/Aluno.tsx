import { AuroraBackground, HemeraHeader } from "@/components/HemeraChrome";
import { FloatingSidebar } from "@/components/FloatingSidebar";
import { Button } from "@/components/ui/button";
import { Sparkles, BookOpen, ClipboardList, Trophy, PlayCircle } from "lucide-react";
import { useAuth } from "@/hooks/useAuth";

const disciplinas = [
  { name: "Matemática", prof: "Prof. Iansantos", aura: 78, color: "from-primary to-primary-glow" },
  { name: "Geografia", prof: "Profa. Marina", aura: 62, color: "from-sun to-primary" },
  { name: "Química", prof: "Prof. Hélio", aura: 84, color: "from-primary-glow to-sun" },
  { name: "Língua Portuguesa", prof: "Profa. Aurora", aura: 91, color: "from-sun-glow to-primary" },
];

const atividades = [
  { tipo: "PROVA", titulo: "Diário de Bordo · Experimento", data: "27/11", peso: "2.0 pts" },
  { tipo: "ATIVIDADE", titulo: "Avaliação de Geografia", data: "05/12", peso: "2.0 pts" },
  { tipo: "AULA AVA", titulo: "Funções Quadráticas · Módulo 3", data: "Hoje", peso: "12 min" },
];

const Aluno = () => {
  const { profile } = useAuth();
  const name = (profile?.display_name || profile?.full_name || "Aluno").split(" ")[0];
  const hour = new Date().getHours();
  const greeting = hour < 12 ? "Bom dia" : hour < 18 ? "Boa tarde" : "Boa noite";
  return (
    <div className="min-h-screen relative pl-24 pr-6">
      <AuroraBackground />
      <FloatingSidebar role="aluno" />
      <HemeraHeader>
        <Button variant="outline" size="sm" className="gap-2"><Sparkles className="h-4 w-4 text-sun" /> ZIOS</Button>
      </HemeraHeader>

      <div className="max-w-7xl mx-auto py-6 animate-fade-in">
        <div className="flex items-end justify-between mb-8">
          <div>
            <p className="text-xs uppercase tracking-[0.25em] text-primary/80 mb-2">{greeting}, {name}</p>
            <h1 className="font-display text-5xl">Sua aurora hoje</h1>
          </div>
          <div className="glass rounded-2xl px-5 py-3 flex items-center gap-3">
            <Trophy className="h-5 w-5 text-sun" />
            <div>
              <div className="text-[10px] uppercase tracking-wider text-muted-foreground">Aura acumulada</div>
              <div className="font-display text-2xl text-primary">7.9 <span className="text-sm text-muted-foreground">/ 10</span></div>
            </div>
          </div>
        </div>

        {/* Stats */}
        <div className="grid sm:grid-cols-4 gap-4 mb-8">
          {[
            { l: "Disciplinas", v: "6", i: BookOpen },
            { l: "Atividades", v: "11", i: ClipboardList },
            { l: "Cursos AVA", v: "3", i: PlayCircle },
            { l: "Frequência", v: "100%", i: Trophy },
          ].map((s) => (
            <div key={s.l} className="glass rounded-2xl p-5">
              <div className="flex justify-between items-start mb-2">
                <span className="text-xs uppercase tracking-wider text-muted-foreground">{s.l}</span>
                <s.i className="h-4 w-4 text-primary/60" />
              </div>
              <div className="font-display text-3xl">{s.v}</div>
            </div>
          ))}
        </div>

        <div className="grid lg:grid-cols-[1fr_380px] gap-6">
          {/* Disciplinas */}
          <div className="glass rounded-2xl p-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="font-display text-2xl">Trilha de conhecimento</h2>
              <button className="text-xs text-primary hover:underline">Ver todas ›</button>
            </div>
            <div className="space-y-3">
              {disciplinas.map((d) => (
                <div key={d.name} className="flex items-center gap-4 p-3 rounded-xl hover:bg-accent/40 transition-colors">
                  <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${d.color} grid place-items-center text-primary-foreground`}>
                    <BookOpen className="h-5 w-5" />
                  </div>
                  <div className="flex-1">
                    <div className="font-semibold">{d.name}</div>
                    <div className="text-xs text-muted-foreground">{d.prof}</div>
                  </div>
                  <div className="w-40">
                    <div className="flex justify-between text-xs mb-1"><span className="text-muted-foreground">Aura</span><span className="font-medium text-primary">{d.aura}%</span></div>
                    <div className="h-1.5 bg-muted rounded-full overflow-hidden">
                      <div className="h-full bg-gradient-to-r from-primary to-sun" style={{ width: `${d.aura}%` }} />
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Cronograma + ZIOS */}
          <div className="space-y-4">
            <div className="glass rounded-2xl p-6">
              <h2 className="font-display text-2xl mb-4">Cronograma</h2>
              <div className="space-y-3">
                {atividades.map((a) => (
                  <div key={a.titulo} className="flex gap-3">
                    <div className="flex flex-col items-center">
                      <div className="w-2 h-2 rounded-full bg-primary mt-2" />
                      <div className="w-px flex-1 bg-border mt-1" />
                    </div>
                    <div className="flex-1 pb-3">
                      <div className="flex items-center gap-2 mb-1">
                        <span className="text-[10px] font-semibold uppercase tracking-wider text-primary bg-primary/10 px-1.5 py-0.5 rounded">{a.tipo}</span>
                        <span className="text-xs text-muted-foreground">{a.data}</span>
                      </div>
                      <div className="text-sm font-medium">{a.titulo}</div>
                      <div className="text-xs text-muted-foreground">{a.peso}</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="glass-strong rounded-2xl p-5 bg-gradient-to-br from-primary/95 to-primary-glow/90 text-primary-foreground">
              <div className="flex items-center gap-2 mb-2">
                <Sparkles className="h-4 w-4 text-sun-glow" />
                <span className="text-xs uppercase tracking-[0.2em] opacity-80">ZIOS sugere</span>
              </div>
              <p className="text-sm opacity-95 mb-3">Sua nota em Geografia caiu 8% — preparei 5 questões focadas no ENEM pra recuperar a aura antes da próxima prova.</p>
              <Button size="sm" variant="secondary" className="bg-card text-primary hover:bg-card/90">Começar reforço</Button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Aluno;
