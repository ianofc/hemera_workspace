import React from 'react';
import { AppLayout } from '../components/layout/AppLayout';
import { MoodleSync } from '../components/lyceum/MoodleSync';
import { GamificationStats } from '../components/lyceum/GamificationStats';

const AlunoNotas: React.FC = () => {
  return (
    <AppLayout role="aluno">
      <div className="max-w-[1600px] mx-auto px-6 space-y-8 pb-20">
        
        {/* Barra de XP */}
        <section>
          <GamificationStats />
        </section>

        {/* Integração Moodle */}
        <section>
          <MoodleSync />
        </section>

      </div>
    </AppLayout>
  );
};

export default AlunoNotas;
