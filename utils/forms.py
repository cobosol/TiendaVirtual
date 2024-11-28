from django import forms
from utils.models import Price
from django.db import models
from django_ckeditor_5.widgets import CKEditor5Widget

class PriceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
          super().__init__(*args, **kwargs)
          #self.fields["description"].required = False

    class Meta:
        model = Price
        fields = '__all__'
        """         widgets = {
            "description": CKEditor5Widget(
                  attrs={"class": "django_ckeditor_5"}, config_name="comment"
              )
          } """