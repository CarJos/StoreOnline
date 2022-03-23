from django.shortcuts import render
from carts.utils import get_or_create_cart
from orders.models import Order
from orders.utils import get_or_create_order
from django.contrib.auth.decorators import login_required
from orders.utils import breadcrumb
import shipping_address

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

    shipping_address = order.shipping_address
    return render(request, 'address.html', context={
        'cart':cart,
        'order':order,
        'breadcrumb':breadcrumb(address=True),
    })