import React from "react";
import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { Polis } from "../pages/Polis";

// Mock mutable role for multi-tenancy role-based UI testing
let mockRole: 'professor' | 'aluno' = 'professor';

// Mock authorization and toast hooks
vi.mock("@/hooks/useAuth", () => ({
  useAuth: () => ({
    user: { id: "user-123", email: "usuario@hemera.os", role: mockRole },
    role: mockRole,
    login: vi.fn(),
    logout: vi.fn(),
  }),
}));

vi.mock("@/hooks/use-toast", () => ({
  useToast: () => ({
    toast: vi.fn(),
    dismiss: vi.fn(),
    toasts: [],
  }),
}));

describe("Painel de Comunidade - Polis", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    mockRole = "professor"; // default to professor for standard tests
  });

  const renderComponent = () => {
    return render(
      <MemoryRouter>
        <Polis />
      </MemoryRouter>
    );
  };

  it("deve renderizar a estrutura inicial do Polis com título e seletores", () => {
    renderComponent();
    
    // Verifica cabeçalho e título
    expect(screen.getByText("Comunidade da Turma")).toBeInTheDocument();
    expect(screen.getByText("Hemera Polis")).toBeInTheDocument();

    // Verifica seletores de escola e turma
    expect(screen.getByTestId("school-selector")).toBeInTheDocument();
    expect(screen.getByTestId("class-selector")).toBeInTheDocument();

    // Verifica as abas disponíveis
    expect(screen.getByTestId("tab-mural")).toBeInTheDocument();
    expect(screen.getByTestId("tab-feed")).toBeInTheDocument();
    expect(screen.getByTestId("tab-arquivos")).toBeInTheDocument();
  });

  it("deve aplicar a segmentação multi-tenancy alternando entre escolas e atualizando as turmas", async () => {
    renderComponent();
    
    const schoolSelector = screen.getByTestId("school-selector") as HTMLSelectElement;
    const classSelector = screen.getByTestId("class-selector") as HTMLSelectElement;

    // Escola padrão é Alpha, e a primeira turma deve ser do 9º Ano A
    expect(schoolSelector.value).toBe("school-alpha");
    expect(classSelector.value).toBe("class-alpha-9a");

    // Altera para a escola Beta
    fireEvent.change(schoolSelector, { target: { value: "school-beta" } });
    
    // A turma ativa deve mudar automaticamente para a primeira turma da escola Beta
    expect(schoolSelector.value).toBe("school-beta");
    expect(classSelector.value).toBe("class-beta-eng1");
  });

  it("deve renderizar o formulário de aviso se o usuário for Professor", () => {
    mockRole = "professor";
    renderComponent();

    // O professor deve ver o formulário de fixar avisos importantes
    expect(screen.getByText("Fixar Novo Aviso no Mural Oficial")).toBeInTheDocument();
    expect(screen.getByPlaceholderText("Título do aviso...")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /Publicar Comunicado/i })).toBeInTheDocument();
  });

  it("deve OCULTAR o formulário de novos avisos no mural se o usuário for Aluno", () => {
    mockRole = "aluno";
    renderComponent();

    // O aluno NÃO deve ver o formulário para adicionar novos avisos (apenas o professor cria no Mural)
    expect(screen.queryByText("Fixar Novo Aviso no Mural Oficial")).not.toBeInTheDocument();
    expect(screen.queryByPlaceholderText("Título do aviso...")).not.toBeInTheDocument();
  });

  it("deve interagir com o Feed da Comunidade: postar, curtir e comentar", async () => {
    mockRole = "aluno";
    renderComponent();

    // Navegar para a aba de Feed
    const feedTab = screen.getByTestId("tab-feed");
    fireEvent.click(feedTab);

    // Verifica se a área de feed carregou
    expect(screen.getByTestId("tab-content-feed")).toBeInTheDocument();
    
    // Encontrar campo de texto do feed e publicar post
    const textarea = screen.getByTestId("feed-textarea");
    fireEvent.change(textarea, { target: { value: "Olá comunidade! Novo post de teste aqui." } });
    
    const publishBtn = screen.getByTestId("publish-post-btn");
    fireEvent.click(publishBtn);

    // A postagem do feed deve aparecer na tela
    expect(screen.getByText("Olá comunidade! Novo post de teste aqui.")).toBeInTheDocument();

    // Tenta curtir a postagem criada
    // Como a nova postagem terá um id dinâmico baseado em Date.now(), vamos buscá-la pelo texto e curtir o botão correspondente
    const likeButtons = screen.getAllByRole("button", { name: /Curtidas/i });
    
    // O post recém-criado deve iniciar com 0 curtidas
    expect(likeButtons[0].textContent).toContain("0 Curtidas");

    // Clica no botão de curtir
    fireEvent.click(likeButtons[0]);

    // O contador de curtidas deve incrementar para 1
    expect(likeButtons[0].textContent).toContain("1 Curtidas");
  });

  it("deve interagir com a aba de Arquivos: pesquisar e simular upload de material", async () => {
    mockRole = "professor";
    renderComponent();

    // Navegar para a aba de arquivos
    const arquivosTab = screen.getByTestId("tab-arquivos");
    fireEvent.click(arquivosTab);

    expect(screen.getByTestId("tab-content-arquivos")).toBeInTheDocument();

    // Pesquisar por um arquivo inexistente para ver o feedback visual
    const searchInput = screen.getByPlaceholderText("Pesquisar arquivos por nome...");
    fireEvent.change(searchInput, { target: { value: "arquivo_inexistente_123" } });
    
    expect(screen.getByText("Nenhum arquivo encontrado nesta pasta.")).toBeInTheDocument();

    // Limpa a busca
    fireEvent.change(searchInput, { target: { value: "" } });

    // Clicar para abrir formulário de upload
    const uploadToggle = screen.getByTestId("upload-toggle-btn");
    fireEvent.click(uploadToggle);

    // Preencher informações do arquivo
    const fileNameInput = screen.getByPlaceholderText("Ex: roteiro-seminario");
    fireEvent.change(fileNameInput, { target: { value: "manual-da-disciplina" } });

    const submitFileBtn = screen.getByTestId("submit-file-btn");
    fireEvent.click(submitFileBtn);

    // O arquivo recém adicionado deve aparecer listado
    expect(screen.getByText("manual-da-disciplina.pdf")).toBeInTheDocument();
  });
});
