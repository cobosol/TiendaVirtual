#from ecomstore.checkout import google_checkout
from cart import cart
from .models import Order, OrderItem
from .forms import CheckoutForm
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
import os, sys 
from django.conf import settings
from django.contrib.staticfiles import finders
import json
from django.utils.html import strip_tags
#from core.settings import TOKEN

def loadSecret():
    # read the s3 creds from json file
    try:
        credsFile=open('secrets.txt')
        creds = json.load(credsFile)
        return creds
    except Exception as e:
            print("Error loading oauth secret from local file called 'brightcove_oauth.txt'")
            print("\tThere should be a local file in this directory called brightcove_oauth.txt ")
            print("\tWhich has contents like this:")
            print(""" { "account_id": "1234567890001",
                   "client_id": "30ff0909-0909-33d3-ae88-c9887777a7b7",
                   "client_secret": "mzKKjZZyeW5YgsdfBD37c5730g397agU35-Dsgeox6-73giehbeihgleh659dhgjhdegessDge0s0ynegg987t0996nQ"
                   }"""
            )
            sys.exit("System error: " + str(e) )

env = {
            "base_url" : "https://tropipay-dev.herokuapp.com",
            "mail" : "testdev@mailinator.com",
            "password" : "4321REWq",
            "client_id": "4e5355280b4580ee2ad679d2e8a9a3a2",
            "client_secret": "8aca706ee4eb1d9545c7425d784c5aba",
            "access_token" : "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwYXJlbnQiOm51bGwsImNyZWRlbnRpYWxJZCI6MTI5ODE4LCJjcmVkZW50aWFsTmFtZSI6IjU1ZmM4MDVmYzM1NTY0ZTk1NjI3YTczY2JmODkyY2QzIiwiaWQiOiI3YmY0NTE1MC02NTU4LTExZWQtYmQzMy1mYjc2MWRhNjQ5ODgiLCJpYXQiOjE3MTQ1NzA3NDUsImV4cCI6MTcxNDU3Nzk0NX0.TYIFJHQnK-IoLb6hsrIKC77TfNKqPBhoe7U_j9-DFAE",
            "refresh_token" : "MTcxNDU3MDc0NTg2ODpkNDU3NzY0ZTc5ZDdjOTgzZDNkYjc4NjQ0MzRkOTFmODozNzYyNjYzNDM1MzEzNTMwMmQzNjM1MzUzODJkMzEzMTY1NjQyZDYyNjQzMzMzMmQ2NjYyMzczNjMxNjQ2MTM2MzQzOTM4Mzg=",
            "expires_in" : "1714577945",
            "Funciona bien" : "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwYXJlbnQiOm51bGwsImNyZWRlbnRpYWxJZCI6MTI5ODM4LCJjcmVkZW50aWFsTmFtZSI6IjhkMTg2MjUwNjQxNDcwNWZiNTRiOTZiNDFiYWE5OTJkIiwiaWQiOiI3YmY0NTE1MC02NTU4LTExZWQtYmQzMy1mYjc2MWRhNjQ5ODgiLCJpYXQiOjE3MTQ2NTExMDUsImV4cCI6MTcxNDY1ODMwNX0.OI98aEvQyCrg-6_CKH028VdQFs74dwkIaoRf0dGh8pQ",
            "Nuevo generado" : "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwYXJlbnQiOm51bGwsImNyZWRlbnRpYWxJZCI6MTI5ODM3LCJjcmVkZW50aWFsTmFtZSI6ImM2YTk5NWI5ZTFkYjI0MmYzMDdmZWE2ODI4NmMyMGY4IiwiaWQiOiI3YmY0NTE1MC02NTU4LTExZWQtYmQzMy1mYjc2MWRhNjQ5ODgiLCJpYXQiOjE3MTQ2NTM5NTEsImV4cCI6MTcxNDY2MTE1MX0.EuEI_QCBAAt7U1_NdKxdbiRp_hJHYLqyItBAB4m7kco"
      }      

def createPaymentCardsJSON(request, order_number):
    creds = loadSecret()
    url = "https://tropipay-dev.herokuapp.com/api/v2/paymentcards"

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
        "urlSuccess": "http://127.0.0.1:8000/compra/exito/",
        "urlFailed": "http://127.0.0.1:8000/compra/fallo/",
        "urlNotification": "https://webhook.site/0c8da2ed-ce2a-4f72-9de1-905b662e1e22",
        "serviceDate": "2024-04-30",
        "client": {
            "name": "Pepe",
            "lastName": "Pérez",
            "address": "Calle5, Cotorro, La Habana",
            "phone": "+5358236469",
            "email": "este@gmail.com",
            "countryId": 3,
            "termsAndConditions": "true"
        },
        "directPayment": True,
        "paymentMethods": ["EXT","TPP"]
        }
    
    ordern = order_number['order_number']
    order = Order.objects.filter(id=ordern)[0]
    total = order.total * 100
    payloadDic['amount'] = int(total)
    user = request.user
    client = payloadDic.get('client')
    client['name'] = user.first_name
    #client['lastName'] = user.last_name
    #client['address'] = "" 
    client['phone'] = order.phone
    client['email'] = order.email 
    payloadDic['client'] = client
    print("que tiene client")
    print(client)
    print()

    payload = json.dumps(payloadDic)
    
    headers = {
        'Prefer': 'code=200, example=Example with client data',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwYXJlbnQiOm51bGwsImNyZWRlbnRpYWxJZCI6MTI5ODM3LCJjcmVkZW50aWFsTmFtZSI6ImM2YTk5NWI5ZTFkYjI0MmYzMDdmZWE2ODI4NmMyMGY4IiwiaWQiOiI3YmY0NTE1MC02NTU4LTExZWQtYmQzMy1mYjc2MWRhNjQ5ODgiLCJpYXQiOjE3MTQ2NTM5NTEsImV4cCI6MTcxNDY2MTE1MX0.EuEI_QCBAAt7U1_NdKxdbiRp_hJHYLqyItBAB4m7kco'
        } 
    
    creds = loadSecret()
    headers['Authorization'] = 'Bearer ' + creds["token"]   
    print(headers)

    response = requests.request("POST", url, headers=headers, data=payload)
    return response

    """
      #payload.client.name = user.first_name
      #payload.client.lastName = user.last_name

      #headers["Authorization"] = access_token_T["access_token"]

      #conn = httplib.HTTPSConnection("data.brightcove.com")
      response = requests.request("POST", url, headers = headers, data = payload)
      return response

      """ 
 
""" def tPRefreshToken2():
    try:
        URL = "https://tropipay-dev.herokuapp.com/api/v2/access/token"
        
        headers = {
             "Content-Type": "application/json"
             }
        
        payload = json.dumps({
              "grant_type": "refresh_token",
              "client_id": "5684a554c329aa999d663697e8d3404a",
              "client_secret": "617cf3edfe4bd5db1e385df9154da605",
              "refresh_token": "MTcxNDQ4NzMwNDYxNDoyYWJlMDliOTdiMGQ3NDMyZWZhMTU5MmUwMWZkNzJjNjozNzYyNjYzNDM1MzEzNTMwMmQzNjM1MzUzODJkMzEzMTY1NjQyZDYyNjQzMzMzMmQ2NjYyMzczNjMxNjQ2MTM2MzQzOTM4Mzg="
              })

        response = requests.request("POST", URL, headers = headers, data = payload)
        dicto = json.loads(response.content)
        print(dicto)
        #env["access_token"] = dicto["access_token"]
        return dicto
    except Exception as e:
        print( 'La Exception >> ' + type(e).__name__ )
        raise e      
    
def tPRefreshToken():
    global env
    print("acceso al env")
    print(env["refresh_token"])
    try:
        URL = env["base_url"] + "/api/v2/access/token"
        print(URL)
        headers = {
             "Accept": "application/json",
             "Content-Type": "application/json"
             }

        payload = json.dumps({
              "grant_type": "refresh_token",
              "client_id": env["client_id"],
              "client_secret": env["client_secret"],
              "refresh_token": env["refresh_token"]
              })
        print(payload)
        response = requests.request("POST", URL, headers = headers, data = payload)
        dicto = json.loads(response.content)
        print(dicto)
        #env["access_token"] = dicto["access_token"]
        return dicto
    except Exception as e:
        print( 'La Exception >> ' + type(e).__name__ )
        raise e       """
      
def tPAccessToken():
    try:
        URL = "https://tropipay-dev.herokuapp.com/api/v2/access/token"
        headers = {
              "Accept": "application/json",
              "Content-Type": "application/json"
              }

        payload = json.dumps({
              "grant_type": "client_credentials",
              "client_id": "c6a995b9e1db242f307fea68286c20f8",
              "client_secret": "d1bdbeff05927ca063ae04dbba9a1d42"
              })

        response = requests.request("POST", URL, headers = headers, data = payload)
        return response
    except Exception as e:
        print( 'La Exception >> ' + type(e).__name__ )
        raise e
      
def get_checkout_url(request):
    url = reverse('checkout')
    return HttpResponseRedirect(url)

def process2(request):
    # Transaction results
    APPROVED = '1'
    DECLINED = '2'
    ERROR = '3'
    HELD_FOR_REVIEW = '4'
    postdata = request.POST.copy()
    """ card_num = postdata.get('credit_card_number','')
    exp_month = postdata.get('credit_card_expire_month','')
    exp_year = postdata.get('credit_card_expire_year','') 
    exp_date = exp_month + exp_year
    cvv = postdata.get('credit_card_cvv','')"""
    amount = cart.cart_subtotal(request)
    results = {}
    """ response = authnet.do_auth_capture(amount=amount,
    card_num=card_num,
    exp_date=exp_date,
    card_cvv=cvv) """
    transaction_id = 1 #response[6]
    #if response[0] == APPROVED:
    transaction_id = 1 #response[6]
    order = create_order(request, transaction_id)
    results = {'order_number':order.id,'message':'Creó la orden'}
    """ if response[0] == DECLINED:
        results = {'order_number':0,'message':'There is a problem with your credit card.'}
    if response[0] == ERROR or response[0] == HELD_FOR_REVIEW:
        results = {'order_number':0,'message':'Error processing your order.'} """
    return results

def process_iracuba(request, order_number):
    URL= 'https://stripe-back-3943.onrender.com/api/muhia/stripe'
    headers = {
    'Content-Type': 'application/json',
    }
    data = {
          "total": 10,
          "successUrl": "https://tienda.produccionesmuhia.ca/compra/exitoStripe/",
          "cancelUrl": "https://tienda.produccionesmuhia.ca/compra/fallo"
    }
    ordern = order_number['order_number']
    order = Order.objects.filter(id=ordern)[0]
    total = order.total 
    data['total'] = int(total)
    payload = json.dumps(data)
    try:
        response = requests.post( URL, headers = headers, data = payload )
        print(response)
        resp = json.loads(response.content)
        print(resp)
        return response
    except Exception as e:
        print( 'La Exception >> ' + type(e).__name__ )
        raise e

def create_order(request,transaction_id):
    order = Order()
    checkout_form = CheckoutForm(request.POST, instance=order)
    order = checkout_form.save(commit=False)
    order.transaction_id = transaction_id
    order.ip_address = request.META.get('REMOTE_ADDR')
    order.user = request.user
    order.status = Order.SUBMITTED
    order.delivery_price = cart.cart_delivery_price(request)
    order.save()
    # if the order save succeeded
    if order.pk:
        cart_items = cart.get_cart_items(request)
        for ci in cart_items:
            # create order item for each cart item
            oi = OrderItem()
            oi.order = order
            oi.quantity = ci.quantity
            oi.price = ci.price() # now using @property
            oi.product = ci.product
            oi.store_name = ci.delivery.name
            oi.save()
        # all set, empty cart
        cart.empty_cart(request)
    # return the new order object
    return order

# Generar el pdf
# Para visualizar las imagenes en el pdf
def link_callback(uri, rel):
            """
            Convert HTML URIs to absolute system paths so xhtml2pdf can access those
            resources
            """
            result = finders.find(uri)
            if result:
                    if not isinstance(result, (list, tuple)):
                            result = [result]
                    result = list(os.path.realpath(path) for path in result)
                    path=result[0]
            else:
                    sUrl = settings.STATIC_URL        # Typically /static/
                    sRoot = settings.STATIC_ROOT      # Typically /home/userX/project_static/
                    mUrl = settings.MEDIA_URL         # Typically /media/
                    mRoot = settings.MEDIA_ROOT       # Typically /home/userX/project_static/media/

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
    #Validando roles
    """ if not (request.user.groups.filter(name__in=['Consultor', 'Operador']).exists()) and not request.user.is_superuser:
        raise Http404 """

    #Capturando factura
    #current_factura_object = get_object_or_404(Order, pk = id_orden)
    #print(current_factura_object)
    #Lista de facturas a pasar a la vista
    """     lista_facturas = []
    #Datos a la vista del contenedor
    totales_contenedor = {}  """
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
    #data['order_items'] = orders
    # Cargar el perfil del usurario
    user_profile = Profile.objects.get(user=request.user)
    data['first_name'] = request.user.first_name
    data['last_name'] = request.user.last_name
    data['date'] = order.date
    data['email'] = order.email
    data['phone'] = order.phone
    data['address'] = user_profile.address
    data['importe'] = order.total
    data['delivery_name'] = order.delivery_name
    data['delivery_add1'] = order.delivery_address_1
    data['delivery_add1'] = order.delivery_address_2
    data['state'] = order._state
    data['CI'] = order.delivery_ci
    data['delivery_price'] = order.delivery_price
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


"""     html  = template.render(context)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("utf-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    else:
        print('pdf error')
    return HttpResponse('Unable to process the request, We had some errors<pre>%s</pre>' % escape(html)) """
