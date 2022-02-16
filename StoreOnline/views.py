from multiprocessing import context
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.http import HttpResponse
from django.shortcuts import redirect, render
from StoreOnline.forms import RegisterForm

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

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'Bienvenido {}'.format(user.username))
            return redirect('index')
        else:
            messages.error(request, 'Usuario o contraseñas no validos')
    return render(request, 'users/login.html', {})

def logout_view(request):
    logout(request)
    messages.success(request, 'Sesion cerrada corectamente')
    return redirect('login')

def register(request):
    form = RegisterForm
    context = {
        'form' : form,
    }
    return render(request, 'users/register.html', context)