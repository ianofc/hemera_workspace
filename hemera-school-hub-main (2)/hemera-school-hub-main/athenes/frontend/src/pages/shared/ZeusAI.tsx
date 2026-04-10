import { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Send, Sparkles, Bot, User, BookOpen, Lightbulb, HelpCircle } from 'lucide-react';
import { GlassCard } from '../../components/ui/GlassCard';

interface Message {
  id: string;
  type: 'user' | 'ai';
  content: string;
  suggestions?: string[];
}

export const ZeusAI = () => {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 'welcome',
      type: 'ai',
      content: 'Olá! Sou o Zeus, seu assistente de aprendizagem no ATHENES. Como posso ajudar você hoje?',
      suggestions: ['Explique esse conteúdo', 'Crie um resumo', 'Questões de prática']
    }
  ]);
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      type: 'user',
      content: input
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsTyping(true);

    setTimeout(() => {
      setIsTyping(false);
      setMessages(prev => [...prev, {
        id: (Date.now() + 1).toString(),
        type: 'ai',
        content: 'Entendi sua pergunta! Baseado no contexto de Cálculo Diferencial, posso explicar que a derivada representa a taxa instantânea de variação de uma função...',
        suggestions: ['Exemplo prático', 'Ver fórmulas', 'Exercícios relacionados']
      }]);
    }, 2000);
  };

  const quickActions = [
    { icon: BookOpen, label: 'Resumir Aula', prompt: 'Faça um resumo da última aula' },
    { icon: Lightbulb, label: 'Explicar Tópico', prompt: 'Explique o conceito de...' },
    { icon: HelpCircle, label: 'Quiz Rápido', prompt: 'Crie 5 questões sobre...' },
  ];

  return (
    <div className="h-[calc(100vh-8rem)] flex gap-6">
      <div className="flex-1 flex flex-col">
        <GlassCard className="flex-1 flex flex-col mb-4 overflow-hidden" hover={false}>
          <div className="flex items-center gap-3 pb-4 border-b border-white/30 mb-4">
            <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-zeus-primary to-zeus-secondary flex items-center justify-center shadow-lg">
              <Sparkles className="text-white" size={24} />
            </div>
            <div>
              <h2 className="text-xl font-bold text-slate-800">Zeus AI</h2>
              <p className="text-sm text-slate-500">Assistente de Aprendizagem Inteligente</p>
            </div>
            <div className="ml-auto">
              <span className="px-3 py-1 rounded-full bg-green-100 text-green-700 text-xs font-medium">
                Online
              </span>
            </div>
          </div>

          <div className="flex-1 overflow-y-auto space-y-4 pr-2">
            <AnimatePresence>
              {messages.map((msg) => (
                <motion.div
                  key={msg.id}
                  initial={{ opacity: 0, x: msg.type === 'user' ? 20 : -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  className={`flex gap-3 ${msg.type === 'user' ? 'flex-row-reverse' : ''}`}
                >
                  <div className={`w-10 h-10 rounded-full flex items-center justify-center flex-shrink-0 ${
                    msg.type === 'user' ? 'alpine-gradient' : 'zeus-gradient'
                  }`}>
                    {msg.type === 'user' ? <User size={18} className="text-white" /> : <Bot size={18} className="text-white" />}
                  </div>

                  <div className={`max-w-[70%] ${msg.type === 'user' ? 'items-end' : 'items-start'} flex flex-col`}>
                    <div className={`glass p-4 rounded-2xl ${
                      msg.type === 'user' ? 'rounded-tr-sm bg-sky-100/50' : 'rounded-tl-sm bg-white/80'
                    }`}>
                      <p className="text-slate-700 leading-relaxed">{msg.content}</p>
                    </div>

                    {msg.suggestions && (
                      <div className="flex flex-wrap gap-2 mt-2">
                        {msg.suggestions.map((suggestion, i) => (
                          <button
                            key={i}
                            onClick={() => setInput(suggestion)}
                            className="px-3 py-1.5 text-xs rounded-full bg-white/60 hover:bg-white/90 text-slate-600 border border-white/40 transition-colors"
                          >
                            {suggestion}
                          </button>
                        ))}
                      </div>
                    )}
                  </div>
                </motion.div>
              ))}
            </AnimatePresence>

            {isTyping && (
              <motion.div className="flex gap-3">
                <div className="w-10 h-10 rounded-full zeus-gradient flex items-center justify-center">
                  <Bot size={18} className="text-white" />
                </div>
                <div className="glass p-4 rounded-2xl rounded-tl-sm flex items-center gap-2">
                  <div className="flex gap-1">
                    <div className="w-2 h-2 bg-indigo-400 rounded-full animate-bounce" />
                    <div className="w-2 h-2 bg-indigo-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }} />
                    <div className="w-2 h-2 bg-indigo-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }} />
                  </div>
                  <span className="text-slate-500 text-sm ml-2">Zeus está pensando...</span>
                </div>
              </motion.div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <form onSubmit={handleSubmit} className="mt-4 flex gap-3">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Digite sua pergunta ou dúvida..."
              className="flex-1 glass-input"
            />
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              type="submit"
              disabled={isTyping || !input.trim()}
              className="glass-button zeus-gradient text-white border-0 disabled:opacity-50"
            >
              <Send size={20} />
            </motion.button>
          </form>
        </GlassCard>
      </div>

      <div className="w-80 space-y-4">
        <GlassCard delay={0.1}>
          <h3 className="font-semibold text-slate-800 mb-3 flex items-center gap-2">
            <Sparkles size={18} className="text-zeus-primary" />
            Ações Rápidas
          </h3>
          <div className="space-y-2">
            {quickActions.map((action, idx) => (
              <button
                key={idx}
                onClick={() => setInput(action.prompt)}
                className="w-full flex items-center gap-3 p-3 rounded-xl hover:bg-white/60 transition-colors text-left group"
              >
                <div className="w-10 h-10 rounded-lg bg-sky-100 flex items-center justify-center group-hover:scale-110 transition-transform">
                  <action.icon size={18} className="text-sky-600" />
                </div>
                <span className="text-sm font-medium text-slate-700">{action.label}</span>
              </button>
            ))}
          </div>
        </GlassCard>

        <GlassCard delay={0.2}>
          <h3 className="font-semibold text-slate-800 mb-3">Contexto Atual</h3>
          <div className="space-y-3 text-sm text-slate-600">
            <div className="flex justify-between">
              <span>Matéria:</span>
              <span className="font-medium text-slate-800">Matemática</span>
            </div>
            <div className="flex justify-between">
              <span>Aula:</span>
              <span className="font-medium text-slate-800">Cálculo Diferencial</span>
            </div>
            <div className="flex justify-between">
              <span>Progresso:</span>
              <span className="font-medium text-green-600">75%</span>
            </div>
          </div>
        </GlassCard>
      </div>
    </div>
  );
};