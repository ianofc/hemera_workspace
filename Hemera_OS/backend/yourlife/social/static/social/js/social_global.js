// social_global.js

(function() {
    // =================================================================
    // 1. CONFIGURAÇÃO INICIAL E UTILITÁRIOS
    // =================================================================
    
    // Pega o CSRF token do cookie para usar em requisições AJAX/HTMX
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    const csrftoken = getCookie('csrftoken');

    // Configura o HTMX para incluir o CSRF token em todas as requisições POST
    document.body.addEventListener('htmx:configRequest', (event) => {
        event.detail.headers['X-CSRFToken'] = csrftoken;
    });

    // =================================================================
    // 2. MODAL DE CRIAÇÃO DE POST (Lógica de Preview)
    // =================================================================
    const createPostModal = document.getElementById('createPostModal');
    const mediaPreviewContainer = document.getElementById('mediaPreview');
    const fileInputImage = document.getElementById('fileInputImage');
    const fileInputVideo = document.getElementById('fileInputVideo');

    if (createPostModal && mediaPreviewContainer && fileInputImage && fileInputVideo) {
        
        // Função auxiliar para limpar preview
        const clearPreview = () => {
            mediaPreviewContainer.innerHTML = '';
            mediaPreviewContainer.classList.add('hidden');
            fileInputImage.value = '';
            fileInputVideo.value = '';
        };

        // Lida com seleção de imagem
        fileInputImage.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    mediaPreviewContainer.innerHTML = `
                        <div class="relative">
                            <img src="${e.target.result}" class="w-full h-64 object-cover rounded-xl">
                            <button type="button" onclick="clearPostMedia()" class="absolute top-2 right-2 bg-gray-900/60 hover:bg-gray-900 text-white p-2 rounded-full transition">
                                <i class="fas fa-times"></i>
                            </button>
                        </div>
                    `;
                    mediaPreviewContainer.classList.remove('hidden');
                    fileInputVideo.value = ''; // Limpa input de vídeo se houver
                }
                reader.readAsDataURL(file);
            }
        });

        // Lida com seleção de vídeo
        fileInputVideo.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const url = URL.createObjectURL(file);
                mediaPreviewContainer.innerHTML = `
                    <div class="relative w-full bg-black rounded-xl overflow-hidden">
                        <video src="${url}" controls class="w-full h-64"></video>
                        <button type="button" onclick="clearPostMedia()" class="absolute top-2 right-2 bg-gray-900/60 hover:bg-gray-900 text-white p-2 rounded-full transition z-10">
                            <i class="fas fa-times"></i>
                        </button>
                    </div>
                `;
                mediaPreviewContainer.classList.remove('hidden');
                fileInputImage.value = ''; // Limpa input de imagem se houver
            }
        });

        // Expor função de limpar globalmente para o botão 'X' funcionar
        window.clearPostMedia = clearPreview;

        // Limpa tudo quando o modal fecha
        createPostModal.addEventListener('close', clearPreview);
    }

    // =================================================================
    // 3. BOTÕES DE AÇÃO GENÉRICOS (Feedback Visual)
    // =================================================================
    
    // Botão Compartilhar (Aviãozinho)
    document.addEventListener('click', function(e) {
        const shareBtn = e.target.closest('.share-btn');
        if (shareBtn) {
            // Aqui você implementaria a lógica real (ex: abrir modal de compartilhar, copiar link)
            // Por enquanto, vamos dar um feedback visual
            const icon = shareBtn.querySelector('i');
            const originalClass = icon.className;
            
            icon.className = 'fas fa-check text-green-500 scale-125 transition-transform';
            
            setTimeout(() => {
               icon.className = originalClass;
            }, 2000);

            // Opcional: Mostrar um toast/notificação
            // showToast('Link copiado para a área de transferência!');
        }
    });

    // Botão Salvar (Bookmark)
    document.addEventListener('click', function(e) {
        const saveBtn = e.target.closest('.save-btn');
        if (saveBtn) {
            const icon = saveBtn.querySelector('i');
            if (icon.classList.contains('far')) {
                // Salvar
                icon.classList.remove('far');
                icon.classList.add('fas', 'text-yellow-500', 'scale-125');
                // htmx.ajax('POST', saveUrl, {target: ...}) // Lógica real futura
            } else {
                // Remover
                icon.classList.remove('fas', 'text-yellow-500', 'scale-125');
                icon.classList.add('far');
            }
        }
    });

})();