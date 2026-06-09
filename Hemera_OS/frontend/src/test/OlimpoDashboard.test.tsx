import React from "react";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import { MemoryRouter } from "react-router-dom";
import OlimpoDashboard from "../pages/OlimpoDashboard";

// Mock do Recharts para evitar erros de renderização no JSDOM
vi.mock("recharts", async (importOriginal) => {
  const original = await importOriginal<any>();
  return {
    ...original,
    ResponsiveContainer: ({ children }: any) => <div data-testid="responsive-container">{children}</div>,
    BarChart: ({ children }: any) => <div data-testid="bar-chart">{children}</div>,
    Bar: () => <div data-testid="bar" />,
    XAxis: () => <div data-testid="xaxis" />,
    YAxis: () => <div data-testid="yaxis" />,
    CartesianGrid: () => <div data-testid="cartesian-grid" />,
    Tooltip: () => <div data-testid="tooltip" />,
    Legend: () => <div data-testid="legend" />,
    AreaChart: ({ children }: any) => <div data-testid="area-chart">{children}</div>,
    Area: () => <div data-testid="area" />,
    Line: () => <div data-testid="line" />,
  };
});

// Mock da biblioteca Sonner (toast)
vi.mock("sonner", () => ({
  toast: {
    success: vi.fn(),
    error: vi.fn(),
    info: vi.fn(),
    promise: vi.fn().mockImplementation((promise) => promise),
  },
}));

import { useState, useEffect } from "react";

let mockParams = new URLSearchParams();
const listeners = new Set<(params: URLSearchParams) => void>();

const setMockParams = (newParams: any) => {
  console.log("MOCK: setMockParams called with", newParams);
  mockParams = new URLSearchParams(newParams as any);
  console.log("MOCK: new mockParams is", mockParams.toString());
  console.log("MOCK: notifying", listeners.size, "listeners");
  listeners.forEach((l) => l(mockParams));
};

vi.mock("react-router-dom", async (importOriginal) => {
  const original = await importOriginal<any>();
  return {
    ...original,
    useSearchParams: () => {
      const [params, setParams] = useState(mockParams);
      console.log("MOCK: useSearchParams hook state is", params.toString());
      useEffect(() => {
        listeners.add(setParams);
        return () => {
          listeners.delete(setParams);
        };
      }, []);
      return [params, setMockParams] as const;
    },
  };
});

const renderDashboard = (initialEntries = ["/"]) => {
  // Inicializa os mockParams com a primeira entrada
  if (initialEntries && initialEntries.length > 0) {
    const url = new URL(initialEntries[0], "http://localhost");
    mockParams = new URLSearchParams(url.search);
  } else {
    mockParams = new URLSearchParams();
  }
  return render(
    <MemoryRouter initialEntries={initialEntries}>
      <OlimpoDashboard />
    </MemoryRouter>
  );
};

const clickElement = (element: HTMLElement) => {
  fireEvent.pointerDown(element);
  fireEvent.mouseDown(element);
  fireEvent.click(element);
};

describe("OlimpoDashboard Component Tests", () => {
  it("should render Olimpo Dashboard successfully with default layout", () => {
    renderDashboard();
    
    // Verifica cabeçalhos principais do Olimpo
    expect(screen.getByText("CENTRAL ADMIN • OLIMPO")).toBeInTheDocument();
    expect(screen.getByText("Dashboard de Gestão")).toBeInTheDocument();
    expect(screen.getByText("Olimpo")).toBeInTheDocument();
    expect(screen.getByText("SISTEMA ONLINE")).toBeInTheDocument();
  });

  it("should render tabs and switch to Matrículas tab", async () => {
    renderDashboard();

    // Encontra os botões de tabulação
    const tabOverview = screen.getByText("Visão Geral");
    const tabMatriculas = screen.getByText("Matrículas & Turmas");
    
    expect(tabOverview).toBeInTheDocument();
    expect(tabMatriculas).toBeInTheDocument();

    // Clica na tab de Matrículas
    clickElement(tabMatriculas);

    // Espera que a seção de matrículas apareça na tela
    await waitFor(() => {
      expect(screen.getByText("Nova Matrícula")).toBeInTheDocument();
      expect(screen.getByText("Alunos Matriculados")).toBeInTheDocument();
      expect(screen.getByText("Atribuição Docente")).toBeInTheDocument();
    });
  });

  it("should filter the student enrollments table based on search input", async () => {
    renderDashboard();
    
    // Vai para a tab de matrículas
    clickElement(screen.getByText("Matrículas & Turmas"));

    // Verifica que alguns estudantes mockados iniciais estão na tela
    await waitFor(() => {
      expect(screen.getByText("Ian Santos")).toBeInTheDocument();
      expect(screen.getByText("Beatriz Sousa")).toBeInTheDocument();
    });

    // Busca o input de pesquisa
    const searchInput = screen.getByPlaceholderText("Pesquisar...");
    
    // Digita "Beatriz"
    fireEvent.change(searchInput, { target: { value: "Beatriz" } });

    // Espera filtrar
    await waitFor(() => {
      expect(screen.getByText("Beatriz Sousa")).toBeInTheDocument();
      expect(screen.queryByText("Ian Santos")).not.toBeInTheDocument();
    });
  });

  it("should allow registering a new student through the enrollment form", async () => {
    renderDashboard();
    
    clickElement(screen.getByText("Matrículas & Turmas"));

    // Preenche o formulário de Nova Matrícula
    let nomeInput!: HTMLElement;
    let emailInput!: HTMLElement;
    let submitBtn!: HTMLElement;

    await waitFor(() => {
      nomeInput = screen.getByLabelText("Nome do Aluno");
      emailInput = screen.getByLabelText("E-mail Escolar");
      submitBtn = screen.getByRole("button", { name: /Concluir Matrícula/i });
    });

    fireEvent.change(nomeInput, { target: { value: "Luiza Alencar" } });
    fireEvent.change(emailInput, { target: { value: "luiza.alencar@escola.pt" } });
    
    // Submete o formulário
    fireEvent.click(submitBtn);

    // Verifica que o novo aluno foi adicionado à tabela
    await waitFor(() => {
      expect(screen.getByText("Luiza Alencar")).toBeInTheDocument();
      expect(screen.getByText("luiza.alencar@escola.pt")).toBeInTheDocument();
    });
  });

  it("should allow deleting a student from the enrollments list", async () => {
    renderDashboard();
    
    clickElement(screen.getByText("Matrículas & Turmas"));

    let rows: HTMLElement[] = [];
    // Encontra a linha que contém "Ian Santos"
    await waitFor(() => {
      rows = screen.getAllByRole("row");
      const ianRow = rows.find(row => row.textContent?.includes("Ian Santos"));
      expect(ianRow).toBeDefined();
    });

    const ianRow = rows.find(row => row.textContent?.includes("Ian Santos"))!;
    // Clica no botão de lixeira dentro dessa linha
    const deleteBtn = ianRow.querySelector("button");
    expect(deleteBtn).toBeDefined();
    
    fireEvent.click(deleteBtn!);

    // Verifica se "Ian Santos" foi removido
    await waitFor(() => {
      expect(screen.queryByText("Ian Santos")).not.toBeInTheDocument();
    });
  });

  it("should update AI calibration sliders and switches", async () => {
    renderDashboard();
    
    // Navega para calibração
    clickElement(screen.getByText("Calibração ZIOS/Rede"));

    // Verifica se os elementos estão presentes
    await waitFor(() => {
      expect(screen.getByText("Calibração ZIOS IA")).toBeInTheDocument();
      expect(screen.getByText("Controle de Banda & Latência")).toBeInTheDocument();
    });

    // Verifica o switch preditivo
    const predictiveSwitch = screen.getByTestId("predictive-switch");
    expect(predictiveSwitch).toBeInTheDocument();
    
    // Clica para alterar estado do switch
    fireEvent.click(predictiveSwitch);

    // Verifica o switch de compressão de rede
    const compressSwitch = screen.getByTestId("network-compress-switch");
    expect(compressSwitch).toBeInTheDocument();
    
    fireEvent.click(compressSwitch);
  });
});
