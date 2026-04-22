import React from 'react';

// O segredo está aqui: "export const" (Exportação nomeada)
export const AuroraBackground: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  return (
    <div className="min-h-screen w-full bg-[#FAFAFA] relative overflow-hidden">
      {/* Efeito Blur Flutuante */}
      <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-secondary/20 rounded-full blur-[120px] pointer-events-none" />
      <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-primary/20 rounded-full blur-[120px] pointer-events-none" />
      
      {/* Conteúdo Glassmorphism */}
      <div className="relative z-10 w-full h-full">
        {children}
      </div>
    </div>
  );
};