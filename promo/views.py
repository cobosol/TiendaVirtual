from django.shortcuts import render
from .models import Banner, Offer
from .forms import BannerForm, OfferForm

#Librerías para mensajes, algunos basados en views
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin 

# Instanciamos las vistas genéricas de Django 
#from django.views import View
from django.views.generic import ListView, DetailView 
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.urls import reverse, reverse_lazy

def banner(request):
    banners = Banner.objects.all()
    return render(request, "promo/banner.html", {'banners':banners})

#---------- Gestión de banners ----------------
class gestion_banners(ListView):
    model = Banner

class crear_banner(SuccessMessageMixin, CreateView):
    model = Banner
    form = BannerForm
    fields = "__all__"
    success_message = "Se ha subido correctamente el banner."

    def get_success_url(self):
        return reverse('banners')

class detal_banner(DetailView):
    model = Banner

class actualizar_banner(SuccessMessageMixin, UpdateView):
    model = Banner
    form = BannerForm
    fields = "__all__"
    success_message = "Se ha actualizado correctamente el banner."

    def get_success_url(self):
        return reverse('banners')

class eliminar_banner(SuccessMessageMixin, DeleteView):
    model = Banner
    form = BannerForm
    fields = "__all__"

    def get_success_url(self): 
        success_message = 'El banner fue eliminado correctamente!'
        messages.success (self.request, (success_message))       
        return reverse('banners') # Redireccionamos a la vista principal
    
def banner(request):
    banners = Banner.objects.all()
    return render(request, "promo/banner.html", {'banners':banners})

#---------- Gestión de ofertas ----------------
class gestion_offers(ListView):
    model = Offer

class crear_offer(SuccessMessageMixin, CreateView):
    model = Offer
    form = OfferForm
    fields = "__all__"
    success_message = "Se ha subido correctamente la oferta."

    def get_success_url(self):
        return reverse('offers')

class detal_offer(DetailView):
    model = Offer

class actualizar_offer(SuccessMessageMixin, UpdateView):
    model = Offer
    form = OfferForm
    fields = "__all__"
    success_message = "Se ha actualizado correctamente la oferta."

    def get_success_url(self):
        return reverse('offers')

class eliminar_offer(SuccessMessageMixin, DeleteView):
    model = Offer
    form = OfferForm
    fields = "__all__"

    def get_success_url(self): 
        success_message = 'La oferta fue eliminada correctamente!'
        messages.success (self.request, (success_message))       
        return reverse('offers') # Redireccionamos a la vista principal