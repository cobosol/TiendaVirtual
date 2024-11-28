from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserCreationFormWithEmail(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Requerido. 254 caracteres como máximo y debe ser un correo válido.")
    
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super(UserCreationFormWithEmail, self).__init__(*args, **kwargs)   
        self.fields['username'].help_text = 'Requerido. Solo letras, dígitos y @/./+/-/_ '
        self.fields['first_name'].help_text = 'Requerido.'
        self.fields['last_name'].help_text = 'Requerido.'
        self.fields['password1'].help_text = 'No puede ser similar a tu otra información. Debe contener al menos 8 caracteres e incluir letras, números y caracteres especiales.'
        self.fields['password2'].help_text = 'Verifique que coincide exatamente con la contraseña anterior'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(u'El correo ya está registrado, pruebe con otro.')
        return email
    
class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        # override default attributes
        self.fields['link'].widget.attrs['size'] = '100'

    class Meta:
        model = Profile
        fields = ['avatar', 'bio', 'link', 'cid', 'client_type', 'money_type', 'phone', 'ws', 'reeup', 'nit', 'address', 'agency', 'contract']
        widgets = {
            'avatar': forms.ClearableFileInput(attrs={'class':'btn-primary btn-block form-control-file mt-3', 'placeholder':'Subir foto'}),
            'bio': forms.Textarea(attrs={'class':'form-control mt-3', 'rows':3, 'placeholder':'Biografía'}),
            'link': forms.URLInput(attrs={'class': 'form-control mt-3', 'placeholder':'enlace'}),
            """ 'cid': forms.TextInput(attrs={'class':'form-control mt-3', 'placeholder':'Número de identidad', 'required': True}), """
            """ 'reeup': forms.TextInput(attrs={'class':'form-control mt-3', 'placeholder':'Código reeup'}),
            'nit': forms.TextInput(attrs={'class':'form-control mt-3', 'placeholder':'Código nit'}), """ 
            """ 'address': forms.TextInput(attrs={'class':'form-control mt-3', 'placeholder':'Dirección legal'}),
            'agency': forms.TextInput(attrs={'class':'form-control mt-3', 'placeholder':'Agencia bancaria'}), """ 
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
                             
class UpdateProfileAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UpdateProfileAdminForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Profile
        fields = ['money_type', 'prefered_store']
