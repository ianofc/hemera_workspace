
const ThemeEngine = {
    init() {
        const savedTheme = localStorage.getItem('nio_theme') || 'aurora';
        this.applyTheme(savedTheme);
    },
    applyTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('nio_theme', theme);
    },
    toggleA11y(cls) {
        document.documentElement.classList.toggle(cls);
    }
};
document.addEventListener('DOMContentLoaded', () => ThemeEngine.init());
