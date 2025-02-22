from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django import forms
from .forms import UserCreationFormWithEmail
from django.views.generic.edit import UpdateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import Profile
from stores.models import Store
from .forms import ProfileForm, UserCreationFormWithEmail, EmailForm, UpdateProfileAdminForm
#Librerías para mensajes, algunos basados en views
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin 

# Instanciamos las vistas genéricas de Django 
#from django.views import View
from django.views.generic import ListView, DetailView 
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse


class SignUpView(CreateView):
    form_class = UserCreationFormWithEmail
    template_name = 'registration/signup.html'

    def get_success_url(self):
        return reverse_lazy('login') + '?register'
    
    def get_form(self, form_class=None):
        form = super(SignUpView, self).get_form()
        form.fields['username'].widget = forms.TextInput(attrs={'class':'form-control mb-2', 'placeholder':'Nombre de usuario'})
        form.fields['first_name'].widget = forms.TextInput(attrs={'class':'form-control mb-2', 'placeholder':'Nombre'})
        form.fields['last_name'].widget = forms.TextInput(attrs={'class':'form-control mb-2', 'placeholder':'Apellidos'})
        form.fields['email'].widget = forms.EmailInput(attrs={'class':'form-control mb-2', 'placeholder':'Dirección de correo electrónico'})
        form.fields['password1'].widget = forms.PasswordInput(attrs={'class':'form-control mb-2', 'placeholder':'Contraseña'})
        form.fields['password2'].widget = forms.PasswordInput(attrs={'class':'form-control mb-2', 'placeholder':'Repita la contraseña'})
        form.fields['username'].label = ''
        form.fields['first_name'].label = ''
        form.fields['last_name'].label = ''
        form.fields['email'].label = ''
        form.fields['password1'].label = ''
        form.fields['password2'].label = ''
        return form    

@method_decorator(login_required, name='dispatch')
class ProfileUpdate(UpdateView):
    form_class = ProfileForm
    success_url = reverse_lazy('profile')
    template_name = 'registration/profile_form.html'

    def get_object(self):
        try:
            return Profile.objects.get(user=self.request.user)
        except Profile.DoesNotExist:
            return Profile.objects.create(user=self.request.user)

@method_decorator(login_required, name='dispatch')
class EmailUpdate(UpdateView):
    form_class = EmailForm
    success_url = reverse_lazy('profile')
    template_name = 'registration/profile_email_form.html'

    def get_object(self):
        return self.request.user
    
    def get_form(self, form_class=None):
        form = super(EmailUpdate, self).get_form()
        form.fields['email'].widget = forms.EmailInput(attrs={'class': 'form-control mb-2', 'placeholder':'Email'})
        return form
    
class update_profile_admin(SuccessMessageMixin, UpdateView):
    model = Profile
    form = UpdateProfileAdminForm
    fields = ['money_type', 'prefered_store']
    success_message = "Se ha actualizado correctamente el perfil."

    def get_success_url(self):
        return reverse('home')
    
def update_profile_admin2(request, template_name="registration/update_profile_admin.html"):
    if request.method == 'POST':
        try:
            postdata = request.POST.copy()
            if postdata['submit'] == 'Actualizar':
                user = request.user
                if (user.is_authenticated):
                    profile = get_object_or_404(Profile, user = user)
                    profile.money_type = int(postdata['money_type'])
                    store_pk = int(postdata['prefered_store'])
                    profile.prefered_store =  get_object_or_404(Store, pk = store_pk) 
                    profile.save()
                    url = reverse('home')
                    return HttpResponseRedirect(url)
        except:
            print("Error") 
    form = UpdateProfileAdminForm()
    return render(request, template_name, locals())