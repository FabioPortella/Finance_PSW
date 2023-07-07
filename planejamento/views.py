from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
# from django.contrib import messages
# from django.contrib.messages import constants

import json
from perfil.models import Categoria



def definir_planejamento(request):
    categorias = Categoria.objects.all()
    context = {
        'categorias': categorias,
    }
    return render(request, 'definir_planejamento.html', context)

@csrf_exempt
def update_valor_categoria(request, id):
    novo_valor = json.load(request)['novo_valor']
    categoria = Categoria.objects.get(id=id)
    categoria.valor_planejamento = novo_valor
    categoria.save()
    # TODO: message: salvo com sucesso.
    # messages.add_message(request, constants.SUCCESS, f"Valor da categoria {categoria.categoria} foi alterado com sucesso")
    # return redirect('/planejamento/definir_planejamento/')

    return JsonResponse({'status': 'Sucesso'})


def ver_planejamento(request):
    categorias = Categoria.objects.all()
    # TODO: Realizar barra com total
    context = {
        'categorias': categorias
        }
    return render(request, 'ver_planejamento.html', context)
