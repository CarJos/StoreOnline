import re
from django import conf
from django.shortcuts import redirect, render
from carts.utils import get_or_create_cart
from orders.models import Order
from orders.utils import get_or_create_order
from django.contrib.auth.decorators import login_required
from orders.utils import breadcrumb
import shipping_address
from django.shortcuts import get_object_or_404
from shipping_address.models import ShippingAddress
from django.contrib import messages
from carts.utils import destroy_cart
from orders.utils import destroy_order
from orders.mails import Mail

@login_required(login_url='login')
def order(request):
    cart = get_or_create_cart(request)
    order = get_or_create_order(cart, request)
    return render(request, 'order.html', {
        'cart': cart,
        'order': order,
        'breadcrumb': breadcrumb,
        })
@login_required(login_url='login')
def address(request):
    cart = get_or_create_cart(request)
    order = get_or_create_order(cart, request)

    shipping_address = order.get_or_set_shipping_address()
    can_choose_address = request.user.shippingaddress_set.count() > 1
    return render(request, 'address.html', context={
        'cart':cart,
        'order':order,
        'shipping_address':shipping_address,
        'can_choose_address':can_choose_address,
        'breadcrumb':breadcrumb(address=True),
    })
@login_required(login_url='login')
def select_address(request):
    shipping_addresses = request.user.shippingaddress_set.all()
    return render(request, 'select_address.html', {
        'breadcrumb':breadcrumb(address=True),
        'shipping_addresses':shipping_addresses,
    })

@login_required(login_url='login')
def check_address(request, pk):
    cart = get_or_create_cart(request)
    order = get_or_create_order(cart,request)
    shipping_address =get_object_or_404(ShippingAddress, pk=pk)

    if request.user.id != shipping_address.user.id:
        return redirect('carts:cart')

    order.update_shipping_address(shipping_address)
    return redirect('orders:address')

@login_required(login_url='login')
def confirm(request):
    cart = get_or_create_cart(request)
    order = get_or_create_order(cart,request)
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
def cancel(request):
    cart = get_or_create_cart(request)
    order = get_or_create_order(cart,request)
    if request.user.id != order.user_id:
        return redirect('carts:cart')
    order.cancel()
    destroy_order(request)
    destroy_cart(request)
    
    messages.error(request, 'Orden Cancelada')
    return redirect('products:index')

@login_required(login_url='login')
def complete(request):
    cart = get_or_create_cart(request)
    order = get_or_create_order(cart,request)

    if request.user.id != order.user_id:
        return redirect('carts:cart')
    order.complete()
    
    Mail.send_complete_order(order, request.user)

    destroy_order(request)
    destroy_cart(request)

    messages.success(request, 'Compra Exitosa')
    return redirect('products:index')