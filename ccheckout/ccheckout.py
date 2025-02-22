#from ecomstore.checkout import google_checkout
from cart import cart
from .models import Order, OrderItem
from .forms import CheckoutForm, PagarForm, CachForm
from stores.models import Store, Product_Sales
from utils.models import Price
#from ecomstore.checkout import authnet
import urllib
from django.urls import reverse
from django.http import HttpResponseRedirect
import requests
from io import BytesIO
from re import escape, split
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, JsonResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from registration.models import Profile
from cart.models import DeliveryInfo
import os, sys 
from django.conf import settings
from django.contrib.staticfiles import finders
import json
from django.utils.html import strip_tags
import decimal

def loadSecret():
    try:
        credsFile=open('secrets.txt')
        creds = json.load(credsFile)
        return creds
    except Exception as e:
            print("Error Leyendo el fichero secrets")
            sys.exit("System error: " + str(e) )

""" env = {
            "base_url" : "https://www.tropipay.com",
            "mail" : "mmalbo@nauta.cu",
            "password" : "...",
            "client_id": "0d94edaf6b147f37453a239f8b7a9451",
            "client_secret": "e303cdd52ec325ff7c88577cfdef63c4",
            "access_token" : "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwYXJlbnQiOm51bGwsImNyZWRlbnRpYWxJZCI6MTI5ODE4LCJjcmVkZW50aWFsTmFtZSI6IjU1ZmM4MDVmYzM1NTY0ZTk1NjI3YTczY2JmODkyY2QzIiwiaWQiOiI3YmY0NTE1MC02NTU4LTExZWQtYmQzMy1mYjc2MWRhNjQ5ODgiLCJpYXQiOjE3MTQ1NzA3NDUsImV4cCI6MTcxNDU3Nzk0NX0.TYIFJHQnK-IoLb6hsrIKC77TfNKqPBhoe7U_j9-DFAE",
            "refresh_token" : "MTcxNDU3MDc0NTg2ODpkNDU3NzY0ZTc5ZDdjOTgzZDNkYjc4NjQ0MzRkOTFmODozNzYyNjYzNDM1MzEzNTMwMmQzNjM1MzUzODJkMzEzMTY1NjQyZDYyNjQzMzMzMmQ2NjYyMzczNjMxNjQ2MTM2MzQzOTM4Mzg=",
            "expires_in" : "1714577945",
            "Funciona bien" : "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwYXJlbnQiOm51bGwsImNyZWRlbnRpYWxJZCI6MTI5ODM4LCJjcmVkZW50aWFsTmFtZSI6IjhkMTg2MjUwNjQxNDcwNWZiNTRiOTZiNDFiYWE5OTJkIiwiaWQiOiI3YmY0NTE1MC02NTU4LTExZWQtYmQzMy1mYjc2MWRhNjQ5ODgiLCJpYXQiOjE3MTQ2NTExMDUsImV4cCI6MTcxNDY1ODMwNX0.OI98aEvQyCrg-6_CKH028VdQFs74dwkIaoRf0dGh8pQ",
            "Nuevo generado" : "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwYXJlbnQiOm51bGwsImNyZWRlbnRpYWxJZCI6MTI5ODM3LCJjcmVkZW50aWFsTmFtZSI6ImM2YTk5NWI5ZTFkYjI0MmYzMDdmZWE2ODI4NmMyMGY4IiwiaWQiOiI3YmY0NTE1MC02NTU4LTExZWQtYmQzMy1mYjc2MWRhNjQ5ODgiLCJpYXQiOjE3MTQ2NTM5NTEsImV4cCI6MTcxNDY2MTE1MX0.EuEI_QCBAAt7U1_NdKxdbiRp_hJHYLqyItBAB4m7kco"
      }      """ 

def createPaymentCardsJSON(request, order_number):
    creds = loadSecret()
    url = creds['URL_Payment'] 

    payloadDic = {
        "reference": "Tienda Virtual MUHIA",
        "concept": "Compra de productos",
        "favorite": True,
        "description": "Productos MUHIA",
        "amount": 4000,
        "currency": "USD",
        "singleUse": True,
        "reasonId": 4,
        "expirationDays": 1,
        "lang": "es",
        "urlSuccess": "exito",
        "urlFailed": "fallo",
        "urlNotification": "notificacion",
        "serviceDate": "2024-04-30",
        "client": {
            "name": "Nombre",
            "lastName": "Apellido",
            "address": "Direccion",
            "phone": "+5555555555",
            "email": "correo@servidor.com",
            "countryId": 1,
            "termsAndConditions": "true",
            "city":"Barcelona",
            "postCode": "78622"
        },
        "directPayment": True,
        "paymentMethods": ["EXT","TPP"]
        }
    
    ordern = order_number['order_number']
    order = Order.objects.filter(id=ordern)[0]
    total = order.total * 100
    payloadDic['amount'] = int(total)
    payloadDic['urlSuccess'] = creds['urlSuccess']
    payloadDic['urlFailed'] = creds['urlFailed']
    payloadDic['urlNotification'] = creds['urlNotification']
    user = request.user
    client = payloadDic.get('client')
    client['name'] = order.payment_name 
    client['phone'] = order.payment_phone
    client['email'] = order.payment_email
    client['city'] = order.payment_city
    client['postCode'] = order.payment_postCode
    payloadDic['reasonId'] = ordern
    payloadDic['client'] = client

    payload = json.dumps(payloadDic)
    
    headers = {
        'Prefer': 'code=200, example=Example with client data',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwYXJlbnQiOm51bGwsImNyZWRlbnRpYWxJZCI6MTI5ODM3LCJjcmVkZW50aWFsTmFtZSI6ImM2YTk5NWI5ZTFkYjI0MmYzMDdmZWE2ODI4NmMyMGY4IiwiaWQiOiI3YmY0NTE1MC02NTU4LTExZWQtYmQzMy1mYjc2MWRhNjQ5ODgiLCJpYXQiOjE3MTQ2NTM5NTEsImV4cCI6MTcxNDY2MTE1MX0.EuEI_QCBAAt7U1_NdKxdbiRp_hJHYLqyItBAB4m7kco'
        } 
    
    headers['Authorization'] = 'Bearer ' + creds["token"]   
    print(headers)
    print(payload)

    response = requests.request("POST", url, headers=headers, data=payload)
    return response
      
def tPAccessToken():
    try:
        headers = {
              "Accept": "application/json",
              "Content-Type": "application/json"
              }
        data1 = {
              "grant_type": "client_credentials",
              "client_id": "0d94edaf6b147f37453a239f8b7a9451",
              "client_secret": "e303cdd52ec325ff7c88577cfdef63c4"
              }
        
        creds = loadSecret()
        URL = creds['URL_AccessToken']
        data1["client_id"] = creds["client_id"]
        data1["client_secret"] = creds["client_secret"]

        payload = json.dumps(data1)
        
        response = requests.request("POST", URL, headers = headers, data = payload)
        return response
    except Exception as e:
        print( 'La Exception >> ' + type(e).__name__ )
        raise e
      
def get_checkout_url(request):
    url = reverse('checkout')
    return HttpResponseRedirect(url)

def process2(request, usd=True):
    postdata = request.POST.copy()
    amount = cart.cart_subtotal(request)
    results = {}
    transaction_id = 1
    order = create_order(request, transaction_id, usd)
    results = {'order_number':order.id,'message':'Creo la orden'}
    return results

def create_order(request, transaction_id, usd = True, cach = False):
    if not cart.verify_cart_items(request):
        results = {'order_number':-1,'message':'No se pudo crear la orden'}
        return results
    order = Order() # Creo la nueva orden vacía
    store = cart.delivery_Store(request) # Capturo el almacen
    price2 = Price.objects.filter(is_active=True)[0] # Capturo la configuración de precio actual
    user = request.user # capturo el usuario registrado
    profile = get_object_or_404(Profile, user = user) # Accedo a su perfil
    MND = profile.MONEY_TYPE[profile.money_type][1] # Saco el tipo de moneda del usuario
    results = {} # Crear variable para la respuesta
    if transaction_id == 2:
        checkout_form = PagarForm(request.POST, instance=order)
        order = checkout_form.save(commit=False)
        order.currency = 'USD'
        deliveryInfo = get_object_or_404(DeliveryInfo, client=request.user)
        cart_subtotal = cart.cart_subtotal(request)
        order.delivery_price = cart.cart_delivery_price(request, cart_subtotal, MND)
        print(order.delivery_price)
    else:
        if cach: # Si se va a pagar en efectivo guardo la información de la Form para efectivo
            checkout_form = CachForm(request.POST, instance=order)
            order = checkout_form.save(commit=False)
            if usd: # Guardo el tipo de moneda en efectivo
                order.currency = 'USD'
            else:
                order.currency = 'CUP'
                order.delivery_price = store.price_cup
        else: # Si es pago por tarjeta
            if usd: # Tarjetas internacionales
                checkout_form = CheckoutForm(request.POST, instance=order)
                order = checkout_form.save(commit=False)
                order.currency = 'USD'
                deliveryInfo = get_object_or_404(DeliveryInfo, client=request.user)
                order.delivery_price = deliveryInfo.calculate_deliveryHabana()
            else: # tarjetas nacionales
                pagar_form = PagarForm(request.POST, instance=order)
                order = pagar_form.save(commit=False)
                if MND == 'CUP': # Si el usuario tiene en su perfil moneda CUP
                    order.delivery_price = store.price_cup
                    order.currency = 'CUP'
                else: # Si tiene en su perfil MLC
                    order.delivery_price = store.price_mlc
                    order.currency = 'MLC'
    #Lleno datos iguales para todo tipo de pago
    order.user = user
    order.transaction_id = transaction_id # Esto viene por parámetro
    order.ip_address = request.META.get('REMOTE_ADDR')
    order.delivery = store
    order.store_name = store.name
    order.price = price2    
    order.save()
    if order.pk:
        cart_items = cart.get_cart_items(request)
        for ci in cart_items:
            oi = OrderItem()
            oi.order = order
            oi.product = ci.product
            oi.store_name = cart.delivery_name(request)
            oi.quantity = ci.quantity
            #actualizar la cantidad de reservado del producto en ese almacen
            prod = ci.product
            if MND == 'USD':
                oi.price = ci.price_USD()
            elif MND == 'CUP':
                oi.price = ci.price_CUP()
            else:
                oi.price = ci.price_MLC()
            oi.save()
        order.update_status(Order.SUBMITTED) 
        order.save()
        print(order.delivery_price)
        print(order.total)
        # all set, empty cart
        cart.empty_cart(request)
    # return the new order object
    results = {'order_number':order.id,'message':'Creo la orden'}
    return results

# Generar el pdf
# Para visualizar las imagenes en el pdf
def link_callback(uri, rel):
            result = finders.find(uri)
            if result:
                    if not isinstance(result, (list, tuple)):
                            result = [result]
                    result = list(os.path.realpath(path) for path in result)
                    path=result[0]
            else:
                    sUrl = settings.STATIC_URL       
                    sRoot = settings.STATIC_ROOT     
                    mUrl = settings.MEDIA_URL        
                    mRoot = settings.MEDIA_ROOT   

                    if uri.startswith(mUrl):
                            path = os.path.join(mRoot, uri.replace(mUrl, ""))
                    elif uri.startswith(sUrl):
                            path = os.path.join(sRoot, uri.replace(sUrl, ""))
                    else:
                            return uri

            # make sure that file exists
            if not os.path.isfile(path):
                    raise RuntimeError(
                            'media URI must start with %s or %s' % (sUrl, mUrl)
                    )
            return path

def export_pdf(request, id_orden):
    data = {}
    #Diccionario de factura
    current_factura = {}        
    #QR datos de transaccion
    qr_generado = '{"id_orden": ' + str(id_orden) 
    #Generando reporte PDF
    template_src = 'checkout/factura_base.html'
    template = get_template(template_src)
    data['id_order'] = id_orden
    orders = OrderItem.objects.filter(order=id_orden)
    order = Order.objects.filter(id=id_orden)[0]
    data['order'] = order
    # Cargar el perfil del usurario
    user_profile = Profile.objects.get(user=order.user)
    data['first_name'] = order.user.first_name
    data['last_name'] = order.user.last_name
    data['date'] = order.date
    data['email'] = order.user.email
    data['phone'] = order.payment_phone
    data['address'] = user_profile.address
    data['importe'] = decimal.Decimal(order.total)
    data['delivery_name'] = order.delivery_name
    if order.delivery_street and order.delivery_apto and order.delivery_between:
        delivery_add1 = order.delivery_street + " " + order.delivery_apto + " entre " + order.delivery_between + ". " + order.SUBSTATE[order.delivery_substate][1] + ", " + order.delivery_state
        data['delivery_add1'] = delivery_add1
    else:
        data['delivery_add1'] = " "
    data['delivery_add2'] = order.delivery_address_2
    data['state'] = order._state
    data['delivery_phone'] = order.delivery_phone
    data['delivery_ws'] = order.delivery_ws
    data['CI'] = order.delivery_ci
    data['delivery_price'] = decimal.Decimal(order.delivery_price)
    data['currency'] = order.currency
    context = {'data': data, 'orders': orders, 'request': request,'qr':qr_generado}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="factura.pdf"'
    html = template.render(context)
    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response, link_callback=link_callback)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
