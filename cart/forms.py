from django import forms
from stores.models import Store
import datetime
import re
from django.shortcuts import render, redirect, get_object_or_404
from registration.models import Profile
from cart.models import DeliveryInfo

class DeliveryForm(forms.ModelForm):
    def __init__(self, request=None, *args, **kwargs):
        super(DeliveryForm, self).__init__(*args, **kwargs)
        # override default attributes

    class Meta:
        model = DeliveryInfo
        fields = ['storeDelivery', 'deliveryZone']

""" class DeliveryForm(forms.Form): 
    
    # each individual substate
    GUANABACOA = 0
    HABANADELESTE = 1
    CERRO = 2
    COTORRO = 3
    DIEZDEOCTUBRE = 4
    HABANAVIEJA = 5
    CENTROHABANA = 6
    SANMIGUEL = 7
    BOYEROS = 8
    MARIANAO = 9
    LALISA = 10
    PLAZA = 11
    PLAYA = 12
    REGLA = 13
    ARROYO = 14

    # set of possible order statuses
    SUBSTATE = ((GUANABACOA,'Guanabacoa'),
                      (HABANADELESTE,'La Habana del Este'),
                      (CERRO,'Cerro'),
                      (COTORRO,'Cotorro'),
                      (DIEZDEOCTUBRE,'Diez de Octubre'),
                      (HABANAVIEJA,'La Habana Vieja'),
                      (CENTROHABANA, 'Centro Habana'),
                      (SANMIGUEL, 'San Miguel del Padrón'),
                      (BOYEROS,'Boyeros'),
                      (MARIANAO,'Marianao'),
                      (LALISA,'La Lisa'),
                      (PLAZA,'Plaza de la Revolución'),
                      (PLAYA, 'Playa'),
                      (REGLA, 'Regla'),
                      (ARROYO, 'Arroyo Naranjo'),
                      )
       
    #prefered_store = 3
    delivery_type = forms.ModelChoiceField(queryset=Store.objects.all())
    delivery_substate = forms.ModelChoiceField(empty_label='Zona de envío', limit_choices_to=SUBSTATE)

    def __init__(self, request=None, *args, **kwargs):
        super(DeliveryForm, self).__init__(*args, **kwargs)



    # custom validation to check for cookies
    def clean(self):
        if self.request:
            if not self.request.session.test_cookie_worked():
                raise forms.ValidationError("Debe habilitar las cookies.")
        return self.cleaned_data  """
