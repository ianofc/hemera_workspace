import React from 'react';
import { describe, it, expect, beforeEach } from "vitest";
import { render, screen, act } from "@testing-library/react";
import { LyceumProvider, useLyceum } from "../contexts/LyceumContext";

// Componente helper para expor os estados do context nos testes
const TestConsumer: React.FC = () => {
  const { xp, level, xpForNextLevel, badges, trails, completeLesson, addXp } = useLyceum();

  return (
    <div>
      <div data-testid="xp-value">{xp}</div>
      <div data-testid="level-value">{level}</div>
      <div data-testid="xp-next">{xpForNextLevel}</div>
      <div data-testid="unlocked-badges">
        {badges.filter(b => b.unlocked).map(b => b.id).join(',')}
      </div>
      <div data-testid="trail-progress">
        {trails.map(t => `${t.id}:${t.progress}`).join(',')}
      </div>
      <button 
        data-testid="add-xp-btn" 
        onClick={() => addXp(350)}
      >
        Add XP
      </button>
      <button 
        data-testid="complete-lesson-btn" 
        onClick={() => completeLesson(1, 101, 1001)}
      >
        Complete Lesson 1001
      </button>
    </div>
  );
};

describe("LyceumProvider and Gamification Tests", () => {
  beforeEach(() => {
    localStorage.clear();
  });

  it("should initialize gamification state with default values", () => {
    render(
      <LyceumProvider>
        <TestConsumer />
      </LyceumProvider>
    );

    expect(screen.getByTestId("xp-value").textContent).toBe("0");
    expect(screen.getByTestId("level-value").textContent).toBe("1");
    expect(screen.getByTestId("xp-next").textContent).toBe("300");
    // O primeiro badge ('badge-welcome') já começa desbloqueado
    expect(screen.getByTestId("unlocked-badges").textContent).toContain("badge-welcome");
    // Os progressos das trilhas começam em 0
    expect(screen.getByTestId("trail-progress").textContent).toContain("1:0");
  });

  it("should handle XP addition and level up correctly", async () => {
    render(
      <LyceumProvider>
        <TestConsumer />
      </LyceumProvider>
    );

    const addXpBtn = screen.getByTestId("add-xp-btn");
    
    await act(async () => {
      addXpBtn.click();
    });

    // XP = 350, Limite nível 1 = 300 XP.
    // 350 - 300 = 50 XP restante. Level deve ir para 2.
    // Damos um pequeno delay por conta do setTimeout interno de level-up
    await new Promise((resolve) => setTimeout(resolve, 150));

    expect(screen.getByTestId("xp-value").textContent).toBe("50");
    expect(screen.getByTestId("level-value").textContent).toBe("2");
    expect(screen.getByTestId("xp-next").textContent).toBe("600"); // Nível 2 precisa de 600 XP (2 * 300)
    
    // Deve desbloquear badge-level-2
    expect(screen.getByTestId("unlocked-badges").textContent).toContain("badge-level-2");
  });

  it("should award XP and update progress when completing a lesson", async () => {
    render(
      <LyceumProvider>
        <TestConsumer />
      </LyceumProvider>
    );

    const completeBtn = screen.getByTestId("complete-lesson-btn");

    await act(async () => {
      completeBtn.click();
    });

    // A lição 1001 dá 50 XP
    expect(screen.getByTestId("xp-value").textContent).toBe("50");
    
    // Deve desbloquear badge-first-lesson
    expect(screen.getByTestId("unlocked-badges").textContent).toContain("badge-first-lesson");
    
    // Matemática Avançada (ID: 1) tem 5 lições no total, completar 1 deve dar 20%
    expect(screen.getByTestId("trail-progress").textContent).toContain("1:20");
  });
});
