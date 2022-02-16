from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    context = {
        'title' : 'Productos',
        'message' : 'Listado de productos',
        'products' : [
            {'title' : 'Playera', 'price' : 20000, 'stock' : True},
            {'title' : 'Camisa', 'price' : 40000, 'stock' : True},
            {'title' : 'Mochila', 'price' : 30000, 'stock' : False},
        ],
    }
    return render(request, 'index.html', context)