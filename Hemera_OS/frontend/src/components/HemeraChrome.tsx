import { HemeraSun } from "./HemeraSun";

export const AuroraBackground = () => (
  <div className="fixed inset-0 -z-10 overflow-hidden pointer-events-none">
    <div className="absolute -top-40 -left-40 w-[42rem] h-[42rem] rounded-full opacity-40 aurora-blob"
         style={{ background: "radial-gradient(circle, hsl(var(--primary, 201 96% 32%) / 0.18), transparent 65%)" }} />
    <div className="absolute top-1/3 -right-32 w-[36rem] h-[36rem] rounded-full opacity-50 aurora-blob"
         style={{ background: "radial-gradient(circle, hsl(var(--sun, 45 100% 50%) / 0.20), transparent 65%)", animationDelay: "-6s" }} />
    <div className="absolute -bottom-40 left-1/4 w-[40rem] h-[40rem] rounded-full opacity-35 aurora-blob"
         style={{ background: "radial-gradient(circle, hsl(var(--primary-glow, 201 96% 50%) / 0.15), transparent 65%)", animationDelay: "-12s" }} />
  </div>
);

export const HemeraHeader = ({ children }: { children?: React.ReactNode }) => (
  <header className="sticky top-0 z-30 px-6 py-4">
    <div className="glass rounded-2xl flex items-center justify-between px-5 py-3">
      <div className="flex items-center gap-3">
        <HemeraSun size={36} />
        <div className="leading-tight">
          <div className="font-display text-2xl text-primary">Hemera</div>
          <div className="text-[10px] uppercase tracking-[0.2em] text-muted-foreground">OS Educacional</div>
        </div>
      </div>
      {children}
    </div>
  </header>
);
