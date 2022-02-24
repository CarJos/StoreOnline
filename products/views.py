import imp
from re import template
from django.shortcuts import render
from django.views import generic

from products.models import Product

class ProductListView(generic.ListView):
    template_name = 'index.html'
    queryset = Product.objects.all().order_by('title')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'Listado de productos'
        context['products'] = context['object_list']
        return context

class ProductDetailView(generic.DetailView):
    model = Product
    template_name = 'product.html'