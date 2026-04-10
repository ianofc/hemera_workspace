// static/social/js/reels/player.js

document.addEventListener('DOMContentLoaded', function() {
    const videos = document.querySelectorAll('video');

    // Função para controlar o mute ao clicar
    videos.forEach(video => {
        video.addEventListener('click', function() {
            this.muted = !this.muted;
            // Opcional: Mostrar ícone de som na tela
        });
    });

    // Otimização: Pausar vídeos que não estão na tela (Intersection Observer)
    let observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (!entry.isIntersecting) {
                entry.target.pause();
            } else {
                entry.target.play();
            }
        });
    }, { threshold: 0.5 });

    videos.forEach(video => observer.observe(video));
});