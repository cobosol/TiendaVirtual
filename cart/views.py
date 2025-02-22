from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.template import RequestContext
from cart import cart
from django.http import HttpResponseRedirect
from catalog.forms import ProductAddToCartForm
from cart.forms import DeliveryForm
from cart.models import DeliveryInfo
import requests
from registration.models import Profile
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from utils.models import Price
from stores.models import Store
from django.contrib.auth.decorators import login_required

from django.http import HttpResponseRedirect
from ccheckout.ccheckout import get_checkout_url

@login_required
def show_cart(request, template_name="cart/cart.html"):
    form = DeliveryForm(request=request)
    price = Price.objects.filter(is_active=True)[0] # Capturo la configración de precio actual
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
            elif postdata['submit'] == '':
                cart.update_cart(request)
                form = DeliveryForm(request, postdata)
            elif postdata['submit'] == '>':
                cart.update_cart(request)
                form = DeliveryForm(request, postdata)
            elif postdata['submit'] == 'Buscar':
                productSearch = postdata['producto']
                url = '/catalogo/productos/' + productSearch + '/'
                return HttpResponseRedirect(url)
            elif postdata['submit'] == 'Reservar':
                if request.user.is_authenticated:
                    if MND == 'USD':
                        url = reverse('reservar')
                        return HttpResponseRedirect(url)
            elif postdata['submit'] == 'Ir a pagar':
                if request.user.is_authenticated:
                    if MND == 'USD':
                        if cart.cart_subtotal(request) < 2:
                            text = "El monto mínimo para la compra en línea es de 2.00 USD"
                            messages.error(request, text)
                            cart_url = reverse('show_cart')
                            return HttpResponseRedirect(cart_url)
                        url = reverse('checkout')
                        return HttpResponseRedirect(url)
                    else:
                        url = reverse('pagar')
                        return HttpResponseRedirect(url)
                else:
                    messages.warning(request,"Debe estar autenticado para ir a pagar")
            elif postdata['submit'] == 'Confirmar pago':
                url = reverse('efectivo')
                return HttpResponseRedirect(url)
            elif postdata['submit'] == 'Buscar':
                productSearch = postdata['producto']
                url = '/catalogo/productos/' + productSearch + '/'
                return HttpResponseRedirect(url)
            elif postdata['submit'] == 'Actualizar entrega':
                form = DeliveryForm(request, postdata)
                form.storeDelivery = postdata['storeDelivery']
                form.deliveryZone = postdata['deliveryZone']
                delivery = postdata['storeDelivery']
                zone = postdata['deliveryZone']
                cart.set_delivery(request, delivery, zone)
                if (user.is_authenticated):
                    profile.prefered_store = get_object_or_404(Store, pk = postdata['storeDelivery'])
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
    cart_delivery = cart.cart_delivery_price(request, cart_subtotal, MND)
    delivery_name = str(cart.delivery_name(request))
    envio = False
    if delivery_name == 'Envío Habana':
        envio = True 
    cart_total = cart_subtotal + cart_delivery
    deliveryObj = get_object_or_404(DeliveryInfo, client=user)
    zone = deliveryObj.getDeliveryZone
    context = {'cart_total':cart_total, 'envio': envio, 
               'delivery_name': delivery_name, 'cart_delivery':cart_delivery, 
               'cart_subtotal':cart_subtotal, 'zone':zone, 'cart_items':cart_items, 'form':form, 'MND':MND}
    return render(request, template_name, context)