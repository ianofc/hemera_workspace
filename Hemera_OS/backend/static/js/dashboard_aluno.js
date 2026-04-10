/* static/js/dashboard_aluno.js */

function appData(config) {
    return {
        // ==========================================
        // 1. ESTADO GERAL DA APLICAÇÃO
        // ==========================================
        theme: 'aurora',
        // Recebe os dados injetados pelo Django no HTML
        gender: config.gender || 'F',
        is_premium: config.is_premium === 'true' || config.is_premium === true,
        currentPath: window.location.pathname,

        // ==========================================
        // 2. CONTROLE DE MODAIS E VISIBILIDADE
        // ==========================================
        talkioOpen: false,       // Drawer do Chat
        studentIdOpen: false,    // Carteirinha Expandida
        scheduleModalOpen: false,// Modal de Horário
        ziosOpen: false,     // Assistente IA
        notificationsOpen: false,// Dropdown de Notificações

        // ==========================================
        // 3. ESTADO ESPECÍFICO DO TALKIO
        // ==========================================
        talkioMenuOpen: false,   // Menu lateral (Hambúrguer)
        activeChat: null,        // Chat atualmente aberto
        messageInput: '',        // Campo de texto
        isRecording: false,      // Estado de gravação de áudio

        // ==========================================
        // 4. DADOS MOCKADOS (Simulação de Backend)
        // ==========================================
        feed: [
            {
                id: 1, 
                author: 'Sistema', 
                title: 'Bem-vindo ao Cortex', 
                content: 'Ambiente virtual atualizado. Explore as novas funcionalidades de IA e Chat.', 
                time: 'Agora', 
                avatar: 'S', avatarColor: '#7c3aed', 
                type: 'welcome', 
                likes: 0, comments: 0
            },
            {
                id: 2, 
                author: 'Secretaria', 
                title: 'Rematrícula', 
                content: 'O período de rematrícula para o próximo semestre começa dia 15.', 
                time: '5h atrás', 
                avatar: 'Sec', avatarColor: '#059669', 
                type: 'alert', borderColor: '#059669', 
                likes: 12, comments: 0
            }
        ],

        schedule: [
            {subject: 'Matemática', time: '08:00', room: 'Sala 3B', status: 'done'},
            {subject: 'Física', time: '10:00', room: 'Lab 1', status: 'current'},
            {subject: 'Inglês', time: '13:00', room: 'Sala 3B', status: 'next'},
        ],

        chats: [
            {
                id: 1, 
                name: 'Prof. Alberto', 
                lastMsg: 'A lista está no portal.', 
                time: '14:30', 
                unread: 2, 
                online: true, 
                avatar: 'https://i.pravatar.cc/150?img=11', 
                type: 'private', 
                isSecret: false
            },
            {
                id: 2, 
                name: 'Turma 8º B', 
                lastMsg: 'Ana: Alguém fez a q4?', 
                time: '14:25', 
                unread: 5, 
                online: true, 
                avatar: 'group', 
                type: 'group', 
                isSecret: false
            },
            {
                id: 3, 
                name: 'Chat Secreto', 
                lastMsg: 'Mensagem autodestrutiva.', 
                time: 'Ontem', 
                unread: 0, 
                online: false, 
                avatar: 'lock', 
                type: 'private', 
                isSecret: true
            },
        ],

        // ==========================================
        // 5. INICIALIZAÇÃO (Lógica de Temas)
        // ==========================================
        init() {
            // Lógica de Tema Automático
            // Prioridade: Premium > Gênero > Padrão
            
            if (this.is_premium) {
                // Se for Premium, aplica os temas Dourados
                if (this.gender === 'F') {
                    this.theme = 'premium-fem'; // Dourado + Vermelho
                } else if (this.gender === 'M') {
                    this.theme = 'premium-masc'; // Dourado + Verde
                } else {
                    this.theme = 'aurora'; // Fallback
                }
            } else {
                // Se for Gratuito, aplica temas padrão
                if (this.gender === 'F') {
                    this.theme = 'pink';
                } else if (this.gender === 'M') {
                    this.theme = 'blue';
                } else {
                    this.theme = 'aurora';
                }
            }
            
            // Aqui você pode inicializar conexões de Socket.IO reais futuramente
            // const socket = io('http://seu-servidor-socket');
        },

        // ==========================================
        // 6. MÉTODOS DE UI (INTERFACE)
        // ==========================================
        setTheme(newTheme) { 
            this.theme = newTheme; 
        },
        
        openTalkio() { 
            this.talkioOpen = true; 
        },
        
        openTalkioChat(chat) { 
            this.activeChat = chat; 
            // Em mobile, fecha o menu lateral ao selecionar um chat
            if (window.innerWidth < 768) {
                this.talkioMenuOpen = false;
            }
        },

        // ==========================================
        // 7. MÉTODOS AVANÇADOS (MÍDIA/APIs)
        // ==========================================
        
        // Gravação de Áudio (Microfone)
        async toggleAudioRecording() {
            if (!this.isRecording) {
                try {
                    // Verifica suporte do navegador
                    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
                        alert("Seu navegador não suporta gravação de áudio.");
                        return;
                    }

                    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                    this.isRecording = true;
                    
                    // TODO: Conectar stream ao MediaRecorder real aqui
                    console.log("Gravação iniciada...");
                    
                } catch (err) {
                    alert("Permissão de microfone negada ou dispositivo não encontrado.");
                    console.error(err);
                }
            } else {
                this.isRecording = false;
                // TODO: Parar MediaRecorder e processar o blob de áudio
                console.log("Gravação parada.");
            }
        },

        // Acesso à Câmera
        async openCamera() {
            try {
                if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
                    alert("Seu navegador não suporta acesso à câmera.");
                    return;
                }

                const stream = await navigator.mediaDevices.getUserMedia({ video: true });
                
                // Em produção: Injetar stream em um <video> dentro de um modal
                alert("Câmera ativada com sucesso! (Stream recebido)");
                
                // Desligar câmera logo após o teste para não manter a luz acesa
                stream.getTracks().forEach(track => track.stop());
            } catch (err) {
                alert("Erro ao acessar câmera: " + err.message);
            }
        },

        // Anexar Arquivos (Simulação)
        triggerAttachment() {
            // Aqui você dispararia um click em um <input type="file" hidden>
            alert("Abrindo explorador de arquivos...");
        },

        // Criar Chat Secreto
        createSecretChat() {
            // Lógica para iniciar chat E2EE
            alert("Iniciando troca de chaves E2EE (Criptografia Ponta-a-Ponta)...");
        }
    }
}