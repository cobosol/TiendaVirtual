from django.shortcuts import render
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin 
from django.urls import reverse, reverse_lazy
# Instanciamos las vistas genéricas de Django 
#from django.views import View
from django.views.generic import ListView, DetailView 
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from utils.forms import PriceForm
from utils.models import Price

#---------- Gestión de productos ----------------
class gestion_precios(ListView):
    model = Price

class crear_precio(SuccessMessageMixin, CreateView):
    model = Price
    form = PriceForm
    fields = "__all__"
    success_message = "Se ha subido correctamente el nuevo precio."

    def get_success_url(self):
        return reverse('precios')

class detal_precio(DetailView):
    model = Price

class actualizar_precio(SuccessMessageMixin, UpdateView):
    model = Price
    form = PriceForm
    fields = "__all__"
    success_message = "Se ha actualizado correctamente el producto."

    def get_success_url(self):
        return reverse('precios')

class eliminar_precio(SuccessMessageMixin, DeleteView):
    model = Price
    form = PriceForm
    fields = "__all__"

    def get_success_url(self): 
        success_message = 'Precio eliminado correctamente!'
        messages.success (self.request, (success_message))       
        return reverse('precios') # Redireccionamos a la vista principal
