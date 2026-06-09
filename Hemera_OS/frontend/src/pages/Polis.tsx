import React, { useState, useEffect } from "react";
import { AppLayout } from "@/components/layout/AppLayout";
import { useAuth } from "@/hooks/useAuth";
import { useToast } from "@/hooks/use-toast";
import { 
  MessageSquare, 
  Users, 
  FileText, 
  Upload, 
  Heart, 
  MessageCircle, 
  Pin, 
  Plus, 
  Search, 
  Share2, 
  School, 
  ChevronDown, 
  Bell, 
  Trash2,
  FileCode,
  FileImage,
  FileArchive,
  Megaphone
} from "lucide-react";

// --- INTERFACES ---
interface School {
  id: string;
  name: string;
}

interface ClassRoom {
  id: string;
  schoolId: string;
  name: string;
}

interface Announcement {
  id: string;
  classId: string;
  title: string;
  content: string;
  author: string;
  authorRole: 'professor' | 'aluno' | 'diretor';
  createdAt: string;
  pinned: boolean;
}

interface Comment {
  id: string;
  author: string;
  authorRole: 'professor' | 'aluno';
  content: string;
  createdAt: string;
}

interface Post {
  id: string;
  classId: string;
  author: string;
  authorRole: 'professor' | 'aluno';
  avatar?: string;
  content: string;
  createdAt: string;
  likes: number;
  likedByMe?: boolean;
  comments: Comment[];
  attachment?: {
    name: string;
    type: 'pdf' | 'doc' | 'image' | 'zip';
    size: string;
  };
}

interface SchoolFile {
  id: string;
  classId: string;
  name: string;
  type: 'pdf' | 'doc' | 'image' | 'zip';
  uploadedBy: string;
  uploadedByRole: 'professor' | 'aluno';
  size: string;
  category: 'Material de Aula' | 'Atividades' | 'Leitura Complementar';
  uploadedAt: string;
}

interface SystemNotification {
  id: string;
  content: string;
  createdAt: string;
  type: 'like' | 'comment' | 'announcement' | 'file';
}

// --- MOCK DATA ---
const schoolsMock: School[] = [
  { id: "school-alpha", name: "Colégio Estadual Hemera Alpha" },
  { id: "school-beta", name: "Instituto Tecnológico Hemera Beta" }
];

const classesMock: ClassRoom[] = [
  { id: "class-alpha-9a", schoolId: "school-alpha", name: "9º Ano A - Ciências e Matemática" },
  { id: "class-alpha-8b", schoolId: "school-alpha", name: "8º Ano B - Humanas e Artes" },
  { id: "class-beta-eng1", schoolId: "school-beta", name: "Engenharia de Software 1A" },
  { id: "class-beta-comp2", schoolId: "school-beta", name: "Ciência da Computação 2B" }
];

const initialAnnouncements: Announcement[] = [
  {
    id: "ann-1",
    classId: "class-alpha-9a",
    title: "Entrega do Trabalho de Física",
    content: "Lembrando que o relatório prático sobre termodinâmica deve ser entregue até a próxima sexta-feira no laboratório físico ou via upload de arquivos.",
    author: "Prof. Alberto Santos",
    authorRole: "professor",
    createdAt: "2026-05-27T10:00:00.000Z",
    pinned: true
  },
  {
    id: "ann-2",
    classId: "class-alpha-9a",
    title: "Reunião de Líderes de Turma",
    content: "Amanhã na hora do intervalo teremos a primeira reunião oficial de representantes com a coordenação pedagógica na sala multimídia.",
    author: "Diretora Marina Silva",
    authorRole: "diretor",
    createdAt: "2026-05-26T14:30:00.000Z",
    pinned: false
  },
  {
    id: "ann-3",
    classId: "class-alpha-8b",
    title: "Visita Guiada ao Museu",
    content: "O formulário de autorização para a visita pedagógica ao Museu de História Natural já está disponível na biblioteca. Entregar assinado pelos responsáveis até segunda-feira.",
    author: "Profa. Carla Lima",
    authorRole: "professor",
    createdAt: "2026-05-27T08:15:00.000Z",
    pinned: true
  },
  {
    id: "ann-4",
    classId: "class-beta-eng1",
    title: "Instruções do Hackathon Hemera",
    content: "Estão abertas as inscrições para o Hackathon Interno! O tema deste ano será Soluções Ambientais Inteligentes em Computação de Borda.",
    author: "Coordenador Marcos Souza",
    authorRole: "professor",
    createdAt: "2026-05-28T09:00:00.000Z",
    pinned: true
  }
];

const initialPosts: Post[] = [
  {
    id: "post-1",
    classId: "class-alpha-9a",
    author: "Gustavo Nogueira",
    authorRole: "aluno",
    content: "Pessoal, alguém conseguiu resolver o exercício 5 da lista de álgebra? Travei na parte da matriz de rotação bidimensional. Se alguém puder ajudar ou mandar uma foto do raciocínio!",
    createdAt: "2026-05-27T22:30:00.000Z",
    likes: 4,
    likedByMe: false,
    comments: [
      {
        id: "com-1",
        author: "Fernanda Costa",
        authorRole: "aluno",
        content: "Eu consegui resolver usando a identidade trigonométrica fundamental! Basicamente você simplifica a matriz antes de multiplicar.",
        createdAt: "2026-05-27T22:45:00.000Z"
      },
      {
        id: "com-2",
        author: "Prof. Alberto Santos",
        authorRole: "professor",
        content: "Dica valiosa, Fernanda! Gustavo, lembre-se também de que o determinante da matriz de rotação deve ser sempre igual a 1. Isso ajuda a conferir as contas.",
        createdAt: "2026-05-28T08:00:00.000Z"
      }
    ],
    attachment: {
      name: "exercicio-matrizes-dicas.pdf",
      type: "pdf",
      size: "1.2 MB"
    }
  },
  {
    id: "post-2",
    classId: "class-alpha-9a",
    author: "Ana Beatriz",
    authorRole: "aluno",
    content: "Compartilhando com vocês as anotações organizadas que fiz da aula de Biologia Celular sobre mitocôndrias e respiração aeróbica. Espero que ajude nos estudos para a prova!",
    createdAt: "2026-05-26T18:20:00.000Z",
    likes: 9,
    likedByMe: true,
    comments: [
      {
        id: "com-3",
        author: "Rodrigo M.",
        authorRole: "aluno",
        content: "Salva demais! Resumo super colorido e direto ao ponto. Valeu Ana!",
        createdAt: "2026-05-26T19:00:00.000Z"
      }
    ],
    attachment: {
      name: "resumo-respiracao-celular.image",
      type: "image",
      size: "3.4 MB"
    }
  },
  {
    id: "post-3",
    classId: "class-beta-eng1",
    author: "Professor Roberto Cruz",
    authorRole: "professor",
    content: "Subi o repositório base com a arquitetura limpa em TypeScript para o nosso projeto semestral. Certifiquem-se de seguir as regras de lint e criar os testes unitários apropriadamente.",
    createdAt: "2026-05-28T01:10:00.000Z",
    likes: 12,
    likedByMe: false,
    comments: [],
    attachment: {
      name: "projeto-base-arquitetura.zip",
      type: "zip",
      size: "14.5 MB"
    }
  }
];

const initialFiles: SchoolFile[] = [
  {
    id: "file-1",
    classId: "class-alpha-9a",
    name: "cronograma_aulas_fisica_2026.pdf",
    type: "pdf",
    uploadedBy: "Prof. Alberto Santos",
    uploadedByRole: "professor",
    size: "450 KB",
    category: "Material de Aula",
    uploadedAt: "2026-05-01T09:00:00.000Z"
  },
  {
    id: "file-2",
    classId: "class-alpha-9a",
    name: "tabela-periodica-interativa.doc",
    type: "doc",
    uploadedBy: "Prof. Alberto Santos",
    uploadedByRole: "professor",
    size: "2.1 MB",
    category: "Material de Aula",
    uploadedAt: "2026-05-15T11:20:00.000Z"
  },
  {
    id: "file-3",
    classId: "class-alpha-9a",
    name: "modelo-relatorio-ciencias.doc",
    type: "doc",
    uploadedBy: "Fernanda Costa",
    uploadedByRole: "aluno",
    size: "1.1 MB",
    category: "Atividades",
    uploadedAt: "2026-05-25T14:40:00.000Z"
  },
  {
    id: "file-4",
    classId: "class-beta-eng1",
    name: "guia_estilos_typescript.pdf",
    type: "pdf",
    uploadedBy: "Professor Roberto Cruz",
    uploadedByRole: "professor",
    size: "890 KB",
    category: "Leitura Complementar",
    uploadedAt: "2026-05-20T10:00:00.000Z"
  }
];

export const Polis: React.FC = () => {
  const { user } = useAuth();
  const { toast } = useToast();
  
  // Multi-tenancy State
  const [selectedSchool, setSelectedSchool] = useState<string>("school-alpha");
  const [selectedClass, setSelectedClass] = useState<string>("class-alpha-9a");
  
  // Navigation Tabs
  const [activeTab, setActiveTab] = useState<"mural" | "feed" | "arquivos">("mural");
  
  // Core Data States (Reactive to current filters)
  const [announcements, setAnnouncements] = useState<Announcement[]>(initialAnnouncements);
  const [posts, setPosts] = useState<Post[]>(initialPosts);
  const [files, setFiles] = useState<SchoolFile[]>(initialFiles);
  
  // Form states
  const [newAnnTitle, setNewAnnTitle] = useState("");
  const [newAnnContent, setNewAnnContent] = useState("");
  const [newAnnPinned, setNewAnnPinned] = useState(false);
  
  const [newPostContent, setNewPostContent] = useState("");
  const [newPostAttachName, setNewPostAttachName] = useState("");
  const [newPostAttachType, setNewPostAttachType] = useState<'pdf' | 'doc' | 'image' | 'zip'>('pdf');
  const [showAttachForm, setShowAttachForm] = useState(false);
  
  const [commentInputs, setCommentInputs] = useState<Record<string, string>>({});
  
  const [searchFileQuery, setSearchFileQuery] = useState("");
  const [newFileName, setNewFileName] = useState("");
  const [newFileType, setNewFileType] = useState<'pdf' | 'doc' | 'image' | 'zip'>('pdf');
  const [newFileCategory, setNewFileCategory] = useState<'Material de Aula' | 'Atividades' | 'Leitura Complementar'>('Material de Aula');
  const [showUploadForm, setShowUploadForm] = useState(false);
  
  // Real-time notifications simulation state
  const [notifications, setNotifications] = useState<SystemNotification[]>([
    {
      id: "not-1",
      content: "Prof. Alberto Santos postou um aviso fixado no Mural.",
      createdAt: "2026-05-27T10:05:00.000Z",
      type: "announcement"
    },
    {
      id: "not-2",
      content: "Fernanda Costa comentou na sua postagem recente.",
      createdAt: "2026-05-27T22:46:00.000Z",
      type: "comment"
    }
  ]);
  
  // Determine role safely
  const currentUserRole = user?.role || "aluno";
  const currentUserName = currentUserRole === "professor" ? "Prof. Cláudio Mendonça" : "Ian Santos";

  // Filter classes based on selected school
  const currentClasses = classesMock.filter(c => c.schoolId === selectedSchool);

  // Auto-switch class when school changes to ensure consistency
  useEffect(() => {
    const firstClassOfSchool = classesMock.find(c => c.schoolId === selectedSchool);
    if (firstClassOfSchool) {
      setSelectedClass(firstClassOfSchool.id);
    }
  }, [selectedSchool]);

  // Handler for adding Announcement (Mural) - restricted to professor
  const handleAddAnnouncement = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newAnnTitle.trim() || !newAnnContent.trim()) {
      toast({
        title: "Erro ao publicar",
        description: "Título e Conteúdo são obrigatórios.",
        variant: "destructive"
      });
      return;
    }

    const newAnn: Announcement = {
      id: `ann-${Date.now()}`,
      classId: selectedClass,
      title: newAnnTitle,
      content: newAnnContent,
      author: currentUserName,
      authorRole: 'professor',
      createdAt: new Date().toISOString(),
      pinned: newAnnPinned
    };

    setAnnouncements([newAnn, ...announcements]);
    
    // Add simulated real-time notification
    const newNotif: SystemNotification = {
      id: `not-${Date.now()}`,
      content: `${currentUserName} publicou um novo comunicado oficial no Mural: "${newAnnTitle}".`,
      createdAt: new Date().toISOString(),
      type: 'announcement'
    };
    setNotifications([newNotif, ...notifications]);

    // Reset Form
    setNewAnnTitle("");
    setNewAnnContent("");
    setNewAnnPinned(false);

    toast({
      title: "Comunicado Publicado!",
      description: "Seu aviso foi fixado no Mural com sucesso.",
    });
  };

  // Handler for adding Post to Feed
  const handleAddPost = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newPostContent.trim()) {
      toast({
        title: "Post vazio",
        description: "Digite alguma coisa antes de publicar.",
        variant: "destructive"
      });
      return;
    }

    const hasAttachment = showAttachForm && newPostAttachName.trim();
    const newPost: Post = {
      id: `post-${Date.now()}`,
      classId: selectedClass,
      author: currentUserName,
      authorRole: currentUserRole,
      content: newPostContent,
      createdAt: new Date().toISOString(),
      likes: 0,
      likedByMe: false,
      comments: [],
      attachment: hasAttachment ? {
        name: newPostAttachName.endsWith(`.${newPostAttachType}`) 
          ? newPostAttachName 
          : `${newPostAttachName}.${newPostAttachType}`,
        type: newPostAttachType,
        size: `${(Math.random() * 5 + 0.5).toFixed(1)} MB`
      } : undefined
    };

    setPosts([newPost, ...posts]);

    // Automatically add attachment to the class file vault if one is present
    if (newPost.attachment) {
      const autoFile: SchoolFile = {
        id: `file-${Date.now()}`,
        classId: selectedClass,
        name: newPost.attachment.name,
        type: newPost.attachment.type,
        uploadedBy: currentUserName,
        uploadedByRole: currentUserRole,
        size: newPost.attachment.size,
        category: "Material de Aula",
        uploadedAt: new Date().toISOString()
      };
      setFiles(prev => [autoFile, ...prev]);

      const fileNotif: SystemNotification = {
        id: `not-f-${Date.now()}`,
        content: `${currentUserName} anexou o arquivo "${newPost.attachment.name}" no feed.`,
        createdAt: new Date().toISOString(),
        type: 'file'
      };
      setNotifications(prev => [fileNotif, ...prev]);
    }

    // Add simulation notification
    const newNotif: SystemNotification = {
      id: `not-${Date.now()}`,
      content: `${currentUserName} compartilhou uma nova postagem na comunidade da turma.`,
      createdAt: new Date().toISOString(),
      type: 'comment'
    };
    setNotifications([newNotif, ...notifications]);

    // Reset Form
    setNewPostContent("");
    setNewPostAttachName("");
    setShowAttachForm(false);

    toast({
      title: "Post publicado!",
      description: "Sua postagem já está disponível no feed da turma.",
    });
  };

  // Like a post
  const handleLikePost = (postId: string) => {
    setPosts(prevPosts => 
      prevPosts.map(post => {
        if (post.id === postId) {
          const liked = !post.likedByMe;
          
          // Trigger notification on new like simulation
          if (liked) {
            const likeNotif: SystemNotification = {
              id: `not-l-${Date.now()}`,
              content: `Você curtiu a postagem de ${post.author}.`,
              createdAt: new Date().toISOString(),
              type: 'like'
            };
            setNotifications(prev => [likeNotif, ...prev]);
          }
          
          return {
            ...post,
            likedByMe: liked,
            likes: liked ? post.likes + 1 : post.likes - 1
          };
        }
        return post;
      })
    );
  };

  // Add comment to post
  const handleAddComment = (postId: string, e: React.FormEvent) => {
    e.preventDefault();
    const commentText = commentInputs[postId];
    if (!commentText || !commentText.trim()) return;

    const newComment: Comment = {
      id: `com-${Date.now()}`,
      author: currentUserName,
      authorRole: currentUserRole,
      content: commentText,
      createdAt: new Date().toISOString()
    };

    setPosts(prevPosts =>
      prevPosts.map(post => {
        if (post.id === postId) {
          return {
            ...post,
            comments: [...post.comments, newComment]
          };
        }
        return post;
      })
    );

    // Notification simulation
    const commentNotif: SystemNotification = {
      id: `not-c-${Date.now()}`,
      content: `Você comentou no post de ${posts.find(p => p.id === postId)?.author}.`,
      createdAt: new Date().toISOString(),
      type: 'comment'
    };
    setNotifications(prev => [commentNotif, ...prev]);

    // Reset Input
    setCommentInputs(prev => ({ ...prev, [postId]: "" }));
  };

  // Handler for file upload simulation
  const handleUploadFile = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newFileName.trim()) {
      toast({
        title: "Nome do arquivo vazio",
        description: "Dê um nome para o arquivo a ser enviado.",
        variant: "destructive"
      });
      return;
    }

    const filename = newFileName.endsWith(`.${newFileType}`) 
      ? newFileName 
      : `${newFileName}.${newFileType}`;

    const newFile: SchoolFile = {
      id: `file-${Date.now()}`,
      classId: selectedClass,
      name: filename,
      type: newFileType,
      uploadedBy: currentUserName,
      uploadedByRole: currentUserRole,
      size: `${(Math.random() * 8 + 0.1).toFixed(1)} MB`,
      category: newFileCategory,
      uploadedAt: new Date().toISOString()
    };

    setFiles([newFile, ...files]);

    // Add simulated real-time notification
    const fileNotif: SystemNotification = {
      id: `not-${Date.now()}`,
      content: `${currentUserName} enviou um novo arquivo: "${filename}" na pasta de arquivos da turma.`,
      createdAt: new Date().toISOString(),
      type: 'file'
    };
    setNotifications([fileNotif, ...notifications]);

    // Reset Form
    setNewFileName("");
    setShowUploadForm(false);

    toast({
      title: "Arquivo enviado!",
      description: `O arquivo ${filename} foi adicionado à pasta de ${newFileCategory}.`,
    });
  };

  // Delete dynamic items for UX polishing
  const handleDeletePost = (postId: string) => {
    setPosts(posts.filter(p => p.id !== postId));
    toast({
      title: "Post removido",
      description: "A postagem foi excluída com sucesso."
    });
  };

  const handleDeleteFile = (fileId: string) => {
    setFiles(files.filter(f => f.id !== fileId));
    toast({
      title: "Arquivo removido",
      description: "O arquivo foi excluído da lista da turma."
    });
  };

  // Helper file icons
  const getFileIcon = (type: string) => {
    switch (type) {
      case 'pdf': return <FileText className="w-8 h-8 text-red-500" />;
      case 'doc': return <FileCode className="w-8 h-8 text-blue-500" />;
      case 'image': return <FileImage className="w-8 h-8 text-green-500" />;
      case 'zip': return <FileArchive className="w-8 h-8 text-yellow-600" />;
      default: return <FileText className="w-8 h-8 text-gray-500" />;
    }
  };

  // Filters application
  const filteredAnnouncements = announcements.filter(ann => ann.classId === selectedClass);
  const filteredPosts = posts.filter(post => post.classId === selectedClass);
  const filteredFiles = files.filter(file => {
    const matchesClass = file.classId === selectedClass;
    const matchesSearch = file.name.toLowerCase().includes(searchFileQuery.toLowerCase());
    return matchesClass && matchesSearch;
  });

  return (
    <AppLayout>
      <div className="max-w-[1600px] mx-auto px-4 md:px-8 pb-20 space-y-8" data-testid="polis-dashboard">
        
        {/* TOP BAR / MULTI-TENANCY UI */}
        <section className="relative rounded-[2rem] overflow-hidden shadow-xl bg-white/40 backdrop-blur-xl border border-glass-border p-6 md:p-8 flex flex-col md:flex-row md:items-center justify-between gap-6">
          <div className="flex items-center gap-4">
            <div className="flex items-center justify-center w-14 h-14 rounded-2xl bg-gradient-to-br from-primary to-secondary text-white shadow-lg">
              <School className="w-8 h-8" />
            </div>
            <div>
              <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-primary/10 text-primary text-[10px] uppercase tracking-wider font-bold border border-primary/20">
                Hemera Polis
              </span>
              <h1 className="text-2xl md:text-3xl font-bold font-display text-gray-800 mt-1">Comunidade da Turma</h1>
              <p className="text-sm text-gray-500 font-medium">Mural de avisos, feed social e compartilhamento de materiais.</p>
            </div>
          </div>

          {/* Tenant selectors */}
          <div className="flex flex-col sm:flex-row gap-4 items-stretch sm:items-center">
            {/* School Selector */}
            <div className="flex flex-col gap-1 flex-1 sm:flex-initial">
              <label className="text-[10px] uppercase font-bold tracking-wider text-gray-500 px-1">Escola / Instituição</label>
              <div className="relative">
                <select
                  data-testid="school-selector"
                  value={selectedSchool}
                  onChange={(e) => setSelectedSchool(e.target.value)}
                  className="w-full sm:w-64 pl-3 pr-10 py-2.5 bg-white/70 backdrop-blur-md border border-gray-200 rounded-xl text-sm font-semibold text-gray-700 focus:outline-none focus:ring-2 focus:ring-primary/40 appearance-none transition-all cursor-pointer"
                >
                  {schoolsMock.map(school => (
                    <option key={school.id} value={school.id}>{school.name}</option>
                  ))}
                </select>
                <ChevronDown className="w-4 h-4 text-gray-500 absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none" />
              </div>
            </div>

            {/* Class Selector */}
            <div className="flex flex-col gap-1 flex-1 sm:flex-initial">
              <label className="text-[10px] uppercase font-bold tracking-wider text-gray-500 px-1">Turma Ativa</label>
              <div className="relative">
                <select
                  data-testid="class-selector"
                  value={selectedClass}
                  onChange={(e) => setSelectedClass(e.target.value)}
                  className="w-full sm:w-64 pl-3 pr-10 py-2.5 bg-white/70 backdrop-blur-md border border-gray-200 rounded-xl text-sm font-semibold text-gray-700 focus:outline-none focus:ring-2 focus:ring-primary/40 appearance-none transition-all cursor-pointer"
                >
                  {currentClasses.map(cls => (
                    <option key={cls.id} value={cls.id}>{cls.name}</option>
                  ))}
                </select>
                <ChevronDown className="w-4 h-4 text-gray-500 absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none" />
              </div>
            </div>
          </div>
        </section>

        {/* MAIN SPLIT LAYOUT (Content + Notifications Sidebar) */}
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          
          {/* Main Area (Feed/Mural/Files) */}
          <div className="lg:col-span-3 space-y-6">
            
            {/* TABS NAVIGATION */}
            <div className="flex p-1.5 rounded-2xl bg-white/40 backdrop-blur-md border border-glass-border shadow-sm max-w-md">
              {(
                [
                  { id: "mural", label: "Mural Oficial", icon: Megaphone },
                  { id: "feed", label: "Feed da Turma", icon: MessageSquare },
                  { id: "arquivos", label: "Arquivos", icon: FileText }
                ] as const
              ).map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  data-testid={`tab-${tab.id}`}
                  className={`flex items-center justify-center flex-1 gap-2.5 py-3 text-xs md:text-sm font-bold transition-all rounded-xl ${
                    activeTab === tab.id
                      ? "bg-white text-primary shadow-md border border-gray-100"
                      : "text-gray-500 hover:text-gray-800"
                  }`}
                >
                  <tab.icon className="w-4 h-4" />
                  {tab.label}
                </button>
              ))}
            </div>

            {/* TAB CONTENT: MURAL */}
            {activeTab === "mural" && (
              <div className="space-y-6" data-testid="tab-content-mural">
                {/* Professor specific form: Add Announcement */}
                {currentUserRole === "professor" && (
                  <form onSubmit={handleAddAnnouncement} className="bg-white/60 backdrop-blur-xl border border-glass-border rounded-[2rem] shadow-lg p-6 space-y-4">
                    <h3 className="text-lg font-bold text-gray-800 flex items-center gap-2">
                      <Pin className="w-5 h-5 text-primary rotate-45" />
                      Fixar Novo Aviso no Mural Oficial
                    </h3>
                    <div className="grid grid-cols-1 gap-4">
                      <input
                        type="text"
                        placeholder="Título do aviso..."
                        value={newAnnTitle}
                        onChange={(e) => setNewAnnTitle(e.target.value)}
                        className="w-full px-4 py-3 bg-white/80 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-primary/40 font-semibold"
                      />
                      <textarea
                        placeholder="Escreva a mensagem detalhada para a turma..."
                        rows={3}
                        value={newAnnContent}
                        onChange={(e) => setNewAnnContent(e.target.value)}
                        className="w-full px-4 py-3 bg-white/80 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-primary/40"
                      />
                    </div>
                    <div className="flex items-center justify-between">
                      <label className="flex items-center gap-2 text-xs font-semibold text-gray-600 cursor-pointer">
                        <input
                          type="checkbox"
                          checked={newAnnPinned}
                          onChange={(e) => setNewAnnPinned(e.target.checked)}
                          className="w-4.5 h-4.5 text-primary rounded border-gray-300 focus:ring-primary/40"
                        />
                        Fixar destaque no topo do mural
                      </label>
                      <button
                        type="submit"
                        className="px-6 py-2.5 bg-primary hover:bg-primary/95 text-white text-xs font-bold rounded-xl shadow-md transition-all flex items-center gap-2"
                      >
                        <Plus className="w-4 h-4" />
                        Publicar Comunicado
                      </button>
                    </div>
                  </form>
                )}

                {/* Announcements list */}
                <div className="space-y-4">
                  {filteredAnnouncements.length === 0 ? (
                    <div className="text-center py-16 bg-white/40 rounded-[2rem] border border-glass-border">
                      <Megaphone className="w-12 h-12 text-gray-400 mx-auto mb-3" />
                      <p className="text-sm font-semibold text-gray-500">Nenhum aviso importante neste mural ainda.</p>
                      <p className="text-xs text-gray-400 mt-1">O professor ou diretoria divulgará comunicados aqui.</p>
                    </div>
                  ) : (
                    filteredAnnouncements.map((ann) => (
                      <div 
                        key={ann.id} 
                        className={`relative overflow-hidden bg-white/70 backdrop-blur-md rounded-3xl p-6 border shadow-sm transition-all hover:shadow-md ${
                          ann.pinned ? "border-primary/30 ring-1 ring-primary/10" : "border-gray-100"
                        }`}
                      >
                        {ann.pinned && (
                          <div className="absolute top-0 right-0 bg-primary text-white text-[10px] font-bold px-3.5 py-1 rounded-bl-2xl flex items-center gap-1.5 shadow-sm">
                            <Pin className="w-3.5 h-3.5 rotate-45" />
                            Fixado
                          </div>
                        )}
                        <div className="flex items-start gap-4">
                          <div className={`w-10 h-10 rounded-full flex items-center justify-center shrink-0 shadow-inner ${
                            ann.authorRole === "professor" ? "bg-primary/10 text-primary" : "bg-purple-100 text-purple-600"
                          }`}>
                            <Megaphone className="w-5 h-5" />
                          </div>
                          <div className="space-y-2 flex-1">
                            <h4 className="text-lg font-bold text-gray-800 pr-16">{ann.title}</h4>
                            <p className="text-sm text-gray-600 leading-relaxed whitespace-pre-line">{ann.content}</p>
                            
                            <div className="flex items-center justify-between pt-2 border-t border-gray-100/50 text-[11px] font-bold text-gray-400">
                              <span className="capitalize">{ann.author} • {ann.authorRole}</span>
                              <span>{new Date(ann.createdAt).toLocaleDateString('pt-BR', {day: '2-digit', month: 'short', hour: '2-digit', minute: '2-digit'})}</span>
                            </div>
                          </div>
                        </div>
                      </div>
                    ))
                  )}
                </div>
              </div>
            )}

            {/* TAB CONTENT: FEED */}
            {activeTab === "feed" && (
              <div className="space-y-6" data-testid="tab-content-feed">
                
                {/* Post Form */}
                <form onSubmit={handleAddPost} className="bg-white/60 backdrop-blur-xl border border-glass-border rounded-[2rem] shadow-lg p-6 space-y-4">
                  <div className="flex items-start gap-4">
                    <div className="w-10 h-10 rounded-full bg-gradient-to-tr from-primary to-secondary flex items-center justify-center text-white text-sm font-bold shrink-0 shadow-md">
                      {currentUserName.charAt(0)}
                    </div>
                    <div className="flex-1">
                      <textarea
                        data-testid="feed-textarea"
                        placeholder={`Olá ${currentUserName.split(" ")[0]}, o que você deseja compartilhar com a turma hoje?`}
                        rows={3}
                        value={newPostContent}
                        onChange={(e) => setNewPostContent(e.target.value)}
                        className="w-full bg-transparent border-0 resize-none text-sm text-gray-700 placeholder-gray-400 focus:ring-0 focus:outline-none"
                      />
                    </div>
                  </div>

                  {/* Attachment Form Subsection */}
                  {showAttachForm && (
                    <div className="bg-white/90 border border-gray-100 p-4 rounded-2xl flex flex-col sm:flex-row gap-4 items-end animate-fade-in">
                      <div className="flex-1 space-y-1">
                        <label className="text-[10px] uppercase font-bold tracking-wider text-gray-500">Nome do Anexo</label>
                        <input
                          type="text"
                          placeholder="Ex: exercicios-aula"
                          value={newPostAttachName}
                          onChange={(e) => setNewPostAttachName(e.target.value)}
                          className="w-full px-3 py-2 bg-gray-50 border border-gray-200 rounded-xl text-xs focus:outline-none focus:ring-2 focus:ring-primary/40 font-semibold"
                        />
                      </div>
                      <div className="w-full sm:w-36 space-y-1">
                        <label className="text-[10px] uppercase font-bold tracking-wider text-gray-500">Extensão</label>
                        <select
                          value={newPostAttachType}
                          onChange={(e) => setNewPostAttachType(e.target.value as any)}
                          className="w-full px-3 py-2 bg-gray-50 border border-gray-200 rounded-xl text-xs focus:outline-none focus:ring-2 focus:ring-primary/40 font-semibold"
                        >
                          <option value="pdf">.pdf (Texto)</option>
                          <option value="doc">.doc (Office)</option>
                          <option value="image">.png (Imagem)</option>
                          <option value="zip">.zip (Arquivo)</option>
                        </select>
                      </div>
                    </div>
                  )}

                  <div className="flex items-center justify-between border-t border-gray-100 pt-4">
                    <button
                      type="button"
                      onClick={() => setShowAttachForm(!showAttachForm)}
                      className={`flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${
                        showAttachForm ? "bg-primary/10 text-primary" : "text-gray-500 hover:bg-gray-50"
                      }`}
                    >
                      <Upload className="w-4 h-4" />
                      {showAttachForm ? "Remover Anexo" : "Anexar Material"}
                    </button>
                    
                    <button
                      type="submit"
                      data-testid="publish-post-btn"
                      className="px-6 py-2.5 bg-primary hover:bg-primary/95 text-white text-xs font-bold rounded-xl shadow-md transition-all"
                    >
                      Publicar no Feed
                    </button>
                  </div>
                </form>

                {/* Posts List */}
                <div className="space-y-4">
                  {filteredPosts.length === 0 ? (
                    <div className="text-center py-16 bg-white/40 rounded-[2rem] border border-glass-border">
                      <MessageSquare className="w-12 h-12 text-gray-400 mx-auto mb-3" />
                      <p className="text-sm font-semibold text-gray-500">Nenhuma postagem no feed ainda.</p>
                      <p className="text-xs text-gray-400 mt-1">Compartilhe uma dúvida ou uma novidade para começar.</p>
                    </div>
                  ) : (
                    filteredPosts.map((post) => (
                      <div key={post.id} className="bg-white/70 backdrop-blur-md rounded-3xl p-6 border border-gray-100 shadow-sm space-y-4">
                        {/* Post Header */}
                        <div className="flex items-center justify-between">
                          <div className="flex items-center gap-3">
                            <div className="w-10 h-10 rounded-full bg-gray-200 flex items-center justify-center font-bold text-gray-700 text-sm">
                              {post.author.charAt(0)}
                            </div>
                            <div>
                              <div className="flex items-center gap-2">
                                <span className="font-bold text-gray-800 text-sm">{post.author}</span>
                                <span className={`px-2 py-0.5 rounded text-[9px] uppercase tracking-wider font-extrabold ${
                                  post.authorRole === "professor" ? "bg-primary/10 text-primary" : "bg-gray-100 text-gray-500"
                                }`}>
                                  {post.authorRole}
                                </span>
                              </div>
                              <span className="text-[10px] text-gray-400 font-semibold">
                                {new Date(post.createdAt).toLocaleDateString('pt-BR', {day: '2-digit', month: 'short', hour: '2-digit', minute: '2-digit'})}
                              </span>
                            </div>
                          </div>

                          {/* Options / Delete (Simulated) */}
                          {(post.author === currentUserName || currentUserRole === "professor") && (
                            <button
                              onClick={() => handleDeletePost(post.id)}
                              className="text-gray-400 hover:text-red-500 p-1.5 rounded-lg hover:bg-red-50 transition-all"
                              title="Remover Postagem"
                            >
                              <Trash2 className="w-4 h-4" />
                            </button>
                          )}
                        </div>

                        {/* Post Content */}
                        <p className="text-sm text-gray-600 leading-relaxed whitespace-pre-line">{post.content}</p>

                        {/* Post Attachment */}
                        {post.attachment && (
                          <div className="flex items-center justify-between p-4 bg-gray-50/70 border border-gray-100 rounded-2xl">
                            <div className="flex items-center gap-3">
                              {getFileIcon(post.attachment.type)}
                              <div className="text-left">
                                <p className="text-xs font-bold text-gray-700 truncate max-w-xs sm:max-w-md">{post.attachment.name}</p>
                                <p className="text-[10px] font-semibold text-gray-400 capitalize">{post.attachment.type} • {post.attachment.size}</p>
                              </div>
                            </div>
                            <a 
                              href="#" 
                              onClick={(e) => {
                                e.preventDefault();
                                toast({
                                  title: "Download Iniciado",
                                  description: `Baixando o arquivo ${post.attachment?.name} do repositório da turma.`
                                });
                              }}
                              className="px-4 py-2 bg-white hover:bg-gray-100 border border-gray-200 text-gray-700 text-xs font-bold rounded-xl transition-all shadow-sm flex items-center gap-1.5"
                            >
                              Baixar
                            </a>
                          </div>
                        )}

                        {/* Actions buttons */}
                        <div className="flex items-center gap-4 pt-2 border-t border-gray-100/50">
                          <button
                            data-testid={`like-btn-${post.id}`}
                            onClick={() => handleLikePost(post.id)}
                            className={`flex items-center gap-1.5 text-xs font-bold transition-all px-3 py-1.5 rounded-lg ${
                              post.likedByMe 
                                ? "text-red-500 bg-red-50 hover:bg-red-100/60" 
                                : "text-gray-500 hover:bg-gray-50"
                            }`}
                          >
                            <Heart className={`w-4 h-4 ${post.likedByMe ? "fill-current" : ""}`} />
                            {post.likes} Curtidas
                          </button>
                          <span className="flex items-center gap-1.5 text-xs font-bold text-gray-500 px-3 py-1.5">
                            <MessageCircle className="w-4 h-4" />
                            {post.comments.length} Comentários
                          </span>
                        </div>

                        {/* Comments section */}
                        <div className="bg-gray-50/50 rounded-2xl p-4 space-y-4">
                          {post.comments.length > 0 && (
                            <div className="space-y-3 max-h-60 overflow-y-auto pr-1">
                              {post.comments.map(c => (
                                <div key={c.id} className="text-left bg-white/70 p-3 rounded-xl border border-gray-100/60 shadow-inner">
                                  <div className="flex items-center justify-between mb-1">
                                    <span className="text-xs font-bold text-gray-800">{c.author}</span>
                                    <span className="text-[9px] text-gray-400 capitalize">{c.authorRole}</span>
                                  </div>
                                  <p className="text-xs text-gray-600 leading-relaxed">{c.content}</p>
                                </div>
                              ))}
                            </div>
                          )}
                          
                          {/* Write Comment Form */}
                          <form onSubmit={(e) => handleAddComment(post.id, e)} className="flex gap-2">
                            <input
                              type="text"
                              placeholder="Escreva um comentário rápido..."
                              value={commentInputs[post.id] || ""}
                              onChange={(e) => setCommentInputs({ ...commentInputs, [post.id]: e.target.value })}
                              className="flex-1 px-3.5 py-2 bg-white border border-gray-200 rounded-xl text-xs focus:outline-none focus:ring-2 focus:ring-primary/40 font-semibold"
                            />
                            <button
                              type="submit"
                              className="px-4 py-2 bg-primary text-white text-xs font-bold rounded-xl shadow-md hover:bg-primary/95 transition-all"
                            >
                              Enviar
                            </button>
                          </form>
                        </div>
                      </div>
                    ))
                  )}
                </div>
              </div>
            )}

            {/* TAB CONTENT: FILES */}
            {activeTab === "arquivos" && (
              <div className="space-y-6" data-testid="tab-content-arquivos">
                {/* Search Bar + Add File Button */}
                <div className="flex flex-col sm:flex-row gap-4 items-stretch sm:items-center justify-between">
                  <div className="relative flex-1 max-w-md">
                    <Search className="w-4 h-4 text-gray-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
                    <input
                      type="text"
                      placeholder="Pesquisar arquivos por nome..."
                      value={searchFileQuery}
                      onChange={(e) => setSearchFileQuery(e.target.value)}
                      className="w-full pl-10 pr-4 py-2.5 bg-white border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-primary/40"
                    />
                  </div>
                  <button
                    onClick={() => setShowUploadForm(!showUploadForm)}
                    data-testid="upload-toggle-btn"
                    className="px-5 py-2.5 bg-secondary hover:bg-secondary/95 text-white text-xs font-bold rounded-xl shadow-md transition-all flex items-center gap-2 justify-center"
                  >
                    <Upload className="w-4 h-4" />
                    {showUploadForm ? "Cancelar Upload" : "Enviar Arquivo"}
                  </button>
                </div>

                {/* Upload File Form */}
                {showUploadForm && (
                  <form onSubmit={handleUploadFile} className="bg-white/60 backdrop-blur-xl border border-glass-border rounded-[2rem] shadow-lg p-6 space-y-4">
                    <h3 className="text-lg font-bold text-gray-800 flex items-center gap-2">
                      <Upload className="w-5 h-5 text-secondary" />
                      Enviar Novo Material para a Pasta da Turma
                    </h3>
                    <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                      <div className="sm:col-span-1 space-y-1">
                        <label className="text-[10px] uppercase font-bold tracking-wider text-gray-500 px-1">Nome do Arquivo</label>
                        <input
                          type="text"
                          placeholder="Ex: roteiro-seminario"
                          value={newFileName}
                          onChange={(e) => setNewFileName(e.target.value)}
                          className="w-full px-4 py-2.5 bg-white border border-gray-200 rounded-xl text-xs focus:outline-none focus:ring-2 focus:ring-primary/40 font-semibold"
                        />
                      </div>
                      <div className="space-y-1">
                        <label className="text-[10px] uppercase font-bold tracking-wider text-gray-500 px-1">Formato</label>
                        <select
                          value={newFileType}
                          onChange={(e) => setNewFileType(e.target.value as any)}
                          className="w-full px-4 py-2.5 bg-white border border-gray-200 rounded-xl text-xs focus:outline-none focus:ring-2 focus:ring-primary/40 font-semibold"
                        >
                          <option value="pdf">.pdf (Documento PDF)</option>
                          <option value="doc">.doc (Processador Texto)</option>
                          <option value="image">.png (Imagem / Slide)</option>
                          <option value="zip">.zip (Arquivo Compactado)</option>
                        </select>
                      </div>
                      <div className="space-y-1">
                        <label className="text-[10px] uppercase font-bold tracking-wider text-gray-500 px-1">Categoria</label>
                        <select
                          value={newFileCategory}
                          onChange={(e) => setNewFileCategory(e.target.value as any)}
                          className="w-full px-4 py-2.5 bg-white border border-gray-200 rounded-xl text-xs focus:outline-none focus:ring-2 focus:ring-primary/40 font-semibold"
                        >
                          <option value="Material de Aula">Material de Aula</option>
                          <option value="Atividades">Atividades</option>
                          <option value="Leitura Complementar">Leitura Complementar</option>
                        </select>
                      </div>
                    </div>
                    <div className="flex justify-end pt-2">
                      <button
                        type="submit"
                        data-testid="submit-file-btn"
                        className="px-6 py-2.5 bg-secondary text-white text-xs font-bold rounded-xl shadow-md hover:bg-secondary/95 transition-all"
                      >
                        Salvar na Biblioteca da Turma
                      </button>
                    </div>
                  </form>
                )}

                {/* Files Grid / List */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {filteredFiles.length === 0 ? (
                    <div className="col-span-full text-center py-16 bg-white/40 rounded-[2rem] border border-glass-border">
                      <FileText className="w-12 h-12 text-gray-400 mx-auto mb-3" />
                      <p className="text-sm font-semibold text-gray-500">Nenhum arquivo encontrado nesta pasta.</p>
                      <p className="text-xs text-gray-400 mt-1">Os uploads feitos por professores e alunos aparecem aqui.</p>
                    </div>
                  ) : (
                    filteredFiles.map((file) => (
                      <div key={file.id} className="bg-white/70 backdrop-blur-md rounded-2xl p-5 border border-gray-100 shadow-sm flex items-start gap-4 transition-all hover:shadow-md">
                        <div className="mt-1">{getFileIcon(file.type)}</div>
                        <div className="flex-1 min-w-0 text-left">
                          <h4 className="font-bold text-gray-800 text-sm truncate" title={file.name}>
                            {file.name}
                          </h4>
                          <span className="inline-block px-2 py-0.5 bg-gray-100 rounded text-[9px] font-bold text-gray-500 mt-1">
                            {file.category}
                          </span>
                          <p className="text-[10px] text-gray-400 font-semibold mt-2.5">
                            Por: <strong className="text-gray-500">{file.uploadedBy}</strong> ({file.uploadedByRole})
                          </p>
                          <p className="text-[9px] text-gray-400 font-medium">
                            Enviado em: {new Date(file.uploadedAt).toLocaleDateString('pt-BR')} • {file.size}
                          </p>
                          
                          <div className="flex gap-2.5 mt-4">
                            <a 
                              href="#"
                              onClick={(e) => {
                                e.preventDefault();
                                toast({
                                  title: "Arquivo Visualizado",
                                  description: `Abrindo prévia de ${file.name} em modo de leitura.`
                                });
                              }}
                              className="px-3.5 py-1.5 bg-gray-100 hover:bg-gray-200 text-gray-700 text-[10px] font-bold rounded-lg transition-all"
                            >
                              Visualizar
                            </a>
                            <a 
                              href="#"
                              onClick={(e) => {
                                e.preventDefault();
                                toast({
                                  title: "Download Concluído",
                                  description: `Material ${file.name} salvo localmente.`
                                });
                              }}
                              className="px-3.5 py-1.5 bg-primary/10 text-primary hover:bg-primary/20 text-[10px] font-bold rounded-lg transition-all"
                            >
                              Baixar
                            </a>
                            {/* Option to delete file by creator or professor */}
                            {(file.uploadedBy === currentUserName || currentUserRole === "professor") && (
                              <button
                                onClick={() => handleDeleteFile(file.id)}
                                className="px-2.5 py-1.5 hover:bg-red-50 text-red-500 rounded-lg transition-all ml-auto"
                                title="Deletar Arquivo"
                              >
                                <Trash2 className="w-3.5 h-3.5" />
                              </button>
                            )}
                          </div>
                        </div>
                      </div>
                    ))
                  )}
                </div>
              </div>
            )}
          </div>

          {/* Right Sidebar: Real-time Community Activity */}
          <div className="lg:col-span-1 space-y-6">
            <div className="bg-white/60 backdrop-blur-xl rounded-[2rem] shadow-xl p-6 border border-glass-border">
              <h4 className="flex items-center gap-2 mb-4 text-base font-bold text-gray-800 border-b border-gray-100 pb-3">
                <Bell className="w-5 h-5 text-warning animate-pulse" />
                Atividades da Polis
              </h4>
              
              <div className="space-y-4 max-h-[450px] overflow-y-auto custom-scrollbar pr-1">
                {notifications.map((notif) => (
                  <div key={notif.id} className="text-left p-3 bg-white/70 border border-gray-100 rounded-xl space-y-1.5 shadow-sm">
                    <p className="text-xs text-gray-600 font-medium leading-relaxed">{notif.content}</p>
                    <span className="text-[9px] text-gray-400 font-bold block">
                      {new Date(notif.createdAt).toLocaleTimeString('pt-BR', {hour: '2-digit', minute: '2-digit'})}
                    </span>
                  </div>
                ))}
                {notifications.length === 0 && (
                  <p className="text-xs text-gray-400 text-center py-6">Sem atividades recentes.</p>
                )}
              </div>
            </div>
          </div>
        </div>

      </div>
    </AppLayout>
  );
};

export default Polis;
