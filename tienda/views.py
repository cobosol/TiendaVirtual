from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.views import View
from catalog.models import Product
from registration.models import Profile
from cart import cart
from promo.models import Banner
from registration.forms import UpdateProfileAdminForm

def index_view(request, template_name="index.html"):
    products = Product.objects.all()
    banners = Banner.objects.all()
    if not products.exists() or not banners.exists():
        return HttpResponseRedirect('https://testtienda.produccionesmuhia.ca/admin')
    distribuidor = False
    productor = False
    user = request.user
    vendedor = False
    profile = Profile
    if (user.is_authenticated):
        profile = get_object_or_404(Profile, user = user)
        if user.groups.filter(name__in=['vendedores']):
            vendedor = True
    if request.method == 'POST':
        try:
            postdata = request.POST.copy()
            if postdata['submit'] == 'Comprar':
                product_slug = postdata.get('product_slug','')
                cart.add_to_cart(request, product_slug)
                if request.session.test_cookie_worked():
                    request.session.delete_test_cookie()
            elif postdata['submit'] == 'Buscar':
                print("Entro a submit Buscar")
                print(postdata)
                productSearch = postdata['producto']
                url = '/catalogo/productos/' + productSearch + '/'
                print(url)
                return HttpResponseRedirect(url)
        except Exception:
                print("Error en el envío de información")
    return render(request, 'index.html', {'products':products, 'banners':banners, 'vendedor':vendedor, 'profile':profile})

""" def file_not_found_404(request):
    page_title = 'Page Not Found'
    return render(request, '404.html', {'title':'Página no encontrada'}) """


def about(request):    
    context={
    }
    return render(request, 'index.html', context)

def services(request):
    context={
    }
    return render(request, 'index.html', context)

def store(request):
    context={
    }
    return render(request, 'index.html', context)

def contact(request):
    context={
    }
    return render(request, 'index.html', context)

def blog(request):
    context={
    }
    return render(request, 'index.html', context)

def sample(request):
    context={
    }
    return render(request, 'index.html', context)

def show_carrito(request, template_name="cart/cart.html"):
    return render(request, template_name, locals())

def show_pagar(request, template_name="cart/checkout.html"):
    return render(request, template_name, locals())

def show_contact(request, template_name="contact/contact.html"):
    return render(request, template_name, locals())
