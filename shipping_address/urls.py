from django.urls import path

from shipping_address import views

app_name = 'shipping_address'

urlpatterns = [
    path('', views.ShippingAddressListView.as_view(), name='shipping_addresses'),
    path('nueva', views.create, name='create'),
    path('editar/<int:pk>', views.ShippingAddressUpdateViews.as_view(), name='update'),
    path('eliminar/<int:pk>', views.ShippingAddressDeleteViews.as_view(), name='delete'),
    path('default/<int:pk>', views.default, name='default'),
]