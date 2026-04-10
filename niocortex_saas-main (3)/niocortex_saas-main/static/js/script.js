document.addEventListener('DOMContentLoaded', () => {
    console.log('NioCortex Frontend Loaded 🚀');

    // Fechar mensagens flash automaticamente
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.transition = "opacity 0.5s ease";
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 500);
        }, 5000);
    });
});

// Helper CSRF
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// --- LÓGICA DO MODAL ---
const modal = document.getElementById('modal-analise-ia');
const backdrop = document.getElementById('modal-backdrop');
const panel = document.getElementById('modal-panel');

function abrirModalIA(dados) {
    if (!modal) return;

    // 1. Preencher Texto
    const elResumo = document.getElementById('ia-resumo');
    if (elResumo) elResumo.textContent = dados.resumo_desempenho;
    
    // 2. Preencher Listas
    const renderLista = (items, iconClass, colorClass) => {
        return items.map(item => `
            <li class="flex items-start gap-2 text-sm text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700/50 p-2 rounded-lg border border-gray-100 dark:border-gray-600 shadow-sm">
                <i class="${iconClass} mt-1 ${colorClass}"></i>
                <span>${item}</span>
            </li>
        `).join('');
    };

    const elFortes = document.getElementById('ia-fortes');
    if (elFortes) elFortes.innerHTML = renderLista(dados.pontos_fortes, 'fas fa-check', 'text-green-500');
    
    const elAtencao = document.getElementById('ia-atencao');
    if (elAtencao) elAtencao.innerHTML = renderLista(dados.pontos_atencao, 'fas fa-exclamation-circle', 'text-amber-500');

    // 3. Preencher Sugestões
    const elSugestoes = document.getElementById('ia-sugestoes');
    if (elSugestoes) {
        elSugestoes.innerHTML = dados.sugestoes_acao.map(s => `
            <div class="flex gap-3 items-start p-3 rounded-lg bg-indigo-50 dark:bg-indigo-900/20 border border-indigo-100 dark:border-indigo-800/30">
                <div class="min-w-[24px] h-6 flex items-center justify-center rounded-full bg-indigo-100 text-indigo-600 text-xs font-bold">
                    <i class="fas fa-lightbulb"></i>
                </div>
                <p class="text-sm text-indigo-900 dark:text-indigo-200 leading-snug">${s}</p>
            </div>
        `).join('');
    }

    // 4. Configurar Badge de Risco (Correção de Erro de Sintaxe)
    const badge = document.getElementById('ia-risco');
    if (badge) {
        badge.textContent = dados.risco_evasao;
        
        // Define a classe base
        let baseClass = 'px-2 py-0.5 rounded text-xs font-bold uppercase border ';
        
        // Adiciona cores conforme o risco
        const risco = dados.risco_evasao.toLowerCase();
        if (risco.includes('alto')) {
            baseClass += 'bg-red-50 text-red-700 border-red-200';
        } else if (risco.includes('médio') || risco.includes('medio')) {
            baseClass += 'bg-amber-50 text-amber-700 border-amber-200';
        } else {
            baseClass += 'bg-emerald-50 text-emerald-700 border-emerald-200';
        }
        
        // Aplica a classe final de uma vez (evita erros de property assignment em alguns parsers)
        badge.setAttribute('class', baseClass);
    }

    // 5. Mostrar Modal
    modal.classList.remove('hidden');
    requestAnimationFrame(() => {
        backdrop.classList.remove('opacity-0');
        panel.classList.remove('opacity-0', 'translate-y-4', 'sm:scale-95');
        panel.classList.add('opacity-100', 'translate-y-0', 'sm:scale-100');
    });
}

function fecharModalIA() {
    if (!modal) return;
    
    backdrop.classList.add('opacity-0');
    panel.classList.remove('opacity-100', 'translate-y-0', 'sm:scale-100');
    panel.classList.add('opacity-0', 'translate-y-4', 'sm:scale-95');
    
    setTimeout(() => {
        modal.classList.add('hidden');
    }, 300);
}

// --- FUNÇÃO DE CHAMADA ---
async function solicitarAnaliseIA(alunoId) {
    const btn = document.getElementById(`btn-ia-${alunoId}`);
    if (!btn) return;

    const originalContent = btn.innerHTML;
    btn.disabled = true;
    btn.classList.add('opacity-75', 'cursor-wait');
    btn.innerHTML = '<i class="fas fa-circle-notch fa-spin"></i>';

    try {
        const response = await fetch(`/pedagogico/api/analisar-aluno/${alunoId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json'
            }
        });

        const data = await response.json();

        if (data.status === 'success') {
            abrirModalIA(data.data);
        } else {
            alert(`Erro na análise: ${data.message}`);
        }

    } catch (error) {
        console.error(error);
        alert('Erro de comunicação com o servidor.');
    } finally {
        btn.disabled = false;
        btn.classList.remove('opacity-75', 'cursor-wait');
        btn.innerHTML = originalContent;
    }
}