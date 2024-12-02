from django.shortcuts import render, redirect, get_object_or_404
from catalog.models import Category, Product
from django.template import RequestContext
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
import uuid
from django.core.files.base import ContentFile
from base64 import b64decode

#Librerías para mensajes, algunos basados en views
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin 

# Instanciamos las vistas genéricas de Django 
#from django.views import View
from django.views.generic import ListView, DetailView 
from django.views.generic.edit import CreateView, UpdateView, DeleteView

# Habilitamos los formularios en Django
from django import forms

#from registration.views import superuser_only

# Importamos lo necesario de la aplicación
from cart import cart
from catalog.forms import ProductAddToCartForm, SelectStoreForm
from stores.models import Store, Product_Sales
from catalog.models import *
from pages.models import *
from .forms import ProductAdminForm, ProductForm, ProductAlmacenForm

def index(request, template_name="index.html"):
    context = {'name':'Tienda Virtual MUHIA'}
    return render(request, template_name, context)

def show_search(request, productSearch, template_name="catalog/search.html"):
    productSearch = Product.objects.filter(meta_keywords__icontains=productSearch)
    products = Product.objects.filter(is_active=True)
    if request.method == 'POST':
        try:
            postdata = request.POST.copy()
            if postdata['submit'] == 'Comprar': 
                product_slug = postdata.get('product_slug','')
                if cart.add_to_cart(request, product_slug):
                    if request.session.test_cookie_worked():
                        request.session.delete_test_cookie()
                else:
                    messages.info(request,"No hay disponibilidad del producto")       
            elif postdata['submit'] == 'Buscar':
                productSearch = postdata['producto']
                url = '/catalogo/productos/' + productSearch + '/'
                return HttpResponseRedirect(url) 
        except Exception:
            print("Error al adicionar al carrito")
    return render(request, template_name, locals())    

def show_category(request, category_slug, template_name="catalog/category.html"):
    c = get_object_or_404(Category, slug=category_slug)
    products = c.product_set.all()
    page_title = c.name
    meta_keywords = c.meta_keywords
    meta_description = c.meta_description
    cart_items = cart.get_cart_items(request)
    product = get_object_or_404(Product, pk=1)
    vendedor = False
    if (request.user.is_authenticated):
        if request.user.groups.filter(name__in=['vendedores']):
            vendedor = True
    # Add to cart
    if request.method == 'POST':
        try:
            postdata = request.POST.copy()
            if postdata['submit'] == 'Comprar': 
                product_slug = postdata.get('product_slug','')
                if cart.add_to_cart(request, product_slug):
                    if request.session.test_cookie_worked():
                        request.session.delete_test_cookie()
                else:
                    messages.info(request,"No hay disponibilidad del producto")       
            elif postdata['submit'] == 'Buscar':
                productSearch = postdata['producto']
                url = '/catalogo/productos/' + productSearch + '/'
                return HttpResponseRedirect(url) 
        except Exception:
            print("Error al adicionar al carrito")
    request.session.set_test_cookie()
    return render(request, template_name, locals())

def show_categories(request, template_name="catalog/categories.html"):
    return render(request, template_name, locals())

def validateCount(postdata, products_stores):
    dely = postdata['delivery_type']
    s = get_object_or_404(Store, pk=dely)
    for ps in products_stores:
        if ps.store.slug == s.slug:
            if int(postdata['quantity']) > ps.available:
                return False
            return True
    return False

def get_Product_Store(postdata, products_stores):
    dely = postdata['delivery_type']
    s = get_object_or_404(Store, pk=dely)
    for ps in products_stores:
        if ps.store.slug == s.slug:
            return ps
    return 0

# new product view, with POST vs GET detection
def show_product(request, product_slug, template_name="catalog/product.html"):
    p = get_object_or_404(Product, slug=product_slug)    
    products_stores = Product_Sales.objects.filter(product=p)
    categories = p.categories.all()
    page_title = p.name
    meta_keywords = p.meta_keywords
    meta_description = p.meta_description
    quantity = 1
    delivery = 1
    vendedor = False
    if (request.user.is_authenticated):
        if request.user.groups.filter(name__in=['vendedores']):
            vendedor = True
    if request.method == 'POST':
        try:
            postdata = request.POST.copy()
            if postdata['submit'] == 'Comprar': 
                product_slug = postdata.get('product_slug','')
                flag = cart.add_to_cart(request, product_slug)
                if request.session.test_cookie_worked():
                    request.session.delete_test_cookie()
                url = reverse('show_cart')
                return HttpResponseRedirect(url)
            elif postdata['submit'] == 'Buscar':
                productSearch = postdata['producto']
                url = '/catalogo/productos/' + productSearch + '/'
                return HttpResponseRedirect(url)
        except Exception:
            messages.error(request,"Error desconocido en el envío de información")
    request.session.set_test_cookie()
    return render(request, template_name, locals())

#@method_decorator(superuser_only)
def i_admin(request):
    return render(request, "catalog/gestion.html", {})

#---------- Gestión de productos ----------------
class gestion_productos(ListView):
    model = Product

class crear_producto(SuccessMessageMixin, CreateView):
    model = Product
    form = ProductForm
    fields = ('name', 'gname', 'presentation', 'brand', 'sku', 'price', 'price_base', 'old_price', 
              'image', 'is_active', 'is_bestseller', 'is_featured', 'prod_datasheet', 'description', 
              'is_feedstock', 'available_CUP', 'available_MLC',
              'meta_keywords', 'meta_description', 'categories')
    success_message = "Se ha subido correctamente el nuevo producto."

    def get_success_url(self):
        return reverse('productos')

class detal_producto(DetailView):
    model = Product

class actualizar_producto(SuccessMessageMixin, UpdateView):
    model = Product
    form = ProductForm
    fields = ('name', 'gname', 'presentation', 'brand', 'sku', 'price', 'price_base', 'old_price', 
              'image', 'is_active', 'is_bestseller', 'is_featured', 'prod_datasheet', 'description', 
                'is_feedstock', 'available_online', 'available_CUP', 'available_MLC',
              'meta_keywords', 'meta_description', 'categories')
    success_message = "Se ha actualizado correctamente el producto."

    def get_success_url(self):
        return reverse('productos')

class eliminar_producto(SuccessMessageMixin, DeleteView):
    model = Product
    form = ProductForm
    fields = "__all__"

    def get_success_url(self): 
        success_message = 'Producto eliminado correctamente!'
        messages.success (self.request, (success_message))       
        return reverse('productos') # Redireccionamos a la vista principal



#---------- Gestión de productos en almacen----------------
""" class gestion_productos_almacen(ListView):
    model = Product_Sales """

def gestion_productos_almacen(request, template_name="catalog/productos_almacen_admin.html"):
    form = SelectStoreForm(request=request)
    try:
        if request.method == 'POST':
            postdata = request.POST.copy()
            print(postdata)
            if postdata['submit'] == 'Ver':
                form = SelectStoreForm(request, postdata)
                form.selected_store = postdata['selected_store']
                object_list = Product_Sales.objects.filter(store=postdata['selected_store'])
        else:
            object_list = Product_Sales.objects.filter(pk=1)
    except:
        text = "Error al seleccionar el almacén"
        messages.error(request, text)
    context={'object_list':object_list, 'form':form}
    return render(request, template_name, context)

class crear_producto_almacen(SuccessMessageMixin, CreateView):
    model = Product_Sales
    form = ProductAlmacenForm
    fields = "__all__"
    success_message = "Se ha subido correctamente el nuevo producto."

    def get_success_url(self):
        return reverse('productos_almacen')

class detal_producto_almacen(DetailView):
    model = Product_Sales

class actualizar_producto_almacen(SuccessMessageMixin, UpdateView):
    model = Product_Sales
    form = ProductAlmacenForm
    fields = "__all__"
    success_message = "Se ha actualizado correctamente el producto."

    def get_success_url(self):
        return reverse('productos_almacen')

class eliminar_producto_almacen(SuccessMessageMixin, DeleteView):
    model = Product_Sales
    form = ProductAlmacenForm
    fields = "__all__"

    def get_success_url(self): 
        success_message = 'Producto eliminado correctamente!'
        messages.success (self.request, (success_message))       
        return reverse('productos_almacen') # Redireccionamos a la vista principal