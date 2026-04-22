import { AuroraBackground, HemeraHeader } from "@/components/HemeraChrome";
import { FloatingSidebar } from "@/components/FloatingSidebar";
import { Button } from "@/components/ui/button";
import { Plus, Settings, Calendar as CalIcon, Users, Sparkles } from "lucide-react";
import { useAuth } from "@/hooks/useAuth";

const turmas = [
  { code: "1ª A", name: "INTEGRAL", students: 12, color: "from-primary to-primary-glow" },
  { code: "1ª A", name: "ADM", students: 36, color: "from-sun to-primary" },
  { code: "1ª B", name: "INTEGRAL", students: 13, color: "from-primary-glow to-sun" },
  { code: "1ª D", name: "ADM", students: 32, color: "from-primary to-sun-glow" },
  { code: "2ª", name: "INTEGRAL", students: 13, color: "from-sun-glow to-primary" },
  { code: "3ª C", name: "ELETIVA", students: 38, color: "from-primary-glow to-primary" },
];

const grade = [
  { hora: "13:10", seg: "1ª A INTEGRAL", ter: "2ª INTEGRAL", qua: "1ª B INTEGRAL", qui: "AC", sex: "3ªC ELETIVA" },
  { hora: "14:00", seg: "1ª A ADM", ter: "2ª INTEGRAL", qua: "1ª B INTEGRAL", qui: "AC", sex: "1ª A INTEGRAL" },
  { hora: "14:50", seg: "1ª B ADM", ter: "1ª D ADM", qua: "—", qui: "AC", sex: "—" },
  { hora: "15:40", seg: "2ª/3ª E FLUXO", ter: "1ª D ADM", qua: "2ª/3ª E FLUXO", qui: "AC", sex: "—" },
];

const Professor = () => {
  const { profile } = useAuth();
  const name = profile?.display_name || profile?.full_name || "Professor";
  const initial = (name[0] || "P").toUpperCase();
  const levelLabel = profile?.education_level === "creche" ? "Creche"
    : profile?.education_level === "fundamental_1" ? "Fundamental I"
    : profile?.education_level === "fundamental_2" ? "Fundamental II"
    : profile?.education_level === "superior" ? "Superior"
    : "Ensino Médio";
  return (
    <div className="min-h-screen relative pl-24 pr-6">
      <AuroraBackground />
      <FloatingSidebar role="professor" />
      <HemeraHeader>
        <div className="flex items-center gap-2">
          <Button variant="outline" size="sm" className="gap-2"><Sparkles className="h-4 w-4 text-sun" /> Modo Visão</Button>
        </div>
      </HemeraHeader>

      <div className="max-w-7xl mx-auto py-6 animate-fade-in">
        <div className="flex items-end justify-between mb-8">
          <div>
            <p className="text-xs uppercase tracking-[0.25em] text-primary/80 mb-2">Sábado · Aurora ativa</p>
            <h1 className="font-display text-5xl">Painel do Professor</h1>
          </div>
          <div className="flex gap-2">
            <Button variant="outline" className="gap-2"><Settings className="h-4 w-4" /> Configurar grade</Button>
            <Button className="bg-primary hover:bg-primary/90 gap-2"><Plus className="h-4 w-4" /> Nova turma</Button>
          </div>
        </div>

        <div className="grid lg:grid-cols-[280px_1fr] gap-6">
          {/* Coluna esquerda */}
          <div className="space-y-4">
            <div className="glass rounded-2xl p-5 text-center">
              <div className="w-20 h-20 mx-auto rounded-full bg-gradient-to-br from-primary to-sun grid place-items-center text-primary-foreground font-display text-3xl">{initial}</div>
              <div className="font-display text-xl mt-3 truncate">{name}</div>
              <div className="text-xs text-muted-foreground">Professor · {levelLabel}</div>
            </div>

            <div className="glass rounded-2xl p-5 bg-gradient-to-br from-primary/90 to-primary-glow/90 text-primary-foreground">
              <div className="flex justify-between items-start">
                <div>
                  <div className="font-display text-5xl">19°</div>
                  <div className="text-sm opacity-80">Seabra</div>
                </div>
                <div className="w-10 h-10"><HemeraSunMini /></div>
              </div>
              <div className="grid grid-cols-3 gap-2 mt-6 text-xs opacity-90">
                <div><div>09h</div><div className="font-display text-lg">20°</div></div>
                <div><div>15h</div><div className="font-display text-lg">22°</div></div>
                <div><div>20h</div><div className="font-display text-lg">20°</div></div>
              </div>
            </div>

            <div className="glass rounded-2xl p-4 text-sm space-y-3">
              <button className="w-full flex justify-between items-center hover:text-primary transition-colors">
                <span className="flex items-center gap-2"><CalIcon className="h-4 w-4" /> Planejamentos</span><span>›</span>
              </button>
              <div className="h-px bg-border" />
              <button className="w-full flex justify-between items-center hover:text-primary transition-colors">
                <span className="flex items-center gap-2"><Users className="h-4 w-4" /> Diário de Bordo</span><span>›</span>
              </button>
            </div>
          </div>

          {/* Coluna direita */}
          <div className="space-y-6">
            <div className="glass rounded-2xl overflow-hidden">
              <div className="flex items-center justify-between px-5 py-4 border-b border-border/60">
                <h2 className="font-display text-2xl flex items-center gap-2"><CalIcon className="h-5 w-5 text-primary" /> Grade Semanal</h2>
                <span className="text-xs text-emerald-600 flex items-center gap-1.5"><span className="w-1.5 h-1.5 rounded-full bg-emerald-500" /> ATIVA</span>
              </div>
              <table className="w-full text-sm">
                <thead><tr className="text-[10px] uppercase tracking-wider text-muted-foreground">
                  {["Horário","Seg","Ter","Qua","Qui","Sex"].map(h => <th key={h} className="text-left px-4 py-2 font-medium">{h}</th>)}
                </tr></thead>
                <tbody>
                  {grade.map((row) => (
                    <tr key={row.hora} className="border-t border-border/40">
                      <td className="px-4 py-3 text-muted-foreground font-medium">{row.hora}</td>
                      {[row.seg,row.ter,row.qua,row.qui,row.sex].map((c, i) => (
                        <td key={i} className="px-4 py-3">
                          {c === "—" ? <span className="text-muted-foreground/40">—</span>
                           : c === "AC" ? <span className="text-xs text-muted-foreground">AC</span>
                           : <div className="rounded-lg bg-primary/8 border border-primary/15 px-2 py-1.5">
                               <div className="text-xs font-semibold text-primary">{c}</div>
                             </div>}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            <div>
              <h3 className="text-xs uppercase tracking-[0.25em] text-muted-foreground mb-4">Acesso rápido</h3>
              <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-3">
                {turmas.map((t) => (
                  <button key={t.code+t.name} className="glass rounded-2xl p-4 flex items-center gap-3 hover:-translate-y-0.5 transition-transform text-left">
                    <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${t.color} grid place-items-center text-primary-foreground font-display text-lg`}>{t.code}</div>
                    <div className="flex-1">
                      <div className="font-semibold text-sm">{t.code} {t.name}</div>
                      <div className="text-xs text-muted-foreground">VESPERTINO · {t.students} alunos</div>
                    </div>
                    <span className="text-muted-foreground">›</span>
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

const HemeraSunMini = () => (
  <svg viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="5" fill="hsl(var(--sun))" />
    {[0,45,90,135,180,225,270,315].map(d => <line key={d} x1="12" y1="2" x2="12" y2="5" stroke="hsl(var(--sun-glow))" strokeWidth="1.5" strokeLinecap="round" transform={`rotate(${d} 12 12)`} />)}
  </svg>
);

export default Professor;
