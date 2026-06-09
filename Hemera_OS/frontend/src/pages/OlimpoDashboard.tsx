import React, { useState, useEffect } from "react";
import { useSearchParams } from "react-router-dom";
import { AppLayout } from "../components/layout/AppLayout";
import { 
  Home, Users, BookOpen, Settings, Brain, Zap, Shield, Globe, Cpu, 
  Plus, Search, Download, CheckCircle, AlertTriangle, Play, RefreshCw, 
  Trash2, Edit, Award, UserCheck, Eye, EyeOff, Save
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Switch } from "@/components/ui/switch";
import { Slider } from "@/components/ui/slider";
import { Badge } from "@/components/ui/badge";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { toast } from "sonner";
import { 
  ResponsiveContainer, BarChart, Bar, XAxis, YAxis, CartesianGrid, 
  Tooltip, Legend, LineChart, Line, AreaChart, Area 
} from "recharts";

// Mock de dados iniciais
const INITIAL_MATRICULAS = [
  { id: "1", nome: "Ian Santos", email: "ian@escola.pt", turma: "9º Ano A", curso: "Fundamental II", status: "Ativo" },
  { id: "2", nome: "Beatriz Sousa", email: "beatriz@escola.pt", turma: "9º Ano A", curso: "Fundamental II", status: "Ativo" },
  { id: "3", nome: "Carlos Souza", email: "carlos@escola.pt", turma: "8º Ano B", curso: "Fundamental II", status: "Pendente" },
  { id: "4", nome: "Mariana Costa", email: "mariana@escola.pt", turma: "3ª Série A", curso: "Ensino Médio", status: "Ativo" },
  { id: "5", nome: "Diogo Oliveira", email: "diogo@escola.pt", turma: "1º Período", curso: "Creche/Pré", status: "Inativo" },
];

const INITIAL_TURMAS = [
  { id: "t1", nome: "9º Ano A", curso: "Fundamental II", professor: "Prof. Alexandre", disciplina: "Matemática" },
  { id: "t2", nome: "8º Ano B", curso: "Fundamental II", professor: "Profa. Cláudia", disciplina: "Física" },
  { id: "t3", nome: "3ª Série A", curso: "Ensino Médio", professor: "Prof. Alexandre", disciplina: "Física" },
  { id: "t4", nome: "1º Período", curso: "Creche/Pré", professor: "Profa. Juliana", disciplina: "Artes" },
];

const INITIAL_DIARIOS = [
  { id: "d1", professor: "Prof. Alexandre", turma: "9º Ano A", disciplina: "Matemática", data: "2026-05-27", conteudo: "Introdução às Equações do 2º Grau e problemas práticos.", presenca: "96%" },
  { id: "d2", professor: "Profa. Cláudia", turma: "8º Ano B", disciplina: "Física", data: "2026-05-26", conteudo: "Óptica geométrica e refração da luz em lentes.", presenca: "91%" },
  { id: "d3", professor: "Prof. Alexandre", turma: "3ª Série A", disciplina: "Física", data: "2026-05-25", conteudo: "Eletrodinâmica: Leis de Ohm e circuitos complexos.", presenca: "94%" },
  { id: "d4", professor: "Profa. Juliana", turma: "1º Período", disciplina: "Artes", data: "2026-05-27", conteudo: "Pintura a dedo com cores primárias e coordenação motora.", presenca: "100%" },
];

const PERFORMANCE_DATA = [
  { turma: "9º Ano A", Matematica: 82, Fisica: 78, Portugues: 85, presenca: 96 },
  { turma: "8º Ano B", Matematica: 75, Fisica: 74, Portugues: 80, presenca: 91 },
  { turma: "3ª Série A", Matematica: 88, Fisica: 84, Portugues: 90, presenca: 94 },
  { turma: "1º Período", Matematica: 95, Fisica: 0, Portugues: 95, presenca: 100 },
];

const ENGAGEMENT_DATA = [
  { dia: "Seg", engajamento: 65, acessos: 320, latencia: 42 },
  { dia: "Ter", engajamento: 72, acessos: 410, latencia: 38 },
  { dia: "Qua", engajamento: 85, acessos: 490, latencia: 35 },
  { dia: "Qui", engajamento: 78, acessos: 460, latencia: 37 },
  { dia: "Sex", engajamento: 90, acessos: 520, latencia: 32 },
];

export default function OlimpoDashboard() {
  const [searchParams, setSearchParams] = useSearchParams();
  const currentTab = searchParams.get("tab") || "overview";

  // Estados locais para controle de dados
  const [matriculas, setMatriculas] = useState(INITIAL_MATRICULAS);
  const [turmas, setTurmas] = useState(INITIAL_TURMAS);
  const [diarios, setDiarios] = useState(INITIAL_DIARIOS);
  
  // Estados para pesquisa/filtro
  const [searchMatricula, setSearchMatricula] = useState("");
  const [filterTurmaDiarios, setFilterTurmaDiarios] = useState("TODAS");

  // Estado para cadastro de nova matrícula
  const [novaMatricula, setNovaMatricula] = useState({
    nome: "",
    email: "",
    turma: "9º Ano A",
    curso: "Fundamental II",
    status: "Ativo"
  });

  // Estado para nova atribuição de turma/professor
  const [novaAtribuicao, setNovaAtribuicao] = useState({
    turmaId: "t1",
    professor: "",
    disciplina: ""
  });

  // Estados de Calibração IA / Rede
  const [iaConfig, setIaConfig] = useState({
    temperatura: 0.3,
    maxTokens: 500,
    predictiveModel: true,
    aiKey: "zios_sk_••••••••••••••••••••3a8c",
  });
  const [showAiKey, setShowAiKey] = useState(false);

  const [redeConfig, setRedeConfig] = useState({
    prioridadeBanda: 80,
    compressaoVideo: true,
    latenciaAlvo: 35,
    statusRede: "Excelente",
  });

  // Alteração de Abas
  const handleTabChange = (val: string) => {
    setSearchParams({ tab: val });
  };

  useEffect(() => {
    // Sincroniza a tab da URL se houver alteração externa
    const tabParam = searchParams.get("tab");
    if (!tabParam) {
      setSearchParams({ tab: "overview" });
    }
  }, [searchParams, setSearchParams]);

  // Função para criar matrícula
  const handleCreateMatricula = (e: React.FormEvent) => {
    e.preventDefault();
    if (!novaMatricula.nome || !novaMatricula.email) {
      toast.error("Por favor, preencha todos os campos.");
      return;
    }

    const novoItem = {
      id: String(matriculas.length + 1),
      ...novaMatricula
    };

    setMatriculas([novoItem, ...matriculas]);
    toast.success("Matrícula realizada com sucesso!", {
      description: `${novaMatricula.nome} enturmado em ${novaMatricula.turma}`
    });

    setNovaMatricula({
      nome: "",
      email: "",
      turma: "9º Ano A",
      curso: "Fundamental II",
      status: "Ativo"
    });
  };

  // Função para salvar atribuição de professor/disciplina
  const handleSaveAtribuicao = (e: React.FormEvent) => {
    e.preventDefault();
    if (!novaAtribuicao.professor || !novaAtribuicao.disciplina) {
      toast.error("Preencha professor e disciplina.");
      return;
    }

    const updatedTurmas = turmas.map(t => {
      if (t.id === novaAtribuicao.turmaId) {
        return {
          ...t,
          professor: novaAtribuicao.professor,
          disciplina: novaAtribuicao.disciplina
        };
      }
      return t;
    });

    setTurmas(updatedTurmas);
    toast.success("Atribuição de professor salva!", {
      description: `Professor ${novaAtribuicao.professor} alocado em ${turmas.find(t => t.id === novaAtribuicao.turmaId)?.nome}`
    });

    setNovaAtribuicao({
      turmaId: "t1",
      professor: "",
      disciplina: ""
    });
  };

  // Deletar matrícula
  const handleDeleteMatricula = (id: string) => {
    setMatriculas(matriculas.filter(m => m.id !== id));
    toast.info("Matrícula removida.");
  };

  // Alterar status de matrícula
  const handleToggleStatus = (id: string) => {
    setMatriculas(matriculas.map(m => {
      if (m.id === id) {
        const nextStatus = m.status === "Ativo" ? "Inativo" : m.status === "Inativo" ? "Pendente" : "Ativo";
        return { ...m, status: nextStatus };
      }
      return m;
    }));
    toast.info("Status da matrícula atualizado.");
  };

  // Salvar calibração de IA/Rede
  const handleSaveCalibracao = () => {
    toast.success("Parâmetros do sistema calibrados!", {
      description: "As diretivas da IA ZIOS e de tráfego de rede escolar foram recarregadas no barramento principal."
    });
  };

  // Filtros de matrículas
  const filteredMatriculas = matriculas.filter(m => 
    m.nome.toLowerCase().includes(searchMatricula.toLowerCase()) ||
    m.email.toLowerCase().includes(searchMatricula.toLowerCase()) ||
    m.turma.toLowerCase().includes(searchMatricula.toLowerCase())
  );

  // Filtros de diários
  const filteredDiarios = filterTurmaDiarios === "TODAS" 
    ? diarios 
    : diarios.filter(d => d.turma === filterTurmaDiarios);

  return (
    <AppLayout>
      <div className="max-w-[1600px] mx-auto px-4 md:px-8 pb-20 space-y-8" data-testid="olimpo-container">
        
        {/* Cabeçalho */}
        <section className="relative rounded-[2.5rem] overflow-hidden shadow-2xl min-h-[160px] group border border-glass-border">
          <div className="absolute inset-0 bg-gradient-to-r from-[#1E293B] via-[#0F172A] to-[#1E293B] opacity-95" />
          <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top_right,_var(--tw-gradient-stops))] from-amber-500/10 via-transparent to-transparent" />
          
          <div className="absolute inset-0 flex items-center px-8 md:px-12">
            <div className="flex flex-col md:flex-row md:items-center justify-between w-full gap-4">
              <div>
                <span className="inline-flex items-center gap-1.5 px-3 py-1 text-xs font-bold tracking-wider uppercase border rounded-full bg-amber-500/10 border-amber-500/30 text-amber-500 mb-2">
                  <Shield className="w-3.5 h-3.5" /> CENTRAL ADMIN • OLIMPO
                </span>
                <h1 className="text-3xl font-extrabold text-white tracking-tight md:text-4xl">
                  Dashboard de Gestão <span className="text-transparent bg-clip-text bg-gradient-to-r from-amber-400 to-orange-400">Olimpo</span>
                </h1>
                <p className="text-slate-400 text-sm mt-1">Gerencie matrículas, acompanhe relatórios de diários e controle as redes de IA do Hemera OS.</p>
              </div>

              <div className="flex items-center gap-3">
                <Badge variant="outline" className="bg-emerald-500/10 border-emerald-500/20 text-emerald-400 px-3 py-1 text-xs font-bold flex items-center gap-1">
                  <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping" />
                  SISTEMA ONLINE
                </Badge>
                <button 
                  onClick={() => {
                    toast.promise(new Promise((resolve) => setTimeout(resolve, 1000)), {
                      loading: 'Sincronizando barramentos...',
                      success: 'Todos os diários e matrículas atualizados!',
                      error: 'Erro na sincronização.',
                    });
                  }}
                  className="p-2.5 rounded-xl border border-slate-700 bg-slate-800 text-slate-300 hover:text-white hover:bg-slate-700 transition-colors"
                  title="Sincronizar barramento de dados"
                >
                  <RefreshCw className="w-4 h-4" />
                </button>
              </div>
            </div>
          </div>
        </section>

        {/* Abas */}
        <Tabs value={currentTab} onValueChange={handleTabChange} className="space-y-6">
          <TabsList className="grid grid-cols-2 md:grid-cols-5 h-auto p-1.5 bg-slate-900/60 border border-slate-800 rounded-2xl max-w-4xl">
            <TabsTrigger value="overview" className="rounded-xl py-2.5 text-xs font-bold transition-all data-[state=active]:bg-amber-500 data-[state=active]:text-white">
              <Home className="w-4 h-4 mr-2" /> Visão Geral
            </TabsTrigger>
            <TabsTrigger value="matriculas" className="rounded-xl py-2.5 text-xs font-bold transition-all data-[state=active]:bg-amber-500 data-[state=active]:text-white">
              <Users className="w-4 h-4 mr-2" /> Matrículas & Turmas
            </TabsTrigger>
            <TabsTrigger value="diarios" className="rounded-xl py-2.5 text-xs font-bold transition-all data-[state=active]:bg-amber-500 data-[state=active]:text-white">
              <BookOpen className="w-4 h-4 mr-2" /> Diários de Classe
            </TabsTrigger>
            <TabsTrigger value="relatorios" className="rounded-xl py-2.5 text-xs font-bold transition-all data-[state=active]:bg-amber-500 data-[state=active]:text-white">
              <Award className="w-4 h-4 mr-2" /> Notas & Presença
            </TabsTrigger>
            <TabsTrigger value="config" className="rounded-xl py-2.5 text-xs font-bold transition-all data-[state=active]:bg-amber-500 data-[state=active]:text-white">
              <Settings className="w-4 h-4 mr-2" /> Calibração ZIOS/Rede
            </TabsTrigger>
          </TabsList>

          {/* TAB 1: VISÃO GERAL (OVERVIEW) */}
          <TabsContent value="overview" className="space-y-6 outline-none">
            {/* Cards de Resumo */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
              {[
                { title: "Matrículas Ativas", value: matriculas.filter(m => m.status === "Ativo").length + " / " + matriculas.length, desc: "+12% em relação ao mês anterior", icon: Users, color: "text-amber-500" },
                { title: "Presença Geral", value: "95.2%", desc: "Consistente com a meta escolar", icon: UserCheck, color: "text-emerald-500" },
                { title: "Rendimento Médio", value: "82.5 / 100", desc: "Aumento de 2.4 pontos este ano", icon: Award, color: "text-indigo-500" },
                { title: "Latência ZIOS IA", value: redeConfig.latenciaAlvo + " ms", desc: "Status de Rede: " + redeConfig.statusRede, icon: Brain, color: "text-cyan-500" }
              ].map((card, idx) => (
                <Card key={idx} className="bg-white/60 backdrop-blur-xl border border-glass-border shadow-md rounded-2xl overflow-hidden hover:shadow-lg transition-shadow">
                  <CardHeader className="flex flex-row items-center justify-between pb-2 space-y-0">
                    <CardTitle className="text-xs font-bold text-slate-500 uppercase tracking-wider">{card.title}</CardTitle>
                    <card.icon className={`w-5 h-5 ${card.color}`} />
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-black text-slate-800">{card.value}</div>
                    <p className="text-[10px] font-medium text-slate-400 mt-1">{card.desc}</p>
                  </CardContent>
                </Card>
              ))}
            </div>

            {/* PentaIA ZIOS Notification */}
            <div className="relative overflow-hidden bg-white/60 backdrop-blur-xl rounded-2xl shadow-md p-6 border border-glass-border">
              <div className="absolute top-0 right-0 w-48 h-48 rounded-full bg-amber-500/5 blur-3xl -translate-y-1/2 translate-x-1/4" />
              <div className="relative z-10 flex flex-col md:flex-row items-start md:items-center gap-5">
                <div className="flex items-center justify-center w-12 h-12 rounded-2xl bg-gradient-to-br from-amber-400 to-orange-500 text-white shadow-md">
                  <Brain className="w-6 h-6 animate-pulse" />
                </div>
                <div className="flex-1">
                  <h3 className="flex items-center gap-2 text-base font-bold text-slate-800">
                    Sugestão de Calibração ZIOS IA
                    <span className="flex items-center gap-0.5 px-2 py-0.5 rounded-full bg-amber-100 border border-amber-200 text-amber-600 text-[9px] uppercase tracking-wider font-bold">
                      <Zap className="w-2.5 h-2.5" /> Recomendado
                    </span>
                  </h3>
                  <p className="mt-1 text-slate-600 text-xs leading-relaxed">
                    Identifiquei um pico de acessos escolares planejado para amanhã às 08:00 (Simulados Nacionais).
                    Recomendo ativar a <strong>Compressão de Pacotes de Vídeo</strong> e reduzir a <strong>Latência Alvo do ZIOS</strong> para 30ms para evitar gargalos nos diários online.
                  </p>
                </div>
                <Button 
                  onClick={() => {
                    setRedeConfig(prev => ({ ...prev, compressaoVideo: true, latenciaAlvo: 30 }));
                    toast.success("Calibração automática ZIOS efetuada!");
                  }}
                  className="bg-amber-500 hover:bg-amber-600 text-white font-bold text-xs px-4 py-2 rounded-xl transition-all shadow-md shadow-amber-500/20"
                >
                  Otimizar Agora
                </Button>
              </div>
            </div>

            {/* Gráficos de Performance e Engajamento */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Gráfico 1: Rendimento Escolar por Turma */}
              <Card className="bg-white/60 backdrop-blur-xl border border-glass-border shadow-md rounded-2xl">
                <CardHeader>
                  <CardTitle className="text-base font-bold text-slate-800">Rendimento Médio Geral por Turma</CardTitle>
                  <CardDescription className="text-xs">Notas médias em exames nas principais disciplinas</CardDescription>
                </CardHeader>
                <CardContent className="h-[300px]">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={PERFORMANCE_DATA} margin={{ top: 20, right: 10, left: -20, bottom: 0 }}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#F1F5F9" />
                      <XAxis dataKey="turma" stroke="#64748B" fontSize={11} tickLine={false} />
                      <YAxis stroke="#64748B" fontSize={11} domain={[0, 100]} tickLine={false} />
                      <Tooltip contentStyle={{ borderRadius: '12px', border: '1px solid #E2E8F0' }} />
                      <Legend verticalAlign="top" height={36} iconSize={10} iconType="circle" wrapperStyle={{ fontSize: '11px' }} />
                      <Bar dataKey="Matematica" name="Matemática" fill="#F59E0B" radius={[4, 4, 0, 0]} />
                      <Bar dataKey="Fisica" name="Física" fill="#3B82F6" radius={[4, 4, 0, 0]} />
                      <Bar dataKey="Portugues" name="Português" fill="#8B5CF6" radius={[4, 4, 0, 0]} />
                    </BarChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>

              {/* Gráfico 2: Engajamento & Acessos */}
              <Card className="bg-white/60 backdrop-blur-xl border border-glass-border shadow-md rounded-2xl">
                <CardHeader>
                  <CardTitle className="text-base font-bold text-slate-800">Acessos e Engajamento Semanal</CardTitle>
                  <CardDescription className="text-xs">Interações dos alunos no ecossistema digital Hemera</CardDescription>
                </CardHeader>
                <CardContent className="h-[300px]">
                  <ResponsiveContainer width="100%" height="100%">
                    <AreaChart data={ENGAGEMENT_DATA} margin={{ top: 20, right: 10, left: -20, bottom: 0 }}>
                      <defs>
                        <linearGradient id="colorEngage" x1="0" y1="0" x2="0" y2="1">
                          <stop offset="5%" stopColor="#F59E0B" stopOpacity={0.2}/>
                          <stop offset="95%" stopColor="#F59E0B" stopOpacity={0}/>
                        </linearGradient>
                      </defs>
                      <CartesianGrid strokeDasharray="3 3" stroke="#F1F5F9" />
                      <XAxis dataKey="dia" stroke="#64748B" fontSize={11} tickLine={false} />
                      <YAxis stroke="#64748B" fontSize={11} tickLine={false} />
                      <Tooltip contentStyle={{ borderRadius: '12px', border: '1px solid #E2E8F0' }} />
                      <Legend verticalAlign="top" height={36} iconSize={10} wrapperStyle={{ fontSize: '11px' }} />
                      <Area type="monotone" dataKey="engajamento" name="Engajamento (%)" stroke="#F59E0B" fillOpacity={1} fill="url(#colorEngage)" strokeWidth={2} />
                      <Line type="monotone" dataKey="acessos" name="Acessos Totais" stroke="#10B981" strokeWidth={2} dot={{ r: 4 }} />
                    </AreaChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          {/* TAB 2: MATRÍCULAS E TURMAS */}
          <TabsContent value="matriculas" className="space-y-6 outline-none">
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              
              {/* Formulário: Nova Matrícula */}
              <Card className="bg-white/60 backdrop-blur-xl border border-glass-border shadow-md rounded-2xl h-fit">
                <CardHeader>
                  <CardTitle className="text-base font-bold text-slate-800">Nova Matrícula</CardTitle>
                  <CardDescription className="text-xs">Registre e enturme novos discentes no ecossistema.</CardDescription>
                </CardHeader>
                <form onSubmit={handleCreateMatricula}>
                  <CardContent className="space-y-4">
                    <div className="space-y-2">
                      <Label htmlFor="nome" className="text-xs font-bold text-slate-600">Nome do Aluno</Label>
                      <Input 
                        id="nome" 
                        value={novaMatricula.nome} 
                        onChange={e => setNovaMatricula(prev => ({ ...prev, nome: e.target.value }))}
                        placeholder="Ex: Clara Mendes" 
                        className="bg-white"
                        required
                      />
                    </div>
                    
                    <div className="space-y-2">
                      <Label htmlFor="email" className="text-xs font-bold text-slate-600">E-mail Escolar</Label>
                      <Input 
                        id="email" 
                        type="email"
                        value={novaMatricula.email} 
                        onChange={e => setNovaMatricula(prev => ({ ...prev, email: e.target.value }))}
                        placeholder="Ex: clara.mendes@escola.pt" 
                        className="bg-white"
                        required
                      />
                    </div>

                    <div className="grid grid-cols-2 gap-4">
                      <div className="space-y-2">
                        <Label htmlFor="turma" className="text-xs font-bold text-slate-600">Turma</Label>
                        <Select 
                          value={novaMatricula.turma}
                          onValueChange={val => {
                            const matchingTurma = turmas.find(t => t.nome === val);
                            setNovaMatricula(prev => ({ 
                              ...prev, 
                              turma: val,
                              curso: matchingTurma ? matchingTurma.curso : "Fundamental II"
                            }));
                          }}
                        >
                          <SelectTrigger className="bg-white">
                            <SelectValue placeholder="Selecione" />
                          </SelectTrigger>
                          <SelectContent>
                            {turmas.map(t => (
                              <SelectItem key={t.id} value={t.nome}>{t.nome}</SelectItem>
                            ))}
                          </SelectContent>
                        </Select>
                      </div>

                      <div className="space-y-2">
                        <Label htmlFor="status" className="text-xs font-bold text-slate-600">Status Inicial</Label>
                        <Select 
                          value={novaMatricula.status}
                          onValueChange={val => setNovaMatricula(prev => ({ ...prev, status: val }))}
                        >
                          <SelectTrigger className="bg-white">
                            <SelectValue placeholder="Selecione" />
                          </SelectTrigger>
                          <SelectContent>
                            <SelectItem value="Ativo">Ativo</SelectItem>
                            <SelectItem value="Pendente">Pendente</SelectItem>
                            <SelectItem value="Inativo">Inativo</SelectItem>
                          </SelectContent>
                        </Select>
                      </div>
                    </div>
                  </CardContent>
                  <CardFooter>
                    <Button type="submit" className="w-full bg-amber-500 hover:bg-amber-600 text-white font-bold rounded-xl shadow-md">
                      <Plus className="w-4 h-4 mr-2" /> Concluir Matrícula
                    </Button>
                  </CardFooter>
                </form>
              </Card>

              {/* Tabela de Matrículas */}
              <Card className="bg-white/60 backdrop-blur-xl border border-glass-border shadow-md rounded-2xl lg:col-span-2">
                <CardHeader className="flex flex-row items-center justify-between pb-2 space-y-0">
                  <div>
                    <CardTitle className="text-base font-bold text-slate-800">Alunos Matriculados</CardTitle>
                    <CardDescription className="text-xs">Gerencie o fluxo de enturmação e status dos alunos.</CardDescription>
                  </div>
                  <div className="relative w-48">
                    <Search className="absolute left-3 top-2.5 w-3.5 h-3.5 text-slate-400" />
                    <Input 
                      placeholder="Pesquisar..." 
                      value={searchMatricula}
                      onChange={e => setSearchMatricula(e.target.value)}
                      className="pl-8 bg-white h-9 text-xs rounded-xl"
                    />
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="border border-slate-100 rounded-xl overflow-hidden bg-white/40">
                    <Table>
                      <TableHeader className="bg-slate-50/70">
                        <TableRow>
                          <TableHead className="text-xs font-bold text-slate-600">Aluno</TableHead>
                          <TableHead className="text-xs font-bold text-slate-600">Turma</TableHead>
                          <TableHead className="text-xs font-bold text-slate-600">Curso</TableHead>
                          <TableHead className="text-xs font-bold text-slate-600">Status</TableHead>
                          <TableHead className="text-xs font-bold text-slate-600 text-right">Ações</TableHead>
                        </TableRow>
                      </TableHeader>
                      <TableBody>
                        {filteredMatriculas.length > 0 ? (
                          filteredMatriculas.map((mat) => (
                            <TableRow key={mat.id} className="hover:bg-slate-50/50">
                              <TableCell>
                                <div className="font-bold text-slate-800 text-xs">{mat.nome}</div>
                                <div className="text-[10px] text-slate-400">{mat.email}</div>
                              </TableCell>
                              <TableCell className="text-xs text-slate-600">{mat.turma}</TableCell>
                              <TableCell className="text-xs text-slate-500">{mat.curso}</TableCell>
                              <TableCell>
                                <Badge 
                                  onClick={() => handleToggleStatus(mat.id)}
                                  className={`text-[9px] font-bold px-2 py-0.5 cursor-pointer hover:opacity-85 ${
                                    mat.status === "Ativo" ? "bg-emerald-100 border border-emerald-200 text-emerald-700" :
                                    mat.status === "Pendente" ? "bg-amber-100 border border-amber-200 text-amber-700" :
                                    "bg-rose-100 border border-rose-200 text-rose-700"
                                  }`}
                                >
                                  {mat.status}
                                </Badge>
                              </TableCell>
                              <TableCell className="text-right">
                                <Button 
                                  variant="ghost" 
                                  size="icon" 
                                  className="h-7 w-7 text-rose-500 hover:text-rose-600 hover:bg-rose-50 rounded-lg"
                                  onClick={() => handleDeleteMatricula(mat.id)}
                                >
                                  <Trash2 className="w-3.5 h-3.5" />
                                </Button>
                              </TableCell>
                            </TableRow>
                          ))
                        ) : (
                          <TableRow>
                            <TableCell colSpan={5} className="text-center text-slate-400 py-6 text-xs">Nenhum aluno encontrado.</TableCell>
                          </TableRow>
                        )}
                      </TableBody>
                    </Table>
                  </div>
                </CardContent>
              </Card>

            </div>

            {/* Atribuição de Professores e Disciplinas */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              
              {/* Form de Atribuição */}
              <Card className="bg-white/60 backdrop-blur-xl border border-glass-border shadow-md rounded-2xl h-fit">
                <CardHeader>
                  <CardTitle className="text-base font-bold text-slate-800">Atribuição Docente</CardTitle>
                  <CardDescription className="text-xs">Atribua professores a disciplinas e turmas.</CardDescription>
                </CardHeader>
                <form onSubmit={handleSaveAtribuicao}>
                  <CardContent className="space-y-4">
                    <div className="space-y-2">
                      <Label htmlFor="atrib-turma" className="text-xs font-bold text-slate-600">Turma Alvo</Label>
                      <Select 
                        value={novaAtribuicao.turmaId}
                        onValueChange={val => setNovaAtribuicao(prev => ({ ...prev, turmaId: val }))}
                      >
                        <SelectTrigger className="bg-white">
                          <SelectValue placeholder="Selecione" />
                        </SelectTrigger>
                        <SelectContent>
                          {turmas.map(t => (
                            <SelectItem key={t.id} value={t.id}>{t.nome} ({t.curso})</SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>

                    <div className="space-y-2">
                      <Label htmlFor="professor" className="text-xs font-bold text-slate-600">Professor</Label>
                      <Input 
                        id="professor"
                        value={novaAtribuicao.professor}
                        onChange={e => setNovaAtribuicao(prev => ({ ...prev, professor: e.target.value }))}
                        placeholder="Ex: Prof. Roberto"
                        className="bg-white"
                        required
                      />
                    </div>

                    <div className="space-y-2">
                      <Label htmlFor="disciplina" className="text-xs font-bold text-slate-600">Disciplina</Label>
                      <Input 
                        id="disciplina"
                        value={novaAtribuicao.disciplina}
                        onChange={e => setNovaAtribuicao(prev => ({ ...prev, disciplina: e.target.value }))}
                        placeholder="Ex: Química"
                        className="bg-white"
                        required
                      />
                    </div>
                  </CardContent>
                  <CardFooter>
                    <Button type="submit" className="w-full bg-slate-800 hover:bg-slate-700 text-white font-bold rounded-xl shadow-md">
                      <Save className="w-4 h-4 mr-2" /> Salvar Atribuição
                    </Button>
                  </CardFooter>
                </form>
              </Card>

              {/* Tabela de Turmas & Atribuições */}
              <Card className="bg-white/60 backdrop-blur-xl border border-glass-border shadow-md rounded-2xl lg:col-span-2">
                <CardHeader>
                  <CardTitle className="text-base font-bold text-slate-800">Quadro de Turmas e Professores</CardTitle>
                  <CardDescription className="text-xs">Turmas ativas com seus respectivos regentes.</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="border border-slate-100 rounded-xl overflow-hidden bg-white/40">
                    <Table>
                      <TableHeader className="bg-slate-50/70">
                        <TableRow>
                          <TableHead className="text-xs font-bold text-slate-600">Turma</TableHead>
                          <TableHead className="text-xs font-bold text-slate-600">Curso / Série</TableHead>
                          <TableHead className="text-xs font-bold text-slate-600">Professor</TableHead>
                          <TableHead className="text-xs font-bold text-slate-600">Disciplina</TableHead>
                        </TableRow>
                      </TableHeader>
                      <TableBody>
                        {turmas.map((t) => (
                          <TableRow key={t.id} className="hover:bg-slate-50/50">
                            <TableCell className="text-xs font-bold text-slate-800">{t.nome}</TableCell>
                            <TableCell className="text-xs text-slate-500">{t.curso}</TableCell>
                            <TableCell className="text-xs text-slate-700 font-medium">{t.professor || <span className="text-rose-500 text-[10px]">Sem docente</span>}</TableCell>
                            <TableCell>
                              {t.disciplina ? (
                                <Badge variant="outline" className="bg-slate-100 text-slate-700 text-[10px]">{t.disciplina}</Badge>
                              ) : (
                                <span className="text-rose-500 text-[10px]">Não definida</span>
                              )}
                            </TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          {/* TAB 3: DIÁRIOS DE CLASSE */}
          <TabsContent value="diarios" className="space-y-6 outline-none">
            <Card className="bg-white/60 backdrop-blur-xl border border-glass-border shadow-md rounded-2xl">
              <CardHeader className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-2">
                <div>
                  <CardTitle className="text-base font-bold text-slate-800">Histórico de Diários de Classe</CardTitle>
                  <CardDescription className="text-xs">Monitore os conteúdos ministrados e a frequência das aulas.</CardDescription>
                </div>
                <div className="flex items-center gap-3">
                  <span className="text-xs text-slate-500 whitespace-nowrap">Filtrar por Turma:</span>
                  <Select value={filterTurmaDiarios} onValueChange={setFilterTurmaDiarios}>
                    <SelectTrigger className="bg-white w-40 h-9 rounded-xl text-xs">
                      <SelectValue placeholder="Todas as turmas" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="TODAS">Todas as turmas</SelectItem>
                      {turmas.map(t => (
                        <SelectItem key={t.id} value={t.nome}>{t.nome}</SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
              </CardHeader>
              <CardContent>
                <div className="border border-slate-100 rounded-xl overflow-hidden bg-white/40">
                  <Table>
                    <TableHeader className="bg-slate-50/70">
                      <TableRow>
                        <TableHead className="text-xs font-bold text-slate-600">Data</TableHead>
                        <TableHead className="text-xs font-bold text-slate-600">Docente & Disciplina</TableHead>
                        <TableHead className="text-xs font-bold text-slate-600">Turma</TableHead>
                        <TableHead className="text-xs font-bold text-slate-600">Conteúdo Programático</TableHead>
                        <TableHead className="text-xs font-bold text-slate-600 text-center">Presença Média</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {filteredDiarios.length > 0 ? (
                        filteredDiarios.map((diar) => (
                          <TableRow key={diar.id} className="hover:bg-slate-50/50">
                            <TableCell className="text-xs font-bold text-slate-500 whitespace-nowrap">
                              {diar.data}
                            </TableCell>
                            <TableCell>
                              <div className="text-xs font-bold text-slate-800">{diar.professor}</div>
                              <div className="text-[10px] text-slate-400">{diar.disciplina}</div>
                            </TableCell>
                            <TableCell className="text-xs font-medium text-slate-600">{diar.turma}</TableCell>
                            <TableCell className="text-xs text-slate-600 max-w-xs md:max-w-md truncate" title={diar.conteudo}>
                              {diar.conteudo}
                            </TableCell>
                            <TableCell className="text-center">
                              <Badge className="bg-emerald-500/10 border border-emerald-500/20 text-emerald-600 text-[10px] font-bold">
                                {diar.presenca}
                              </Badge>
                            </TableCell>
                          </TableRow>
                        ))
                      ) : (
                        <TableRow>
                          <TableCell colSpan={5} className="text-center text-slate-400 py-6 text-xs">Nenhum diário registrado para esta turma.</TableCell>
                        </TableRow>
                      )}
                    </TableBody>
                  </Table>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* TAB 4: NOTAS & PRESENÇA (RELATÓRIOS) */}
          <TabsContent value="relatorios" className="space-y-6 outline-none">
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              
              {/* Estatísticas Consolidadas */}
              <div className="space-y-6">
                <Card className="bg-white/60 backdrop-blur-xl border border-glass-border shadow-md rounded-2xl">
                  <CardHeader>
                    <CardTitle className="text-base font-bold text-slate-800 font-mono">Consolidado Escolar</CardTitle>
                    <CardDescription className="text-xs">Métricas globais do rendimento institucional.</CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    {[
                      { label: "Média de Presença em Matemática", value: "96.5%", color: "text-amber-500" },
                      { label: "Média de Presença em Física", value: "92.8%", color: "text-blue-500" },
                      { label: "Média de Presença em Português", value: "95.1%", color: "text-purple-500" },
                      { label: "Alunos com menos de 75% Presença", value: "2 alunos", color: "text-rose-500" }
                    ].map((m, idx) => (
                      <div key={idx} className="flex justify-between items-center p-3 bg-white/70 border border-slate-100 rounded-xl shadow-sm">
                        <span className="text-xs text-slate-600 font-medium">{m.label}</span>
                        <span className={`text-xs font-black ${m.color}`}>{m.value}</span>
                      </div>
                    ))}
                  </CardContent>
                </Card>

                {/* Exportar Dados */}
                <Card className="bg-white/60 backdrop-blur-xl border border-glass-border shadow-md rounded-2xl">
                  <CardHeader>
                    <CardTitle className="text-base font-bold text-slate-800">Exportação de Relatórios</CardTitle>
                    <CardDescription className="text-xs">Baixe os dados estruturados de notas e presença.</CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-3">
                    <Button 
                      onClick={() => {
                        toast.success("Download iniciado!", { description: "relatorio_notas_diario_2026.csv baixado" });
                      }}
                      className="w-full justify-start bg-white border border-slate-200 hover:bg-slate-50 text-slate-700 text-xs font-bold py-3.5 rounded-xl transition-all"
                    >
                      <Download className="w-4 h-4 mr-3 text-amber-500" /> Exportar Notas (CSV)
                    </Button>
                    <Button 
                      onClick={() => {
                        toast.success("Download de Presença iniciado!", { description: "relatorio_presenca_diario_2026.csv baixado" });
                      }}
                      className="w-full justify-start bg-white border border-slate-200 hover:bg-slate-50 text-slate-700 text-xs font-bold py-3.5 rounded-xl transition-all"
                    >
                      <Download className="w-4 h-4 mr-3 text-emerald-500" /> Exportar Frequência Escolar (CSV)
                    </Button>
                  </CardContent>
                </Card>
              </div>

              {/* Tabela de Notas & Presença por Turma */}
              <Card className="bg-white/60 backdrop-blur-xl border border-glass-border shadow-md rounded-2xl lg:col-span-2">
                <CardHeader>
                  <CardTitle className="text-base font-bold text-slate-800">Rendimento e Frequência por Turma</CardTitle>
                  <CardDescription className="text-xs">Quadro consolidado de desempenho por agrupamento acadêmico.</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="border border-slate-100 rounded-xl overflow-hidden bg-white/40">
                    <Table>
                      <TableHeader className="bg-slate-50/70">
                        <TableRow>
                          <TableHead className="text-xs font-bold text-slate-600">Turma</TableHead>
                          <TableHead className="text-xs font-bold text-slate-600 text-center">Matemática (Média)</TableHead>
                          <TableHead className="text-xs font-bold text-slate-600 text-center">Física (Média)</TableHead>
                          <TableHead className="text-xs font-bold text-slate-600 text-center">Português (Média)</TableHead>
                          <TableHead className="text-xs font-bold text-slate-600 text-center">Presença Média</TableHead>
                        </TableRow>
                      </TableHeader>
                      <TableBody>
                        {PERFORMANCE_DATA.map((row, idx) => (
                          <TableRow key={idx} className="hover:bg-slate-50/50">
                            <TableCell className="text-xs font-bold text-slate-800">{row.turma}</TableCell>
                            <TableCell className="text-center text-xs font-bold text-slate-700">
                              {row.Matematica}%
                            </TableCell>
                            <TableCell className="text-center text-xs font-bold text-slate-700">
                              {row.Fisica > 0 ? `${row.Fisica}%` : <span className="text-slate-400 font-normal">-</span>}
                            </TableCell>
                            <TableCell className="text-center text-xs font-bold text-slate-700">
                              {row.Portugues}%
                            </TableCell>
                            <TableCell className="text-center">
                              <span className={`text-xs font-extrabold ${row.presenca >= 95 ? "text-emerald-600" : "text-amber-600"}`}>
                                {row.presenca}%
                              </span>
                            </TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </div>
                </CardContent>
              </Card>

            </div>
          </TabsContent>

          {/* TAB 5: CALIBRAÇÃO REDE / IA */}
          <TabsContent value="config" className="space-y-6 outline-none">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              
              {/* Painel ZIOS IA */}
              <Card className="bg-white/60 backdrop-blur-xl border border-glass-border shadow-md rounded-2xl">
                <CardHeader>
                  <CardTitle className="text-base font-bold text-slate-800 flex items-center gap-2">
                    <Brain className="w-5 h-5 text-amber-500 animate-pulse" /> Calibração ZIOS IA
                  </CardTitle>
                  <CardDescription className="text-xs">Ajuste os limiares cognitivos da IA de suporte pedagógico do Hemera.</CardDescription>
                </CardHeader>
                <CardContent className="space-y-6">
                  
                  {/* Slider: Temperatura */}
                  <div className="space-y-2">
                    <div className="flex justify-between text-xs">
                      <span className="font-bold text-slate-600">Temperatura Cognitiva (Criatividade)</span>
                      <span className="font-bold text-amber-600 font-mono" data-testid="ai-temp-value">{iaConfig.temperatura}</span>
                    </div>
                    <Slider 
                      min={0.0} 
                      max={1.0} 
                      step={0.1} 
                      value={[iaConfig.temperatura]} 
                      onValueChange={val => setIaConfig(prev => ({ ...prev, temperatura: val[0] }))}
                      className="py-2"
                      data-testid="ai-temp-slider"
                    />
                    <p className="text-[10px] text-slate-400 leading-normal">
                      Valores baixos (0.1 - 0.3) garantem respostas científicas e matemáticas precisas. Valores altos (0.7+) estimulam criatividade literária e artística.
                    </p>
                  </div>

                  {/* Slider: Limite de Tokens */}
                  <div className="space-y-2">
                    <div className="flex justify-between text-xs">
                      <span className="font-bold text-slate-600">Tamanho Máximo de Resposta</span>
                      <span className="font-bold text-amber-600 font-mono">{iaConfig.maxTokens} tokens</span>
                    </div>
                    <Slider 
                      min={100} 
                      max={2000} 
                      step={50} 
                      value={[iaConfig.maxTokens]} 
                      onValueChange={val => setIaConfig(prev => ({ ...prev, maxTokens: val[0] }))}
                      className="py-2"
                    />
                    <p className="text-[10px] text-slate-400 leading-normal">
                      Limita o consumo de tokens ZIOS por interação do professor/aluno para controle de cota computacional.
                    </p>
                  </div>

                  {/* Switch: Feedbacks Preditivos */}
                  <div className="flex items-center justify-between p-3.5 bg-white border border-slate-100 rounded-xl shadow-sm">
                    <div className="space-y-0.5 max-w-[80%]">
                      <Label htmlFor="pred-model" className="text-xs font-bold text-slate-700">Relatórios Preditivos Ativos</Label>
                      <p className="text-[10px] text-slate-400 leading-normal">Permite que a PentaIA emita insights de nota/frequência para docentes automaticamente.</p>
                    </div>
                    <Switch 
                      id="pred-model" 
                      checked={iaConfig.predictiveModel} 
                      onCheckedChange={checked => setIaConfig(prev => ({ ...prev, predictiveModel: checked }))}
                      data-testid="predictive-switch"
                    />
                  </div>

                  {/* Input: Chave de Segurança */}
                  <div className="space-y-2 pt-2 border-t border-slate-100">
                    <Label htmlFor="ai-key" className="text-xs font-bold text-slate-600 flex items-center gap-1">
                      <Shield className="w-3.5 h-3.5 text-slate-500" /> Token de API ZIOS (Criptografado)
                    </Label>
                    <div className="relative">
                      <Input 
                        id="ai-key"
                        type={showAiKey ? "text" : "password"}
                        value={iaConfig.aiKey}
                        onChange={e => setIaConfig(prev => ({ ...prev, aiKey: e.target.value }))}
                        className="bg-white font-mono text-xs pr-10 h-10 rounded-xl"
                      />
                      <button 
                        type="button" 
                        onClick={() => setShowAiKey(!showAiKey)}
                        className="absolute p-2 right-2 top-1 text-slate-400 hover:text-slate-600"
                        data-testid="toggle-ai-key-visibility"
                      >
                        {showAiKey ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                      </button>
                    </div>
                  </div>

                </CardContent>
                <CardFooter>
                  <Button onClick={handleSaveCalibracao} className="w-full bg-amber-500 hover:bg-amber-600 text-white font-bold rounded-xl shadow-md" data-testid="save-ai-calib">
                    Salvar Calibração Cognitiva
                  </Button>
                </CardFooter>
              </Card>

              {/* Calibração de Rede */}
              <Card className="bg-white/60 backdrop-blur-xl border border-glass-border shadow-md rounded-2xl">
                <CardHeader>
                  <CardTitle className="text-base font-bold text-slate-800 flex items-center gap-2">
                    <Globe className="w-5 h-5 text-indigo-500" /> Controle de Banda & Latência
                  </CardTitle>
                  <CardDescription className="text-xs">Ajuste os parâmetros de tráfego de rede da instituição.</CardDescription>
                </CardHeader>
                <CardContent className="space-y-6">
                  
                  {/* Slider: Prioridade de Banda */}
                  <div className="space-y-2">
                    <div className="flex justify-between text-xs">
                      <span className="font-bold text-slate-600">Garantia de Banda Escolar</span>
                      <span className="font-bold text-indigo-600 font-mono">{redeConfig.prioridadeBanda}%</span>
                    </div>
                    <Slider 
                      min={10} 
                      max={100} 
                      step={5} 
                      value={[redeConfig.prioridadeBanda]} 
                      onValueChange={val => setRedeConfig(prev => ({ ...prev, prioridadeBanda: val[0] }))}
                      className="py-2"
                    />
                    <p className="text-[10px] text-slate-400 leading-normal">
                      Percentual de largura de banda de rede reservado exclusivamente para o tráfego de dados pedagógicos (Lousa, Diários e Simulados).
                    </p>
                  </div>

                  {/* Slider: Latência Alvo */}
                  <div className="space-y-2">
                    <div className="flex justify-between text-xs">
                      <span className="font-bold text-slate-600">Latência Alvo do Barramento (ZIOS)</span>
                      <span className="font-bold text-indigo-600 font-mono" data-testid="network-latency-value">{redeConfig.latenciaAlvo} ms</span>
                    </div>
                    <Slider 
                      min={10} 
                      max={100} 
                      step={5} 
                      value={[redeConfig.latenciaAlvo]} 
                      onValueChange={val => setRedeConfig(prev => ({ ...prev, latenciaAlvo: val[0] }))}
                      className="py-2"
                      data-testid="network-latency-slider"
                    />
                    <p className="text-[10px] text-slate-400 leading-normal">
                      Janela de latência alvo aceitável para chamadas de API in tempo real na lousa inteligente do Hemera.
                    </p>
                  </div>

                  {/* Switch: Compressão de Vídeo */}
                  <div className="flex items-center justify-between p-3.5 bg-white border border-slate-100 rounded-xl shadow-sm">
                    <div className="space-y-0.5 max-w-[80%]">
                      <Label htmlFor="video-comp" className="text-xs font-bold text-slate-700">Compressão Inteligente de Vídeo</Label>
                      <p className="text-[10px] text-slate-400 leading-normal">Habilita codecs de baixa largura de banda em salas de transmissão simultânea de vídeo híbrido.</p>
                    </div>
                    <Switch 
                      id="video-comp" 
                      checked={redeConfig.compressaoVideo} 
                      onCheckedChange={checked => setRedeConfig(prev => ({ ...prev, compressaoVideo: checked }))}
                      data-testid="network-compress-switch"
                    />
                  </div>

                  {/* Status do Barramento */}
                  <div className="p-4 bg-slate-50 border border-slate-200 rounded-xl flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <Cpu className="w-5 h-5 text-slate-500" />
                      <div>
                        <div className="text-xs font-bold text-slate-700">Carga do Processador do Barramento</div>
                        <div className="text-[10px] text-slate-400">Canal de Comunicação Central</div>
                      </div>
                    </div>
                    <Badge className="bg-slate-200 text-slate-700 font-mono text-xs">
                      12% de Carga
                    </Badge>
                  </div>

                </CardContent>
                <CardFooter>
                  <Button onClick={handleSaveCalibracao} className="w-full bg-slate-800 hover:bg-slate-700 text-white font-bold rounded-xl shadow-md" data-testid="save-network-calib">
                    Calibrar Infraestrutura
                  </Button>
                </CardFooter>
              </Card>

            </div>
          </TabsContent>
        </Tabs>

      </div>
    </AppLayout>
  );
}
