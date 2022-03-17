from multiprocessing import context
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from StoreOnline.forms import RegisterForm
# from django.contrib.auth.models import User
from products.models import Product
from users.models import User

def index(request):
    products = Product.objects.all().order_by('title')
    context = {
        'title' : 'Productos',
        'message' : 'Listado de productos',
        'products' : products,
    }

    return render(request, 'index.html', context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect('products/index')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'Bienvenido {}'.format(user.username))
            if request.GET.get('next'):
                return HttpResponseRedirect(request.GET['next'])
            return redirect('products:index')
        else:
            messages.error(request, 'Usuario o contraseñas no validos')
    return render(request, 'users/login.html', {})

def logout_view(request):
    logout(request)
    messages.success(request, 'Sesion cerrada corectamente')
    return redirect('login')

def register(request):
    if request.user.is_authenticated:
        return redirect('products/index')
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        if user:
            login(request, user)
            messages.success(request, 'Usuario creado de forma exitosa')
            return redirect('products:index')
    context = {
        'form' : form,
    }
    return render(request, 'users/register.html', context)