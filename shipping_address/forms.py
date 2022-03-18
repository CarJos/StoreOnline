from django.forms import ModelForm
# from django.contrib.auth.models import User
from shipping_address.models import ShippingAddress

class ShippingAddressForm(ModelForm):
    class Meta:
        model = ShippingAddress

        fields = [
            'line1', 'line2', 'city', 'state', 'country', 'postal_code', 'reference'
        ]

        labels = {
            'line1':'Calle 1',
            'line2':'Calle 2',
            'city':'Ciudad',
            'state':'Estado',
            'country':'Pais',
            'postal_code':'Codigo Postal',
            'reference':'Referencias',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.fields['postal_code'].widget.attrs.update({'placeholder':'0000'})
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class':'form-control'})