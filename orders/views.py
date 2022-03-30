from ast import arg
from urllib import request
from django import conf
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import EmptyQuerySet
from django.views import generic

from carts.utils import get_or_create_cart
from orders.models import Order
from orders.utils import get_or_create_order
from orders.utils import breadcrumb
from shipping_address.models import ShippingAddress
from carts.utils import destroy_cart
from orders.utils import destroy_order
from orders.mails import Mail
from orders.decorator import validate_car_and_order

import shipping_address
import re
import threading

@login_required(login_url='login')
@validate_car_and_order
def order(request,cart,order):
    return render(request, 'order.html', {
        'cart': cart,
        'order': order,
        'breadcrumb': breadcrumb,
        })
@login_required(login_url='login')
@validate_car_and_order
def address(request,cart,order):
    shipping_address = order.get_or_set_shipping_address()
    can_choose_address = request.user.has_shipping_addresses()
    return render(request, 'address.html', context={
        'cart':cart,
        'order':order,
        'shipping_address':shipping_address,
        'can_choose_address':can_choose_address,
        'breadcrumb':breadcrumb(address=True),
    })
@login_required(login_url='login')
def select_address(request):
    shipping_addresses = request.user.addresses
    return render(request, 'select_address.html', {
        'breadcrumb':breadcrumb(address=True),
        'shipping_addresses':shipping_addresses,
    })

@login_required(login_url='login')
@validate_car_and_order
def check_address(request,cart,order,pk):
    shipping_address =get_object_or_404(ShippingAddress, pk=pk)

    if request.user.id != shipping_address.user.id:
        return redirect('carts:cart')

    order.update_shipping_address(shipping_address)
    return redirect('orders:address')

@login_required(login_url='login')
@validate_car_and_order
def confirm(request,cart,order):
    shipping_address = order.shipping_address
    if shipping_address is None:
        return redirect('orders:address')
    return render(request, 'confirm.html', {
    'cart':cart,
    'order':order,
    'shipping_address':shipping_address,
    'breadcrumb':breadcrumb(address=True, confirmation=True),
    })

@login_required(login_url='login')
@validate_car_and_order
def cancel(request,cart,order):
    if request.user.id != order.user_id:
        return redirect('carts:cart')
    order.cancel()
    destroy_order(request)
    destroy_cart(request)
    
    messages.error(request, 'Orden Cancelada')
    return redirect('products:index')

@login_required(login_url='login')
@validate_car_and_order
def complete(request,cart,order):
    if request.user.id != order.user_id:
        return redirect('carts:cart')
    order.complete()
    
    thread = threading.Thread(target=Mail.send_complete_order, args=(
        order, request.user
    ))
    thread.start()

    destroy_order(request)
    destroy_cart(request)

    messages.success(request, 'Compra Exitosa')
    return redirect('products:index')

class OrderListView(LoginRequiredMixin, generic.ListView):
    login_url = 'login'
    template_name = 'orders.html'

    def get_queryset(self):
        return self.request.user.orders_completed()