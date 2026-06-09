import React from 'react';
import { useLyceum } from '../../contexts/LyceumContext';
import { Award, Zap, Star, ShieldAlert } from 'lucide-react';
import { motion } from 'framer-motion';

export const GamificationStats: React.FC = () => {
  const { xp, level, xpForNextLevel, badges } = useLyceum();
  const xpPercentage = Math.min(100, Math.max(0, Math.round((xp / xpForNextLevel) * 100)));

  return (
    <div className="space-y-6">
      {/* Nível e Barra de XP */}
      <div className="relative p-6 overflow-hidden border bg-white/60 backdrop-blur-xl rounded-3xl border-glass-border shadow-md">
        <div className="absolute top-0 right-0 w-32 h-32 rounded-full bg-primary/10 blur-2xl -mr-8 -mt-8" />
        
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-3">
            <div className="flex items-center justify-center w-12 h-12 text-white shadow-md rounded-2xl bg-gradient-to-br from-primary to-secondary">
              <Zap className="w-6 h-6 animate-pulse" />
            </div>
            <div>
              <p className="text-xs font-bold text-muted-foreground uppercase tracking-widest">Nível Atual</p>
              <h4 className="text-2xl font-bold text-foreground">Nível {level}</h4>
            </div>
          </div>
          <div className="text-right">
            <span className="text-xs font-bold text-muted-foreground">Progresso do Nível</span>
            <p className="text-sm font-bold text-primary">{xp} / {xpForNextLevel} XP</p>
          </div>
        </div>

        {/* Barra de Progresso */}
        <div className="relative w-full h-4 bg-gray-200/50 rounded-full overflow-hidden border border-gray-100">
          <motion.div
            initial={{ width: 0 }}
            animate={{ width: `${xpPercentage}%` }}
            transition={{ duration: 0.8, ease: 'easeOut' }}
            className="h-full rounded-full bg-gradient-to-r from-primary via-secondary to-success shadow-inner"
          />
        </div>
        <p className="mt-2 text-xs text-muted-foreground text-right">Faltam {xpForNextLevel - xp} XP para o nível {level + 1}!</p>
      </div>

      {/* Grid de Badges */}
      <div className="p-6 border bg-white/60 backdrop-blur-xl rounded-3xl border-glass-border shadow-md">
        <div className="flex items-center justify-between mb-6">
          <h3 className="flex items-center gap-2 text-lg font-bold text-foreground">
            <Award className="w-5 h-5 text-primary" /> Conquistas & Badges
          </h3>
          <span className="px-2.5 py-1 text-xs font-bold rounded-full bg-primary/10 text-primary border border-primary/20">
            {badges.filter(b => b.unlocked).length} / {badges.length} Desbloqueados
          </span>
        </div>

        <div className="grid grid-cols-2 gap-4 sm:grid-cols-3 md:grid-cols-3 lg:grid-cols-6">
          {badges.map((badge) => (
            <motion.div
              key={badge.id}
              whileHover={{ scale: badge.unlocked ? 1.05 : 1.0 }}
              className={`relative flex flex-col items-center p-4 border rounded-2xl transition-all text-center h-full justify-between ${
                badge.unlocked
                  ? 'bg-card border-success/30 shadow-sm hover:shadow-md'
                  : 'bg-muted/40 border-border/40 opacity-60'
              }`}
            >
              {/* Badge Icon / Lock */}
              <div className={`relative flex items-center justify-center w-14 h-14 rounded-full text-3xl mb-3 shadow-inner ${
                badge.unlocked
                  ? 'bg-gradient-to-br from-primary/10 to-secondary/10 border border-primary/20'
                  : 'bg-gray-100 border border-dashed border-gray-300'
              }`}>
                {badge.unlocked ? (
                  <span>{badge.icon}</span>
                ) : (
                  <span className="text-gray-400 select-none">🔒</span>
                )}
                
                {badge.unlocked && (
                  <span className="absolute bottom-0 right-0 flex w-3 h-3">
                    <span className="absolute inline-flex w-full h-full rounded-full opacity-75 animate-ping bg-success" />
                    <span className="relative inline-flex w-3 h-3 rounded-full bg-success" />
                  </span>
                )}
              </div>

              <div>
                <h5 className="text-xs font-bold text-foreground line-clamp-1">{badge.title}</h5>
                <p className="mt-1 text-[10px] text-muted-foreground leading-tight line-clamp-2">
                  {badge.description}
                </p>
              </div>

              {badge.unlocked && badge.unlockedAt && (
                <span className="mt-2 text-[8px] text-muted-foreground opacity-70">
                  {new Date(badge.unlockedAt).toLocaleDateString()}
                </span>
              )}
            </motion.div>
          ))}
        </div>
      </div>
    </div>
  );
};
