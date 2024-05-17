from django.shortcuts import render
from django.urls import reverse
from django.template import RequestContext
from cart import cart
from django.http import HttpResponseRedirect
from catalog.forms import ProductAddToCartForm
import requests

from django.http import HttpResponseRedirect
from ccheckout.ccheckout import get_checkout_url

""" def show_cart(request, template_name="cart/cart.html"):
    cart_item_count = cart.cart_distinct_item_count(request)
    page_title = 'Shopping Cart'
    return render(request, template_name, locals()) """

def show_cart(request, template_name="cart/cart.html"):
    if request.method == 'POST':
        postdata = request.POST.copy()
        if postdata['submit'] == 'Eliminar':
            cart.remove_from_cart(request)
        if postdata['submit'] == 'Confirmar':
            cart.update_cart(request)
        if postdata['submit'] == 'Pagar':
            #checkout_url = get_checkout_url(request)
            url = reverse('checkout')
            return HttpResponseRedirect(url)
    cart_items = cart.get_cart_items(request)
    page_title = 'Shopping Cart'
    cart_subtotal = cart.cart_subtotal(request)
    cart_delivery = cart.cart_delivery_price(request)
    cart_total = cart_subtotal + cart_delivery
    return render(request, template_name, locals())