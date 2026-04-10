const TalkioApp = {
    init() {
        const form = document.getElementById('talkioForm');
        const input = document.getElementById('promptInput');
        const area = document.getElementById('messagesArea');

        if (!form) return;

        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const text = input.value.trim();
            if(!text) return;

            this.appendMessage('user', text);
            input.value = '';
            
            // Simulação de Resposta Real do Talkio
            this.showTyping();
            setTimeout(() => {
                this.removeTyping();
                this.appendMessage('ai', `Entendido! Estou processando sua dúvida sobre "${text}". Como seu assistente NioCortex, posso te ajudar a organizar seus estudos ou explicar matérias.`);
            }, 1500);
        });
    },

    appendMessage(role, text) {
        const area = document.getElementById('messagesArea');
        const div = document.createElement('div');
        div.className = `msg-bubble msg-${role} animate-fade-in`;
        div.innerHTML = text;
        area.appendChild(div);
        area.scrollTop = area.scrollHeight;
    },

    showTyping() {
        const area = document.getElementById('messagesArea');
        const div = document.createElement('div');
        div.id = 'talkio-typing';
        div.className = 'msg-bubble msg-ai italic opacity-70';
        div.innerHTML = '<i class="fas fa-ellipsis-h fa-beat"></i> Talkio está pensando...';
        area.appendChild(div);
        area.scrollTop = area.scrollHeight;
    },

    removeTyping() {
        const typing = document.getElementById('talkio-typing');
        if(typing) typing.remove();
    }
};

document.addEventListener('DOMContentLoaded', () => TalkioApp.init());