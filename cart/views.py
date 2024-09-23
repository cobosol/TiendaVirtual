from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.template import RequestContext
from cart import cart
from django.http import HttpResponseRedirect
from catalog.forms import ProductAddToCartForm
from cart.forms import DeliveryForm
import requests
from registration.models import Profile
from django.contrib import messages


from django.http import HttpResponseRedirect
from ccheckout.ccheckout import get_checkout_url

def show_cart(request, template_name="cart/cart.html"):
    form = DeliveryForm(request=request)
    MND = 'USD'
    user = request.user
    if (user.is_authenticated):
        profile = get_object_or_404(Profile, user = user)
        MND = profile.MONEY_TYPE[profile.money_type][1]
    try:
        if request.method == 'POST':
            postdata = request.POST.copy()
            if postdata['submit'] == 'X':
                cart.remove_from_cart(request)
                form = DeliveryForm(request, postdata)
            elif postdata['submit'] == 'Cambiar':
                cart.update_cart(request)
                form = DeliveryForm(request, postdata)
            elif postdata['submit'] == 'Ir a pagar':
                if request.user.is_authenticated:
                    if MND == 'USD':
                        url = reverse('checkout')
                        return HttpResponseRedirect(url)
                    else:
                        url = reverse('pagar')
                        return HttpResponseRedirect(url)
                    """ elif user.groups.filter(name__in=['vendedores']):
                    url = reverse('pagar')
                    return HttpResponseRedirect(url) """
                else:
                    messages.info(request,"Debe estar autenticado para ir a pagar")
            elif postdata['submit'] == 'Confirmar pago':
                url = reverse('efectivo')
                return HttpResponseRedirect(url)
            elif postdata['submit'] == 'Actualizar Factura':
                form = DeliveryForm(request, postdata)
                form.delivery_type = postdata['delivery_type']
                delivery = postdata['delivery_type']
                cart.set_delivery(request, delivery)
    except:
        if postdata['quantity']:
            cart.update_cart(request)
    cart_items = cart.get_cart_items(request)
    st = cart.delivery_Store(request)    
    page_title = 'Shopping Cart'
    cart_subtotal = cart.cart_subtotal(request)
    cart_delivery = cart.cart_delivery_price(request)
    delivery_name = cart.delivery_name(request)
    deli = cart.get_delivery(request)
    envio = False
    if deli == '3':
        envio = True 
    cart_total = cart_subtotal + cart_delivery 
    vendedor = user.groups.filter(name__in=['vendedores'])
    return render(request, template_name, locals())