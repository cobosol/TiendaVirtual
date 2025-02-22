from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.views import View
from catalog.models import Product
from registration.models import Profile
from cart import cart
from promo.models import Banner, Offer
from registration.forms import UpdateProfileAdminForm

def index_view(request, template_name="index.html"):
    products = Product.objects.filter(is_active=True)
    bestsellers = Product.objects.filter(is_bestseller=True)
    banners = Banner.objects.all()
    offers1 = Offer.objects.filter(main=True)
    offers2 = Offer.objects.filter(second=True)
    if not products.exists() or not banners.exists() or not offers1.exists() or not offers2.exists():
        return HttpResponseRedirect('https://testtienda.produccionesmuhia.ca/admin')
    else:
        offer1 = offers1[0]
        offer2 = offers2[0]
    """ distribuidor = False
    productor = False
    vendedor = False
    marketing = False
    adminAccess = False
    comercial = False """
    user = request.user
    profile = Profile
    if (user.is_authenticated):
        profile = get_object_or_404(Profile, user = user)
        """ if user.groups.filter(name__in=['vendedores']):
            vendedor = True
            adminAccess = True
        if user.groups.filter(name__in=['marketing']):
            marketing = True
            adminAccess = True
        if user.groups.filter(name__in=['comercial']):
            comercial = True
            adminAccess = True """
    if request.method == 'POST':
        try:
            postdata = request.POST.copy()
            if postdata['submit'] == 'Comprar':
                product_slug = postdata.get('product_slug','')
                if not cart.add_to_cart(request, product_slug):
                  url = '/accounts/login/'
                  return HttpResponseRedirect(url)  
                if request.session.test_cookie_worked():
                    request.session.delete_test_cookie()
            elif postdata['submit'] == 'Buscar':
                productSearch = postdata['producto']
                url = '/catalogo/productos/' + productSearch + '/'
                return HttpResponseRedirect(url)
        except Exception:
                print("Error en el envío de información")
    return render(request, 'index.html', {'products':products, 'banners':banners, 'bestsellers':bestsellers, 'offer1':offer1, 'offer2':offer2, 'profile':profile})


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
