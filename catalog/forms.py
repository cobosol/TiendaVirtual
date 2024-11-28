from django import forms
from catalog.models import Product
from stores.models import Store, Product_Sales
from django.db import models
from django_ckeditor_5.widgets import CKEditor5Widget


class ProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
          super().__init__(*args, **kwargs)
          self.fields["description"].required = False

    class Meta:
        model = Product
        exclude = ('count','reserved', 'slug')

        widgets = {
            "description": CKEditor5Widget(
                  attrs={"class": "django_ckeditor_5"}, config_name="comment"
              )
          }
    
class ProductAlmacenForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
          super().__init__(*args, **kwargs)

    class Meta:
        model = Product_Sales
        fields = '__all__'
        
class ProductAdminForm(forms.ModelForm):    
    def __init__(self, *args, **kwargs):
          super().__init__(*args, **kwargs)
          self.fields["description"].required = False

    class Meta:
        model = Product
        fields = '__all__'

"""     def clean_price(self):
        if self.cleaned_data['price_base'] <= 0:
            raise forms.ValidationError('El precio debe ser mayor que cero')
        return self.cleaned_data['price_base'] """
    

class ProductAddToCartForm(forms.Form):    
    quantity = forms.IntegerField(widget=forms.TextInput(attrs={'size':'2', 'value':'1', 'class':'form-control bg-secondary text-center', 'maxlength':'3'}), error_messages={'invalid':'Por favor entre un valor entero mayor que cero.'}, min_value=1)
    product_slug = forms.CharField(widget=forms.HiddenInput())
    delivery_type = forms.ModelChoiceField(queryset=Store.objects.all(), initial=1)

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
    
class SelectStoreForm(forms.Form):    
    #prefered_store = 3
    selected_store = forms.ModelChoiceField(queryset=Store.objects.all())

    def __init__(self, request=None, *args, **kwargs):
        super(SelectStoreForm, self).__init__(*args, **kwargs)

