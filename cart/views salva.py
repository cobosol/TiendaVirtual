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
from django.contrib.messages.views import SuccessMessageMixin
from utils.models import Price
from stores.models import Store

from django.http import HttpResponseRedirect
from ccheckout.ccheckout import get_checkout_url

def show_cart(request, template_name="cart/cart.html"):
    form = DeliveryForm(request=request)
    price = Price.objects.filter(is_active=True)[0] # Capturo la configración de precio actual
    MND = 'USD'
    user = request.user
    if (user.is_authenticated):
        profile = get_object_or_404(Profile, user = user)
        MND = profile.MONEY_TYPE[profile.money_type][1]
        delivery_type = profile.prefered_store
        form.delivery_type = int(delivery_type.pk)
        cart.set_delivery(request, delivery_type.pk)
        print("Le puse al delivery session el delivery prefered:")
        print(delivery_type.name)
    try:
        if request.method == 'POST':
            postdata = request.POST.copy()
            print(postdata['submit'])
            if postdata['submit'] == 'X':
                print("X")
                cart.remove_from_cart(request)
                form = DeliveryForm(request, postdata)
            elif postdata['submit'] == 'Cambiar':
                quantity = cart.update_cart(request)
                form = DeliveryForm(request, postdata)
                print(profile.prefered_store)
                #form.delivery_type = profile.prefered_store
            elif postdata['submit'] == 'Ir a pagar':
                if request.user.is_authenticated:
                    if MND == 'USD':
                        if cart.cart_subtotal(request) < 2:
                            fail = reverse('show_cart')
                            text = "El monto mínimo para la compra en línea es de 2.00 USD"
                            messages.error(request, text)
                            cart_url = reverse('show_cart')
                            return HttpResponseRedirect(cart_url)
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
                print("Actualizando factura")
                form = DeliveryForm(request, postdata)
                form.delivery_type = postdata['delivery_type']
                print(postdata['delivery_type'])
                delivery = postdata['delivery_type']
                cart.set_delivery(request, delivery)
                if (user.is_authenticated):
                    profile.prefered_store = get_object_or_404(Store, pk = postdata['delivery_type'])
                    print("Actualizo prefered_store")
                    profile.save()
    except:
        if postdata['quantity']:
            cart.update_cart(request)
    cart_items = cart.get_cart_items(request)
    for cart_i in cart_items:
        text = cart_i.discount_message()
        if text != "":
            messages.info(request, text)
    #st = cart.delivery_Store(request)    
    page_title = 'Shopping Cart'
    cart_subtotal = cart.cart_subtotal(request)
    print(cart_subtotal)
    cart_delivery = cart.cart_delivery_price(request, cart_subtotal)
    print(cart_delivery)
    delivery_name = str(cart.delivery_name(request))
    #deli = cart.get_delivery(request)
    print(delivery_name)
    envio = False
    if delivery_name == 'Envío Habana':
        envio = True 
        print(True)
    cart_total = cart_subtotal + cart_delivery
    print(cart_total)
    vendedor = False 
    if user.groups.filter(name__in=['vendedores']):
        vendedor = True
    print(vendedor)

    #context = {'vendedor':vendedor}
    context = {'vendedor':vendedor, 'cart_total':cart_total, 'envio': envio, 
               'delivery_name': delivery_name, 'cart_delivery':cart_delivery, 
               'cart_subtotal':cart_subtotal, 'cart_items':cart_items, 'form':form, 'MND':MND}
    print(context)
    return render(request, template_name, context)