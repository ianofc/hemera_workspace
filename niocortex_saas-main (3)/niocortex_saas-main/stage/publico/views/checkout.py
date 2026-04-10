import mercadopago
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from ledger.financeiro.models import Transacao

# ==============================================================================
# 2. CHECKOUT E PAGAMENTOS (MERCADO PAGO)
# ==============================================================================

def checkout(request):
    """ Resumo do pedido antes do pagamento """
    plano = request.GET.get('plano', 'Córtex Essential')
    ciclo = request.GET.get('ciclo', 'Mensal')
    preco = request.GET.get('price', '199,00')

    context = {
        'plan_name': plano,
        'cycle': ciclo,
        'price': preco
    }
    return render(request, 'public/checkout.html', context)

def processar_pagamento(request):
    """ Cria a transação no Financeiro e envia para o Mercado Pago """
    if request.method == 'POST':
        nome = request.POST.get('name')
        email = request.POST.get('email')
        doc = request.POST.get('document')
        phone = request.POST.get('phone')
        
        plano_nome = request.POST.get('plan_name')
        ciclo = request.POST.get('cycle')
        preco_str = request.POST.get('price', '0').replace('.', '').replace(',', '.')
        try:
            preco = float(preco_str)
        except ValueError:
            preco = 0.0

        host = getattr(settings, 'NGROK_URL', request.build_absolute_uri('/')[:-1])

        # Cria registro no módulo financeiro (Ledger)
        transacao = Transacao.objects.create(
            nome_cliente=nome,
            email_cliente=email,
            cpf_cnpj=doc,
            telefone=phone,
            plano=plano_nome,
            ciclo=ciclo,
            valor=preco
        )

        try:
            sdk = mercadopago.SDK(settings.MERCADO_PAGO_ACCESS_TOKEN)
            
            # Webhook aponta para o financeiro
            webhook_path = '/financial/webhook/mercadopago/' 
            notification_url = f"{host}{webhook_path}"

            preference_data = {
                "items": [{"title": f"NioCortex - {plano_nome}", "quantity": 1, "unit_price": preco, "currency_id": "BRL"}],
                "payer": {"name": nome, "email": email},
                "back_urls": {
                    "success": f"{host}/sucesso/",
                    "failure": f"{host}/checkout/",
                    "pending": f"{host}/checkout/"
                },
                "notification_url": notification_url,
                "auto_return": "approved",
                "external_reference": str(transacao.id)
            }

            preference_response = sdk.preference().create(preference_data)
            preference = preference_response["response"]

            transacao.mercado_pago_id = preference['id']
            transacao.save()

            return redirect(preference['init_point']) 

        except Exception as e:
            print(f"ERRO MP: {e}")
            messages.error(request, "Erro ao conectar com pagamento.")
            return redirect('stage_publico:checkout')

    return redirect('stage_publico:pricing')

def checkout_sucesso(request):
    return render(request, 'public/sucesso.html')