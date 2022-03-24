from ast import arg
from email import message
from re import template
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic
from orders.views import order
import shipping_address
from shipping_address.models import ShippingAddress
from shipping_address.forms import ShippingAddressForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import reverse
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from carts.utils import get_or_create_cart
from orders.utils import get_or_create_order

@login_required(login_url='login')
def create(request):
    form = ShippingAddressForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        shipping_address = form.save(commit=False)
        shipping_address.user = request.user
        shipping_address.default = not request.user.has_shipping_address()
        shipping_address.save()
        
        if request.GET.get('next'):
            if request.GET['next'] == reverse('orders:address'):
                cart = get_or_create_cart(request)
                order = get_or_create_order(cart,request)

                order.update_shipping_address(shipping_address)
                return HttpResponseRedirect(request.GET['next'])

        messages.success(request, 'Direccion creada con exito')
        return redirect('shipping_address:shipping_addresses')
    return render(request, 'create.html', {'form':form})

@login_required(login_url='login')
def default(request, pk):
    shipping_address = get_object_or_404(ShippingAddress, pk=pk)
    if request.user.id != shipping_address.user_id:
        return redirect('carts:cart')
    if request.user.has_shipping_address():   
        request.user.shipping_address.update_default()
    shipping_address.update_default(True)
    return redirect('shipping_address:shipping_addresses')
    
class ShippingAddressListView(LoginRequiredMixin, generic.ListView):
    login_url = 'login'
    model = ShippingAddress
    template_name = 'shipping_addresses.html'

    def get_queryset(self):
        return ShippingAddress.objects.filter(user=self.request.user).order_by('-default')

class ShippingAddressUpdateViews(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    login_url = 'login'
    model = ShippingAddress
    form_class = ShippingAddressForm
    template_name = 'update.html'
    success_message = 'Direccion Actualizada'

    def get_success_url(self):
        return reverse('shipping_address:shipping_addresses')

    def dispatch(self, request, *args, **kwargs):
        if request.user.id != self.get_object().user_id:
            return redirect('carts:cart')
        return super(ShippingAddressUpdateViews, self).dispatch(request, *args, **kwargs)

class ShippingAddressDeleteViews(LoginRequiredMixin, generic.DeleteView):
    login_url = 'login'
    model = ShippingAddress
    template_name = 'delete.html'
    success_url = reverse_lazy('shipping_address:shipping_addresses')
    success_message = 'Direccion Eliminada'

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().default:
            return redirect('shipping_address:shipping_addresses')
        if request.user.id != self.get_object().user_id:
            return redirect('carts:cart')
        if self.get_object().has_orders():
            return redirect('shipping_address:shipping_addresses')
        return super(ShippingAddressDeleteViews, self).dispatch(request, *args, **kwargs)