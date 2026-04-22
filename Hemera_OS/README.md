# 🦅 Hemera OS

> **O Sistema Operativo Educacional**  
> Focado puramente na vivência escolar: Alunos, Professores e Ensino.

O **Hemera OS** é o ecossistema educacional construído para reimaginar o dia a dia pedagógico. Ele não é um sistema de contabilidade ou de recursos humanos; o Hemera é a interface viva da escola. É onde a jornada do aluno acontece e onde a regência do professor se torna dinâmica, unindo uma usabilidade impecável a uma Inteligência Artificial focada no ensino.

---

## 🧭 O Ecossistema Hemera

O Hemera OS opera sob pilares tecnológicos projetados para a sala de aula e para a experiência do aluno em casa:

### 1. O Motor Pedagógico (Backend Django)
A estrutura sólida que mantém a organização acadêmica.
- **Lumenios & Pedagógico**: Gestão exclusiva do ambiente de aprendizado (Turmas, Diários de Classe, Notas, Desempenho e Matriz Escolar).
- **Consistência MEC/BNCC**: Estruturação atenta às diretrizes da Base Nacional Comum Curricular.

### 2. A Vitrine Dinâmica (Frontend React/Vite)
A interface de usuário (UI) projetada para manter alunos e educadores engajados, utilizando **Glassmorphism**, animações com Framer Motion e design reativo. 
- Dashboards customizados por nível: **Creche**, **Ensino Fundamental**, **Ensino Médio** e **Graduação**. A linguagem e a estética se adaptam à idade do aluno.
- Aplicações responsivas e PWA para uso imersivo.

### 3. A Mente Educacional: PentaIA
O diferencial cognitivo do Hemera. A **PentaIA** atua ativamente para potencializar o processo de aprendizado:
- **Agentes Pedagógicos**: Lêm o diário dos alunos e emitem feedback de mentoria (Aconselhamento por Inteligência Artificial), montando trilhas extras quando o desempenho em uma disciplina cai.
- **Suporte ao Professor**: O gerador de bancos de questões da PentaIA cria avaliações inteiras ajustadas à BNCC em segundos.
- **Heimdall**: A camada de privacidade irreversível. O Heimdall garante blindagem AES-256 para que informações confidenciais das crianças e adolescentes jamais vazem nas requisições da Inteligência Artificial.

---

## 🔄 Fluxos de Usuário no Hemera

### O Fluxo do Aluno
O aluno interage com um ambiente de desenvolvimento pessoal, não uma simples tabela de notas acadêmicas.
1. **Identidade Visual**: Entra no dashboard específico da sua fase escolar (ex: Fundamental).
2. **Mentoria Virtual**: Visualiza os conselhos gerados pela *PentaIA* para melhorar seus estudos baseado no seu rendimento atual.
3. **Engajamento**: Acompanha seu próprio progresso via gráficos amigáveis, acessa a biblioteca e o ambiente virtual de forma intuitiva.

### O Fluxo do Professor
O professor ganha tempo e poder de fogo pedagógico.
1. **Regência**: Controle total e ágil sobre a sala de aula e avaliações.
2. **Integração Moodle**: Caderneta automatizada diretamente pelas integrações de LMS.
3. **Automação de Avaliações**: Utiliza a *PentaIA* para criar testes do zero, poupando o fim de semana que usaria elaborando questões.

---

## 🚀 Como Rodar o Hemera OS Localmente

Certifique-se de que o Docker e o `docker compose` estão instalados em seu ambiente.

```bash
# 1. Clone ou entre no repositório do workspace
cd Hemera_workspace

# 2. Inicie a stack
docker compose up --build -d

# 3. Acesse o Hemera
# Frontend (Aluno/Professor): http://localhost:5173
# Backend (Motor):       http://localhost:8000
# PentaIA (Mente):       http://localhost:8001
```
