from django.shortcuts import render
from carts.models import Cart
# Create your views here.
def cart(request):
    request.session['cart_id'] = None
    user = request.user if request.user.is_authenticated else None
    cart_id = request.session.get('cart_id')
    if cart_id:
        cart = Cart.objects.get(pk=cart_id)
    else:
        cart = Cart.objects.create(user=user)
    request.session['cart_id'] = cart.cart_id
    return render(request, 'carts.html', {})