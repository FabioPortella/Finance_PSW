from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.messages import constants
from django.http import HttpResponse
from perfil.models import Categoria, Conta
from .models import Valores



def novo_valor(request):
    if request.method == 'GET':
        contas = Conta.objects.all()
        categorias = Categoria.objects.all()
        context = {
            'contas': contas,
            'categorias': categorias,
        }
        return render(request, 'novo_valor.html', context)
    
    elif request.method == 'POST':
        valor = request.POST.get('valor')
        categoria = request.POST.get('categoria')
        descricao = request.POST.get('descricao')
        data = request.POST.get('data')
        conta = request.POST.get('conta')
        tipo = request.POST.get('tipo')

        valores = Valores(
            valor = valor,
            categoria_id = categoria,
            descricao = descricao,
            data = data,
            conta_id = conta,
            tipo = tipo,
        )

        valores.save()

        #TODO: Mensagem prodessada de acordo com o tipo
        messages.add_message(request, constants.SUCCESS, "Entrada / Saida cadastrada com sucesso")

        return redirect('/extrato/novo_valor')
