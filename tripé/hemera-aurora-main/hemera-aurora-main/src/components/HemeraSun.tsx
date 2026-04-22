import { cn } from "@/lib/utils";

interface HemeraSunProps {
  className?: string;
  animated?: boolean;
  size?: number;
}

/**
 * Logo Hemera — Sol mítico ornamental.
 * Raios alternados (longos/curtos) + miolo solar com detalhe grego.
 */
export const HemeraSun = ({ className, animated = true, size = 40 }: HemeraSunProps) => {
  const longRays = Array.from({ length: 8 }, (_, i) => i * 45);
  const shortRays = Array.from({ length: 8 }, (_, i) => i * 45 + 22.5);

  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 100 100"
      className={cn(animated && "animate-sun-pulse", className)}
      aria-label="Hemera"
    >
      <defs>
    <radialGradient id="hemeraCore" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stopColor="hsl(var(--sun-glow))" />
          <stop offset="50%" stopColor="hsl(var(--sun))" />
          <stop offset="100%" stopColor="hsl(var(--primary))" />
        </radialGradient>
        <linearGradient id="hemeraRay" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" stopColor="hsl(var(--primary))" />
          <stop offset="50%" stopColor="hsl(var(--primary-glow))" />
          <stop offset="100%" stopColor="hsl(var(--sun))" />
        </linearGradient>
      </defs>

      {/* Raios longos */}
      {longRays.map((deg) => (
        <polygon
          key={`l-${deg}`}
          className="ray"
          points="50,4 47,22 53,22"
          fill="url(#hemeraRay)"
          transform={`rotate(${deg} 50 50)`}
        />
      ))}
      {/* Raios curtos */}
      {shortRays.map((deg) => (
        <polygon
          key={`s-${deg}`}
          className="ray"
          points="50,14 48,24 52,24"
          fill="hsl(var(--sun))"
          opacity="0.85"
          transform={`rotate(${deg} 50 50)`}
        />
      ))}

      {/* Miolo */}
      <circle cx="50" cy="50" r="20" fill="url(#hemeraCore)" />
      <circle cx="50" cy="50" r="20" fill="none" stroke="hsl(var(--primary))" strokeWidth="1.2" opacity="0.6" />
      {/* Detalhe grego — meandro circular simplificado */}
      <circle cx="50" cy="50" r="12" fill="none" stroke="hsl(var(--sun-glow))" strokeWidth="0.8" opacity="0.7" strokeDasharray="2 2" />
      <circle cx="50" cy="50" r="4" fill="hsl(var(--sun-glow))" />
    </svg>
  );
};
