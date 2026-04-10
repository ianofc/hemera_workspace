
document.addEventListener('alpine:init', () => {
    Alpine.store('nav', {
        drawers: {
            talkio: false,
            notif: false,
            profile: false,
            theme: false,
            a11y: false,
            zios: false
        },
        toggle(name) {
            // Se abrir qualquer gaveta lateral, fecha o dropdown do perfil
            if (name !== 'profile') this.drawers.profile = false;
            
            // Garante que apenas UMA gaveta lateral abra por vez
            const sideDrawers = ['talkio', 'notif', 'theme', 'a11y', 'zios'];
            if (sideDrawers.includes(name)) {
                sideDrawers.forEach(k => {
                    if (k !== name) this.drawers[k] = false;
                });
            }
            this.drawers[name] = !this.drawers[name];
        }
    });
});
