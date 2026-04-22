import React from 'react';

import { AuroraBackground } from './AuroraBackground'; 
import { Sidebar } from './Sidebar';

export const AppLayout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  return (
    <AuroraBackground>
      {/* O Layout engloba a Sidebar flutuante e a área de conteúdo */}
      <Sidebar />
      
      {/* Área principal de conteúdo, empurrada para a direita para não ficar sob a Sidebar */}
      <main className="pl-24 pr-8 py-8 min-h-screen w-full transition-all duration-300">
        <div className="max-w-7xl mx-auto h-full">
          {children}
        </div>
      </main>
    </AuroraBackground>
  );
};