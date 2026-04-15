import AppLayout from "@/components/layout/AppLayout";

const bibliotecaMock = [
  { id: 1, titulo: "Álgebra Linear e Aplicações", autor: "Gilbert Strang", tipo: "PDF", categoria: "Matemática", imagem: "https://images.unsplash.com/photo-1635070041078-e363dbe005cb?auto=format&fit=crop&w=300&q=80" },
  { id: 2, titulo: "Mecânica Clássica", autor: "Herbert Goldstein", tipo: "PDF", categoria: "Física", imagem: "https://images.unsplash.com/photo-1636466497217-26a8cbeaf0aa?auto=format&fit=crop&w=300&q=80" },
  { id: 3, titulo: "Dom Casmurro", autor: "Machado de Assis", tipo: "eBook", categoria: "Literatura", imagem: "https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?auto=format&fit=crop&w=300&q=80" },
  { id: 4, titulo: "Biologia Celular", autor: "Bruce Alberts", tipo: "PDF", categoria: "Biologia", imagem: "https://images.unsplash.com/photo-1530026405186-ed1f139313f8?auto=format&fit=crop&w=300&q=80" },
  { id: 5, titulo: "Introdução à Programação", autor: "Python Brasil", tipo: "Vídeo", categoria: "Tecnologia", imagem: "https://images.unsplash.com/photo-1515879218367-8466d910auj?auto=format&fit=crop&w=300&q=80" },
  { id: 6, titulo: "História do Brasil", autor: "Boris Fausto", tipo: "eBook", categoria: "História", imagem: "https://images.unsplash.com/photo-1461360370896-922624d12aa1?auto=format&fit=crop&w=300&q=80" },
];

const Biblioteca = () => {
  return (
    <AppLayout role="aluno">
      <div className="max-w-[1600px] mx-auto px-6 pb-20 space-y-8">
        <div className="flex items-center gap-4 mb-2">
          <div className="w-1.5 h-10 bg-gradient-to-b from-primary to-secondary rounded-full shadow-lg shadow-primary/30" />
          <div>
            <h1 className="text-3xl font-display font-bold text-foreground">Biblioteca Digital</h1>
            <p className="text-sm text-muted-foreground font-medium">Acesse livros, apostilas e materiais de estudo.</p>
          </div>
        </div>

        {/* Search */}
        <div className="glass-card rounded-2xl p-4 shadow-glass flex items-center gap-4">
          <div className="flex items-center flex-1 gap-3 px-4 py-3 rounded-xl bg-card border border-border">
            <i className="fas fa-search text-muted-foreground" />
            <input
              type="text"
              placeholder="Pesquisar na biblioteca..."
              className="flex-1 bg-transparent outline-none text-foreground placeholder:text-muted-foreground text-sm"
            />
          </div>
          <button className="px-6 py-3 font-bold rounded-xl bg-primary text-primary-foreground hover:bg-primary/90 transition-colors text-sm">
            Buscar
          </button>
        </div>

        {/* Grid */}
        <div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
          {bibliotecaMock.map((item) => (
            <div
              key={item.id}
              className="flex gap-4 p-4 transition-all bg-card border border-border rounded-[1.5rem] shadow-sm hover:shadow-lg hover:-translate-y-1 hover:border-primary/20 group cursor-pointer"
            >
              <div className="w-24 h-32 rounded-xl overflow-hidden bg-muted shrink-0">
                <img src={item.imagem} alt={item.titulo} className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-300" />
              </div>
              <div className="flex flex-col flex-1 min-w-0">
                <span className="text-[10px] font-bold uppercase tracking-wider text-primary mb-1">{item.categoria}</span>
                <h3 className="text-sm font-bold text-foreground group-hover:text-primary transition-colors line-clamp-2 mb-1">{item.titulo}</h3>
                <p className="text-xs text-muted-foreground mb-3">{item.autor}</p>
                <div className="mt-auto flex items-center gap-2">
                  <span className="px-2 py-0.5 text-[10px] font-bold rounded-md bg-primary/10 text-primary">{item.tipo}</span>
                  <button className="ml-auto text-xs font-bold text-primary hover:text-primary/80 transition-colors">
                    <i className="fas fa-download mr-1" /> Baixar
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </AppLayout>
  );
};

export default Biblioteca;
