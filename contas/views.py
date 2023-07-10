from django.shortcuts import render, redirect

import sweetify

from datetime import datetime
from perfil.models import Categoria
from .models import ContaPagar, ContaPaga


def definir_contas(request):
    if request.method == "GET":
        categorias = Categoria.objects.all()
        context = {
            'categorias': categorias
        }
        return render(request, 'definir_contas.html', context)
    else:
        titulo = request.POST.get('titulo')
        categoria = request.POST.get('categoria')
        descricao = request.POST.get('descricao')
        valor = request.POST.get('valor')
        dia_pagamento = request.POST.get('dia_pagamento')

        conta = ContaPagar(
            titulo = titulo,
            categoria_id = categoria,
            descricao = descricao,
            valor = valor,
            dia_pagamento = dia_pagamento,
        )
        conta.save()
        sweetify.success(request, 'Saída cadastrada com sucesso')

        return redirect('/contas/definir_contas')


def ver_contas(request):
    MES_ATUAL = datetime.now().month
    DIA_ATUAL = datetime.now().day

    contas = ContaPagar.objects.all().order_by('dia_pagamento')
    contas_pagas = ContaPaga.objects.filter(
        data_pagamento__month=MES_ATUAL).values(
        'conta')
    contas_vencidas = contas.filter(
        dia_pagamento__lt=DIA_ATUAL).exclude(        # menor que o dia atual
        id__in=contas_pagas)
    contas_proximas_vencimento = contas.filter(
        dia_pagamento__lte = DIA_ATUAL + 5).filter(  # menor ou igual que o dia atual
        dia_pagamento__gt = DIA_ATUAL).exclude(      # maior que dia atual
        id__in=contas_pagas)                         # excluir contas pagas
    contas_restantes = contas.exclude(
        id__in = contas_vencidas).exclude(
        id__in = contas_proximas_vencimento).exclude(
        id__in = contas_pagas)
    
    context = {
        'contas_vencidas': contas_vencidas,
        'contas_proximas_vencimento': contas_proximas_vencimento,
        'contas_restantes': contas_restantes,
    }

    return render(request, 'ver_contas.html', context)