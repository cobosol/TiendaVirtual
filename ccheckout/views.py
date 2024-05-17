from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect
from .forms import CheckoutForm
from django.urls import reverse
from .models import Order, OrderItem
from ccheckout.ccheckout import process2, export_pdf, createPaymentCardsJSON, process_iracuba, tPAccessToken, loadSecret
from cart import cart
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, JsonResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
from re import escape, split
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import json
from tienda.settings import API_CLIENT, API_SECRET
import hashlib
from .views import loadSecret


def payment_notification(request):
    response=json.loads(request.raw_post_data)
    if response["status"] == "OK":
        data = response["data"]
        signature = response["signaturev2"]
        bankOrderCode = data["bankOrderCode"]
        creds = loadSecret()
        clientId = "c6a995b9e1db242f307fea68286c20f8" #creds["client_id"]
        clientSecret = "d1bdbeff05927ca063ae04dbba9a1d42" #creds["client_secret"]
        originalCurrencyAmount = data["originalCurrencyAmount"]
        chekSignature = hashlib.sha256( bankOrderCode + clientId + clientSecret + originalCurrencyAmount )
        if signature == chekSignature:
            order_number = request.session.get('order_number','')
            if order_number:
                order = Order.objects.filter(id=order_number)[0]
                order.status = Order.PROCESSED
                order.transaction_id = data["id"]
                order.save()
    else:
        print("status=KO")
    return request

def hit(request):
    print(request)
    order_number = request.session.get('order_number','')
    if order_number:
        order = Order.objects.filter(id=order_number)[0]
        if order.status == Order.PROCESSED: #SUBMITTED: # PROCESSED
            receipt_url = reverse('checkout_receipt')
            return HttpResponseRedirect(receipt_url)
        else:
            fail_url = reverse('checkout_fail')
            return HttpResponseRedirect(fail_url)
    else:
        print("Error en el número de la orden")

def hitS(request):
    postdata = request.POST.copy()
    order_number = request.session.get('order_number','')
    if order_number:
        order = Order.objects.filter(id=order_number)[0]
        order.status = Order.PROCESSED
        order.save()
        receipt_url = reverse('checkout_receipt')
        return HttpResponseRedirect(receipt_url)

@login_required
def show_checkout(request, template_name='checkout/checkout.html'):
    if cart.is_empty(request):
        cart_url = reverse('show_cart')
        return HttpResponseRedirect(cart_url)
    if request.method == 'POST': 
        postdata = request.POST.copy()
        #print("El valor de value?")
        #print(request.POST.get('value'))
        #print(postdata['submit'])
        if postdata['submit'] == 'Pagar con Tropipay':
            form = CheckoutForm(postdata)
            #form.name = request.user.first_name + request.user.last_name
            if form.is_valid():
                #response = process_iracuba(request)
                order_number = process2(request) 
                error_message = postdata.get('message','')
                if order_number:
                    request.session['order_number'] = order_number['order_number']
                    # Creada la orden llamo a efectuar el pago por tropipay
                    #print("Llamo a crear pago")
                    response = createPaymentCardsJSON(request, order_number)
                    dicto = json.loads(response.content)
                    print(dicto)
                    try:
                        print("Entro al try y trato de llamar a la URL de pago")
                        url_pay = dicto["shortUrl"]
                        return HttpResponseRedirect(url_pay)
                    except Exception as e:
                        print("Error en: ")
                        print(dicto["error"]["code"])
                        if dicto["error"]["code"] == "EXPIRED_TOKEN":
                            response = tPAccessToken()
                            dicto = json.loads(response.content)
                            creds = loadSecret()
                            creds["token"] = dicto.get('access_token')
                            #"Guardo el token actualizado en el fichero")
                            with open('secrets.txt', 'w') as archivo:
                                json.dump(creds, archivo)
                            #("Llamo por segunda vez al pago")
                            response2 = createPaymentCardsJSON(request, order_number)
                            dicto2 = json.loads(response2.content)
                            print(dicto2)
                            #print("llamo por segunda vez a la URL de pago")
                            url_pay = dicto2["shortUrl"]
                            return HttpResponseRedirect(url_pay)
                        else:
                            fail_url = reverse('checkout_fail')
                            return HttpResponseRedirect(fail_url)
            else:
                fail_url = reverse('checkout_fail')
                return HttpResponseRedirect(fail_url)
        elif postdata['submit'] == 'Efectuar Pago':
            form = CheckoutForm(postdata)
            #form.name = request.user.first_name + request.user.last_name
            if form.is_valid():
                #response = process_iracuba(request)
                order_number = process2(request) 
                error_message = postdata.get('message','')
                if order_number:
                    request.session['order_number'] = order_number['order_number']
                    # Creada la orden llamo a efectuar el pago por tropipay
                    #print("Llamo a crear pago")
                    try:
                        response = process_iracuba(request, order_number)
                        url_pay = json.loads(response.content)
                        print(url_pay)
                        return HttpResponseRedirect(url_pay)
                    except Exception as e:
                        print("Error en pago con Stripe")
            else:
                messages.error(request,form.errors.as_data)
                error_message = 'Corrija los errores señalados'
        elif postdata['submit'] == 'Confirmar pago efectivo':
                form = CheckoutForm(postdata)
                #form.name = request.user.first_name + request.user.last_name
                if form.is_valid():
                    #response = process_iracuba(request)
                    order_number = process2(request) 
                    error_message = postdata.get('message','')
                    if order_number:
                        request.session['order_number'] = order_number['order_number']
                        order = Order.objects.filter(id=order_number['order_number'])[0]
                        order.status = Order.ENTREGADA
                        order.transaction_id = 1
                        order.save()
                        receipt_url = reverse('checkout_receipt')
                        return HttpResponseRedirect(receipt_url)
                else:
                    messages.error(request,form.errors.as_data)
                    error_message = 'Corrija los errores señalados'
    else:
        form = CheckoutForm()
        form.name = request.user.first_name + request.user.last_name
    page_title = 'Checkout'
    cobra_efectivo = False
    if (request.user.groups.filter(name='Tendero').exists() or request.user.is_superuser):
        cobra_efectivo = True

    return render(request, template_name, locals())

def receipt(request, template_name='checkout/receipt.html'):
    order_number = request.session.get('order_number','')
    if order_number:
        order = Order.objects.filter(id=order_number)[0]
        order_items = OrderItem.objects.filter(order=order_number)
        orderN = order_number
        user = order.user
        """ del request.session['order_number'] """
    else:
        print(str(order_number) + 'No existe la orden')
        cart_url = reverse('show_cart')
        return HttpResponseRedirect(cart_url)
    # Capturar el POST de un botón para generar pdf
    if request.method == 'POST':
        del request.session['order_number']
        return export_pdf(request, order_number)
    return render(request, template_name, locals())

def orders_list(request, template_name='checkout/orders_list.html'):
    if request.method == 'POST':
        postdata = request.POST.copy()
        if postdata['submit'] == 'Generar factura':
            order_number = postdata['order_id']
            return export_pdf(request, order_number)
    orders = Order.objects.filter(user=request.user)
    return render(request, template_name, locals())

def admin_orders_list(request, template_name='checkout/orders_list.html'):
    if request.method == 'POST':
        postdata = request.POST.copy()
        if postdata['submit'] == 'Generar factura':
            order_number = postdata['order_id']
            return export_pdf(request, order_number)
        return HttpResponseRedirect(receipt)
    orders = Order.objects.all()
    return render(request, template_name, locals())

def fail(request, template_name='checkout/fail.html'):
    return render(request, template_name, locals())
