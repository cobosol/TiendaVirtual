from django import forms
from stores.models import Store
import datetime
import re
from django.shortcuts import render, redirect, get_object_or_404
from registration.models import Profile

class DeliveryForm(forms.Form):    
    #prefered_store = 3
    delivery_type = forms.ModelChoiceField(queryset=Store.objects.all())

    def __init__(self, request=None, *args, **kwargs):
        super(DeliveryForm, self).__init__(*args, **kwargs)
        """ self.request = request
        user = request.user
        print("Entró al init")
        if (user.is_authenticated):
            profile = get_object_or_404(Profile, user = user)
            store = profile.prefered_store    
            if store:
                print(store.name)
                print(store.pk)
                self.fields['prefered_store'] = store.pk
                self.fields['delivery_type'] = store
            else:
                print("No hay store") """



    # custom validation to check for cookies
    def clean(self):
        if self.request:
            if not self.request.session.test_cookie_worked():
                raise forms.ValidationError("Debe habilitar las cookies.")
        return self.cleaned_data
