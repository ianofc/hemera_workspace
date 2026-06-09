import React, { useState, useEffect } from 'react';
import { useLyceum, Lesson } from '../../contexts/LyceumContext';
import { PlayCircle, FileText, CheckCircle2, ChevronRight, AlertCircle, RefreshCw, Sparkles, Award } from 'lucide-react';
import { toast } from 'sonner';
import { motion, AnimatePresence } from 'framer-motion';

interface LessonViewerProps {
  courseId: number;
  moduleId: number;
  lesson: Lesson;
  onLessonCompleted?: () => void;
}

export const LessonViewer: React.FC<LessonViewerProps> = ({ courseId, moduleId, lesson, onLessonCompleted }) => {
  const { completeLesson, unlockBadge } = useLyceum();
  
  // Estados para Quiz
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [selectedOption, setSelectedOption] = useState<number | null>(null);
  const [isAnswerChecked, setIsAnswerChecked] = useState(false);
  const [isAnswerCorrect, setIsAnswerCorrect] = useState(false);
  const [wrongAnswersCount, setWrongAnswersCount] = useState(0);
  const [quizFinished, setQuizFinished] = useState(false);

  // Reseta estados quando a lição muda
  useEffect(() => {
    setCurrentQuestionIndex(0);
    setSelectedOption(null);
    setIsAnswerChecked(false);
    setIsAnswerCorrect(false);
    setWrongAnswersCount(0);
    setQuizFinished(false);
  }, [lesson]);

  const handleTextVideoComplete = () => {
    completeLesson(courseId, moduleId, lesson.id);
    toast.success(`Parabéns! Você concluiu a lição e ganhou +${lesson.xpReward} XP!`);
    if (onLessonCompleted) {
      onLessonCompleted();
    }
  };

  const handleOptionSelect = (index: number) => {
    if (isAnswerChecked) return;
    setSelectedOption(index);
  };

  const handleCheckAnswer = () => {
    if (selectedOption === null || !lesson.quiz) return;

    const correctIndex = lesson.quiz[currentQuestionIndex].correctOptionIndex;
    const correct = selectedOption === correctIndex;

    setIsAnswerCorrect(correct);
    setIsAnswerChecked(true);

    if (!correct) {
      setWrongAnswersCount(prev => prev + 1);
      toast.error('Ops! Resposta incorreta. Tente novamente.');
    } else {
      toast.success('Excelente! Resposta correta.');
    }
  };

  const handleNextQuestion = () => {
    if (!lesson.quiz) return;

    setSelectedOption(null);
    setIsAnswerChecked(false);
    setIsAnswerCorrect(false);

    if (currentQuestionIndex + 1 < lesson.quiz.length) {
      setCurrentQuestionIndex(prev => prev + 1);
    } else {
      // Finalizou o quiz!
      setQuizFinished(true);
      completeLesson(courseId, moduleId, lesson.id);
      
      // Se não errou nenhuma, destrava o badge de quiz perfeito!
      if (wrongAnswersCount === 0) {
        unlockBadge('badge-perfect-quiz');
        toast.success(`Incrível! Quiz Perfeito! Você ganhou o badge Cérebro de Aço! +${lesson.xpReward} XP`);
      } else {
        toast.success(`Parabéns! Quiz concluído. Você ganhou +${lesson.xpReward} XP!`);
      }

      if (onLessonCompleted) {
        onLessonCompleted();
      }
    }
  };

  const handleRetryQuestion = () => {
    setSelectedOption(null);
    setIsAnswerChecked(false);
  };

  return (
    <div className="relative flex flex-col w-full h-full min-h-[450px]">
      <AnimatePresence mode="wait">
        {/* Lição Concluída (Quiz) */}
        {quizFinished && (
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0 }}
            className="flex-1 flex flex-col items-center justify-center p-8 text-center bg-success/5 border border-success/15 rounded-3xl"
          >
            <div className="flex items-center justify-center w-20 h-20 bg-success/10 text-success rounded-full mb-6">
              <Sparkles className="w-12 h-12 animate-bounce" />
            </div>
            <h3 className="text-2xl font-bold font-display text-foreground mb-2">Lição Gamificada Concluída!</h3>
            <p className="text-muted-foreground text-sm max-w-md mb-6">
              Você completou com sucesso todos os desafios deste módulo interativo. Seu conhecimento foi testado e aprovado!
            </p>
            
            <div className="flex gap-4 mb-6">
              <div className="p-4 bg-card border rounded-2xl flex items-center gap-3">
                <Award className="w-8 h-8 text-primary" />
                <div className="text-left">
                  <p className="text-[10px] font-bold text-muted-foreground uppercase tracking-wider">XP Recompensa</p>
                  <p className="text-lg font-black text-primary">+{lesson.xpReward} XP</p>
                </div>
              </div>

              {wrongAnswersCount === 0 && (
                <div className="p-4 bg-success/10 border border-success/20 rounded-2xl flex items-center gap-3 text-success">
                  <span className="text-2xl">⚡</span>
                  <div className="text-left">
                    <p className="text-[10px] font-bold uppercase tracking-wider">Quiz Perfeito</p>
                    <p className="text-xs font-bold">Badge Desbloqueado!</p>
                  </div>
                </div>
              )}
            </div>

            <button
              onClick={() => setQuizFinished(false)}
              className="px-6 py-2.5 bg-primary text-primary-foreground font-bold rounded-xl shadow-md hover:bg-primary/95 transition-all text-sm"
            >
              Revisar Conteúdo
            </button>
          </motion.div>
        )}

        {/* Visualização da Lição com base no Tipo */}
        {!quizFinished && (
          <motion.div
            key={lesson.id}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            className="flex-1 flex flex-col"
          >
            {/* Cabeçalho da Lição */}
            <div className="pb-4 border-b border-border mb-6">
              <div className="flex items-center gap-2 mb-2">
                <span className="px-2.5 py-1 text-[10px] font-bold rounded-full bg-primary/10 text-primary border border-primary/20 flex items-center gap-1">
                  {lesson.type === 'VIDEO' && <PlayCircle className="w-3.5 h-3.5" />}
                  {lesson.type === 'TEXTO' && <FileText className="w-3.5 h-3.5" />}
                  {lesson.type === 'EXERCICIO' && <CheckCircle2 className="w-3.5 h-3.5" />}
                  {lesson.type}
                </span>
                <span className="text-xs font-bold text-muted-foreground">+{lesson.xpReward} XP Recompensa</span>
              </div>
              <h2 className="text-2xl font-bold font-display text-foreground">{lesson.title}</h2>
            </div>

            {/* Conteúdo de Vídeo */}
            {lesson.type === 'VIDEO' && (
              <div className="flex-1 flex flex-col gap-6">
                <div className="relative w-full aspect-video rounded-2xl overflow-hidden bg-black shadow-lg">
                  {lesson.videoUrl ? (
                    <iframe
                      src={lesson.videoUrl}
                      title={lesson.title}
                      className="absolute inset-0 w-full h-full border-0"
                      allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                      allowFullScreen
                    />
                  ) : (
                    <div className="absolute inset-0 flex flex-col items-center justify-center text-gray-500">
                      <PlayCircle className="w-16 h-16 opacity-35 mb-2 text-white" />
                      <p className="text-xs text-white">Player de Vídeo Integrado</p>
                    </div>
                  )}
                </div>

                <div className="bg-muted/30 p-5 rounded-2xl border border-border">
                  <h4 className="font-bold text-sm text-foreground mb-2">Resumo da Lição</h4>
                  <p className="text-sm text-foreground/80 leading-relaxed">{lesson.content}</p>
                </div>

                <div className="flex justify-end mt-auto pt-4">
                  <button
                    onClick={handleTextVideoComplete}
                    className={`flex items-center gap-2 px-8 py-3.5 font-bold transition-all shadow-lg rounded-xl text-sm ${
                      lesson.completed
                        ? 'bg-success/20 text-success border border-success/30 cursor-default'
                        : 'bg-primary hover:bg-primary/90 text-primary-foreground hover:-translate-y-0.5'
                    }`}
                  >
                    <CheckCircle2 className="w-4 h-4" />
                    {lesson.completed ? 'Lição Concluída' : 'Marcar como Concluido (+XP)'}
                  </button>
                </div>
              </div>
            )}

            {/* Conteúdo de Texto */}
            {lesson.type === 'TEXTO' && (
              <div className="flex-1 flex flex-col gap-6">
                <div className="flex-1 text-foreground/90 leading-relaxed text-sm bg-card border border-border/80 rounded-2xl p-6 md:p-8 space-y-4">
                  {lesson.content.split('\n\n').map((para, i) => (
                    <p key={i}>{para}</p>
                  ))}
                </div>

                <div className="flex justify-end mt-auto pt-4">
                  <button
                    onClick={handleTextVideoComplete}
                    className={`flex items-center gap-2 px-8 py-3.5 font-bold transition-all shadow-lg rounded-xl text-sm ${
                      lesson.completed
                        ? 'bg-success/20 text-success border border-success/30 cursor-default'
                        : 'bg-primary hover:bg-primary/90 text-primary-foreground hover:-translate-y-0.5'
                    }`}
                  >
                    <CheckCircle2 className="w-4 h-4" />
                    {lesson.completed ? 'Lição Concluída' : 'Concluir Leitura (+XP)'}
                  </button>
                </div>
              </div>
            )}

            {/* Conteúdo de Exercício / Quiz */}
            {lesson.type === 'EXERCICIO' && lesson.quiz && (
              <div className="flex-1 flex flex-col gap-4">
                <div className="flex justify-between items-center text-xs font-bold text-muted-foreground px-1 mb-2">
                  <span>QUESTÃO {currentQuestionIndex + 1} DE {lesson.quiz.length}</span>
                  <span>Erros: {wrongAnswersCount}</span>
                </div>

                {/* Pergunta */}
                <div className="p-6 bg-card border border-border rounded-2xl shadow-sm">
                  <h3 className="text-base font-bold text-foreground leading-relaxed">
                    {lesson.quiz[currentQuestionIndex].question}
                  </h3>
                </div>

                {/* Alternativas */}
                <div className="space-y-2 mt-2">
                  {lesson.quiz[currentQuestionIndex].options.map((option, index) => {
                    const isSelected = selectedOption === index;
                    const isCorrectOption = index === lesson.quiz![currentQuestionIndex].correctOptionIndex;
                    
                    let optionStyle = 'border-border bg-card hover:bg-muted/10';
                    if (isSelected) optionStyle = 'border-primary bg-primary/5';
                    
                    if (isAnswerChecked) {
                      if (isSelected) {
                        optionStyle = isAnswerCorrect
                          ? 'border-success bg-success/10 text-success'
                          : 'border-danger bg-danger/10 text-danger';
                      } else if (isCorrectOption) {
                        // Mostra a correta se o aluno errou
                        optionStyle = 'border-success bg-success/5 text-success';
                      } else {
                        optionStyle = 'border-border/40 opacity-50 cursor-default';
                      }
                    }

                    return (
                      <button
                        key={index}
                        onClick={() => handleOptionSelect(index)}
                        disabled={isAnswerChecked}
                        className={`w-full flex items-center justify-between p-4 border rounded-xl text-left transition-all text-sm font-medium ${optionStyle}`}
                      >
                        <span>{option}</span>
                        {isAnswerChecked && isSelected && (
                          isAnswerCorrect ? (
                            <CheckCircle2 className="w-5 h-5 text-success shrink-0" />
                          ) : (
                            <AlertCircle className="w-5 h-5 text-danger shrink-0" />
                          )
                        )}
                      </button>
                    );
                  })}
                </div>

                {/* Botões de Controle */}
                <div className="flex justify-end items-center gap-3 mt-auto pt-6 border-t border-border">
                  {!isAnswerChecked ? (
                    <button
                      onClick={handleCheckAnswer}
                      disabled={selectedOption === null}
                      className="px-6 py-2.5 bg-primary text-primary-foreground disabled:opacity-50 font-bold rounded-xl shadow-lg hover:bg-primary/95 transition-all text-sm"
                    >
                      Verificar Resposta
                    </button>
                  ) : (
                    <>
                      {!isAnswerCorrect && (
                        <button
                          onClick={handleRetryQuestion}
                          className="flex items-center gap-1.5 px-4 py-2.5 border border-border bg-card text-foreground hover:bg-muted font-bold rounded-xl transition-all text-sm"
                        >
                          <RefreshCw className="w-4 h-4" /> Tentar Novamente
                        </button>
                      )}
                      
                      {(isAnswerCorrect || isAnswerChecked) && (
                        <button
                          onClick={handleNextQuestion}
                          className="flex items-center gap-1 px-6 py-2.5 bg-success text-white font-bold rounded-xl shadow-lg hover:bg-success/95 transition-all text-sm"
                        >
                          Próximo <ChevronRight className="w-4 h-4" />
                        </button>
                      )}
                    </>
                  )}
                </div>
              </div>
            )}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};
