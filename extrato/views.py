# importações django
from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse
from django.template.loader import render_to_string
from django.conf import settings

# importações Python
from io import BytesIO
from datetime import datetime, timedelta
import os

# importações de bibliotecas externas
import sweetify
from weasyprint import HTML

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

        conta = Conta.objects.get(id=conta)
        if tipo == 'E':
            conta.valor += int(valor)
        else:
            conta.valor -= int(valor)
        conta.save()

        if tipo == 'E': 
            sweetify.success(request, 'Entrada cadastrada com sucesso')
        else: 
            sweetify.success(request, 'Saída cadastrada com sucesso')

        return redirect('/extrato/novo_valor')


def view_extrato(request):
    contas = Conta.objects.all()
    conta_get = request.GET.get('conta')
    categoria_get = request.GET.get('categoria')
    periodo_get = request.GET.get('periodo')
    categorias = Categoria.objects.all()
    
    data_atual = datetime.now().date()
    data_anterior = data_atual - timedelta(days=7)

    if periodo_get:
        valores = Valores.objects.filter(data__range=(data_anterior, data_atual))
    else:
        valores = Valores.objects.filter(data__month = datetime.now().month)

    if conta_get:
        valores = valores.filter(conta__id = conta_get)

    if categoria_get:
        valores = valores.filter(categoria__id = categoria_get)         

    context = {
        "contas": contas,
        "categorias": categorias,
        "valores": valores,
    }

    return render(request, 'view_extrato.html', context)


def exportar_pdf(request):
    valores = Valores.objects.filter(data__month = datetime.now().month)
    path_template = os.path.join(settings.BASE_DIR, 'templates/partials/extrato.html')
    context = {
        "valores": valores,
    }
    path_output = BytesIO()
    template_render = render_to_string(path_template, context)
   
    HTML(string=template_render).write_pdf(path_output)
    path_output.seek(0)
    return FileResponse(path_output, filename="extrato.pdf")