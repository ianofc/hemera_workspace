# io_zios/core/agents.py

class BaseAgent:
    def __init__(self, context: dict):
        self.context = context

    def process(self, message: str) -> str:
        return "Estou ouvindo. Como posso ajudar?"

class PedagogicalAgent(BaseAgent):
    """ Atende Professores e Coordenadores """
    def process(self, message: str) -> str:
        msg = message.lower()
        user_name = self.context.get('user_name', 'Professor(a)')
        
        if "plano" in msg:
            return "Posso ajudar a montar seu plano de aula. Qual o tema e a turma?"
        if "nota" in msg or "desempenho" in msg:
            return "Entendido. Quer que eu analise o desempenho da turma inteira ou de um aluno específico?"
        if "indisciplina" in msg:
            return "Situação delicada. Recomendo registrar no diário e, se grave, notificar a coordenação. Quer abrir o formulário de ocorrência?"
        
        return f"Olá {user_name}. Sou seu Copiloto Pedagógico. Posso ajudar com Provas, Planos ou Análise de Turma."

class FamilyAgent(BaseAgent):
    """ Atende Pais e Responsáveis """
    def process(self, message: str) -> str:
        msg = message.lower()
        aluno = self.context.get('filho_nome', 'seu filho')
        
        if "nota" in msg or "boletim" in msg:
            return f"Consultei o boletim do {aluno}. As notas de Matemática subiram, mas História precisa de atenção. Quer ver o gráfico?"
        if "boleto" in msg or "mensalidade" in msg:
            return "Verifiquei no financeiro. A mensalidade deste mês está em aberto. Deseja que eu envie o código de barras agora?"
        if "reunião" in msg:
            return "A próxima reunião de pais é dia 15. Posso confirmar sua presença?"
            
        return f"Olá! Sou o assistente da escola. Como posso ajudar na jornada escolar do {aluno} hoje?"

class StudentAgent(BaseAgent):
    """ Atende Alunos (Tutor & Amigo) """
    def process(self, message: str) -> str:
        msg = message.lower()
        if "prova" in msg:
            return "Sua próxima prova é de Geografia na quinta-feira. Quer revisar?"
        if "ajuda" in msg:
            return "Claro! Mande a questão que eu te ajudo a raciocinar (sem dar a resposta pronta, hein!)."
            
        return "E aí! Travou em alguma matéria ou quer saber do calendário?"

class AdminAgent(BaseAgent):
    """ Atende Direção, Financeiro e RH """
    def process(self, message: str) -> str:
        msg = message.lower()
        if "caixa" in msg or "financeiro" in msg:
            return "O fluxo de caixa desta semana está positivo. Temos 15% de inadimplência na turma do 3º ano. Sugiro uma ação de cobrança."
        if "contrato" in msg:
            return "Acesso aos contratos liberado. Qual funcionário você está buscando?"
            
        return "Painel Executivo Ativo. Aguardando ordens estratégicas."

class AgentFactory:
    @staticmethod
    def get_agent(role: str, context: dict) -> BaseAgent:
        # Normaliza para maiúsculo para evitar erros
        role = str(role).upper()
        
        if role in ['PROFESSOR', 'COORDENADOR', 'DOCENTE']:
            return PedagogicalAgent(context)
        elif role in ['RESPONSAVEL', 'PAI', 'MAE', 'FAMILY']:
            return FamilyAgent(context)
        elif role == 'ALUNO':
            return StudentAgent(context)
        elif role in ['ADMIN', 'DIRETOR', 'FINANCEIRO', 'RH']:
            return AdminAgent(context)
        else:
            return BaseAgent(context)