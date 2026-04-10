from django.urls import path
from .views import public, checkout # Importando dos novos módulos

app_name = 'stage_publico'

urlpatterns = [
    # --- PÁGINAS PÚBLICAS (public.py) ---
    path('', public.index, name='index'),
    path('sobre/', public.about, name='about'),
    path('precos/', public.pricing, name='pricing'),
    path('contato/', public.contact, name='contact'),
    path('demo/', public.demo, name='demo'),
    
    # Features & Legal
    path('funcionalidades/financeiro/', public.feature_financial, name='feature_financial'),
    path('funcionalidades/diario/', public.feature_diary, name='feature_diary'),
    path('status/', public.system_status, name='system_status'),
    path('ajuda/', public.help_center, name='help_center'),
    path('privacidade/', public.privacy_policy, name='privacy_policy'),
    path('termos/', public.terms_of_use, name='terms_of_use'),
    
    # --- CHECKOUT E VENDAS (checkout.py) ---
    path('checkout/', checkout.checkout, name='checkout'),
    path('checkout/processar/', checkout.processar_pagamento, name='processar_pagamento'),
    path('sucesso/', checkout.checkout_sucesso, name='checkout_sucesso'),
]