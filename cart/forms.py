from django import forms
from stores.models import Store
import datetime
import re

class DeliveryForm(forms.Form):    
    delivery_type = forms.ModelChoiceField(queryset=Store.objects.all(), initial=3)


    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super(DeliveryForm, self).__init__(*args, **kwargs)


    # custom validation to check for cookies
    def clean(self):
        if self.request:
            if not self.request.session.test_cookie_worked():
                raise forms.ValidationError("Debe habilitar las cookies.")
        return self.cleaned_data
