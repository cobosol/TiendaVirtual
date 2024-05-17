from django import forms
from stores.models import Store
import datetime
import re

DELIVERY_TYPES = {}

class DeliveryForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(DeliveryForm, self).__init__(*args, **kwargs)
        # override default attributes
        for field in self.fields:
            self.fields[field].widget.attrs['size'] = '30'
        self.fields['credit_card_type'].widget.attrs['size'] = '1'
        
        # Llenar la lista de formas de envío]
        stores = Store.objects.all()
        for s in stores:
            delivery_slug = s.slug
            DELIVERY_TYPES[delivery_slug] = delivery_slug

    delivery_type = forms.CharField(widget=forms.Select(choices=DELIVERY_TYPES))

