from django import forms
from catalog.models import Product
from stores.models import Store
from django.db import models


class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        # pass admin: Yosoy2024++ o CoboSol2024++

    def clean_price(self):
        if self.cleaned_data['price'] <= 0:
            raise forms.ValidationError('El precio debe ser mayor que cero')
        return self.cleaned_data['price']

""" CARD_TYPES = (('Mastercard','Mastercard'),
              ('VISA','VISA'),
              ('AMEX','AMEX'),
              ('Discover','Discover'),) """


class ProductAddToCartForm(forms.Form):
    """ def deliverys():
        DELIVERY_TYPES = {}
        stores = Store.objects.all()
        for s in stores:
            delivery_slug = s.slug
            DELIVERY_TYPES[delivery_slug] = delivery_slug
        return DELIVERY_TYPES """
    
    quantity = forms.IntegerField(widget=forms.TextInput(attrs={'size':'2', 'value':'1', 'class':'form-control bg-secondary text-center', 'maxlength':'3'}), error_messages={'invalid':'Por favor entre un valor entero mayor que cero.'}, min_value=1)
    product_slug = forms.CharField(widget=forms.HiddenInput())
    #delivery_type = forms.CharField(widget=forms.Select(choices=Store.objects.all()))
    delivery_type = forms.ModelChoiceField(queryset=Store.objects.all(), initial=1)
    #credit_card_type = forms.CharField(widget=forms.Select(choices=CARD_TYPES))


    # override the default __init__ so we can set the request
    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super(ProductAddToCartForm, self).__init__(*args, **kwargs)


    # custom validation to check for cookies
    def clean(self):
        if self.request:
            if not self.request.session.test_cookie_worked():
                raise forms.ValidationError("Debe habilitar las cookies.")
        return self.cleaned_data
    
