from django.shortcuts import render
from perfil.models import Categoria

def definir_contas(request):
    if request.method == "GET":
        categorias = Categoria.objects.all()
        context = {
            'categorias': categorias
        }
        return render(request, 'definir_contas.html', context)
