def module_context(request):
    """
    Identifica o módulo atual baseado na URL para adaptar a interface.
    """
    path = request.path
    context = {
        'in_social': path.startswith('/social/'),
        'in_lumenios': any(x in path for x in ['/pedagogico/', '/plataforma/']),
        'in_hub': path.startswith('/hub/'),
        'in_ledger': path.startswith('/financeiro/'),
        'current_module_name': 'MultiVerso'
    }
    
    if context['in_social']: context['current_module_name'] = 'YourLife'
    elif context['in_lumenios']: context['current_module_name'] = 'Lumenios'
    elif context['in_hub']: context['current_module_name'] = 'Hub'
    elif context['in_ledger']: context['current_module_name'] = 'Ledger'
    
    return context