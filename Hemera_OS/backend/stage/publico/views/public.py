from django.shortcuts import render, redirect

# ==============================================================================
# 1. PÁGINAS INSTITUCIONAIS (MARKETING)
# ==============================================================================

def index(request):
    """ Landing Page Principal """
    if request.user.is_authenticated:
        return redirect('core:dashboard')
    return render(request, 'public/landing_page.html')

def about(request):
    return render(request, 'public/about.html')

def pricing(request):
    """ Página de Preços (Vitrine) """
    return render(request, 'public/pricing.html')

def contact(request):
    return render(request, 'public/contact.html')

def demo(request):
    return render(request, 'public/demo.html')

# --- Features (Páginas de Venda de Funcionalidades) ---

def feature_financial(request):
    return render(request, 'public/financial_management.html')

def feature_diary(request):
    return render(request, 'public/digital_diary.html')

# --- Legal / Suporte ---

def system_status(request):
    return render(request, 'public/system_status.html')

def help_center(request):
    return render(request, 'public/help_center.html')

def privacy_policy(request):
    return render(request, 'public/privacy_policy.html')

def terms_of_use(request):
    return render(request, 'public/terms_of_use.html')