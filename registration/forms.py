from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserCreationFormWithEmail(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Requerido. 254 caracteres como máximo y debe ser un emai válido.")

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(u'El email ya está registrado, pruebe con otro.')
        return email
    
CLIENT_TYPE = (('Comprador ocasional','Comprador ocasional'),
               ('Comprador de materias primas','Comprador de materias primas'),
               ('Comprador al mayor','Comprador al mayor'),)

    
class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        # override default attributes
        self.fields['link'].widget.attrs['size'] = '100'

    class Meta:
        model = Profile
        fields = ['avatar', 'bio', 'link', 'client_type', 'reeup', 'nit', 'address', 'agency', 'contract']
        widgets = {
            'avatar': forms.ClearableFileInput(attrs={'class':'btn-primary btn-block form-control-file mt-3', 'placeholder':'Subir foto'}),
            'bio': forms.Textarea(attrs={'class':'form-control mt-3', 'rows':3, 'placeholder':'Biografía'}),
            'link': forms.URLInput(attrs={'class': 'form-control mt-3', 'placeholder':'enlace'}),
            'reeup': forms.TextInput(attrs={'class':'form-control mt-3', 'placeholder':'Código reeup'}),
            'nit': forms.TextInput(attrs={'class':'form-control mt-3', 'placeholder':'Código nit'}),
            'address': forms.TextInput(attrs={'class':'form-control mt-3', 'placeholder':'Dirección legal'}),
            'agency': forms.TextInput(attrs={'class':'form-control mt-3', 'placeholder':'Agencia bancaria'}),
            'contract': forms.TextInput(attrs={'class':'form-control mt-3', 'placeholder':'Número de contrato'}),
        }

class EmailForm(forms.ModelForm):
    email = forms.EmailField(required=True, max_length=254, help_text="Requerido. 254 caracteres máximo y debe ser un email válido.")

    class Meta:
        model = User
        fields = ['email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if 'email' in self.changed_data:
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError("El email ya está registrado, prueba con otro.")
        return email
                             


