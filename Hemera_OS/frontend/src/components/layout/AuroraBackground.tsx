const AuroraBackground = () => (
  <div className="fixed inset-0 z-0 overflow-hidden pointer-events-none">
    <div className="absolute -top-[10%] -left-[10%] w-[600px] h-[600px] rounded-full mix-blend-multiply blur-[120px] opacity-30 animate-float bg-secondary" />
    <div
      className="absolute top-[10%] -right-[10%] w-[500px] h-[500px] rounded-full mix-blend-multiply blur-[120px] opacity-30 animate-float bg-primary"
      style={{ animationDelay: "2s" }}
    />
    <div
      className="absolute -bottom-[10%] left-[20%] w-[600px] h-[600px] rounded-full mix-blend-multiply blur-[120px] opacity-30 animate-float bg-accent"
      style={{ animationDelay: "4s" }}
    />
  </div>
);

export default AuroraBackground;
