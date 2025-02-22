from django import forms
from promo.models import Banner, Offer
from django.db import models

class BannerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
          super().__init__(*args, **kwargs)

    class Meta:
        model = Banner
        fields = '__all__'

class OfferForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
          super().__init__(*args, **kwargs)

    class Meta:
        model = Offer
        fields = '__all__'