from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.messages import constants
from perfil.models import Categoria
from .models import ContaPagar

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
        messages.add_message(request, constants.SUCCESS, "Conta cadastrada com sucesso")

        return redirect('/contas/definir_contas')


def ver_contas(request):
    return render(request, 'ver_contas.html')