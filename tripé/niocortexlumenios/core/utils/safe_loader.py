
from django.urls import include, path
from django.shortcuts import render
import logging

logger = logging.getLogger(__name__)

def maintenance_view(request, module_name="Sistema", error_msg=""):
    return render(request, 'core/system/maintenance.html', {
        'module_name': module_name,
        'error_message': str(error_msg)
    })

def safe_include(route, module_path, namespace=None):
    try:
        # Tenta carregar o módulo normalmente
        if namespace:
            return path(route, include((module_path, namespace), namespace=namespace))
        return path(route, include(module_path))
    except Exception as e:
        # Se falhar (ImportError, AttributeError, etc), registra o erro e retorna a view de manutenção
        logger.error(f"FALHA AO CARREGAR MÓDULO {module_path}: {e}")
        # Criamos uma view wrapper para capturar o erro no momento da requisição
        def error_wrapper(request, *args, **kwargs):
            return maintenance_view(request, module_name=module_path.split('.')[0].upper(), error_msg=e)
        
        # Retorna uma rota "catch-all" para esse módulo quebrado
        return path(f'{route}', error_wrapper)
