from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect
from .forms import CheckoutForm, UpdateStatusForm, PagarForm, CachForm, ReserveForm
from django.urls import reverse
from .models import Order, OrderItem
from ccheckout.ccheckout import process2, export_pdf, createPaymentCardsJSON, tPAccessToken, loadSecret, create_order
from cart import cart
from cart.models import DeliveryInfo
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
#from tienda.settings import API_CLIENT, API_SECRET
import hashlib
from .views import loadSecret
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.admin.views.decorators import staff_member_required
from registration.models import Profile
from contact.contact import notification_user_sale, notification_sale, notification_reserve

# Retorno del pago en Tropipay
@csrf_exempt
@require_http_methods(["POST"])
def payment_notification(request):
    #response = json.loads(request.__dict__()) #.raw_post_data
    #response2 = json.loads(str(request))
    #js = request.json()
    #response = json.loads(js)
    #status = json.loads(request.POST.get('status')) 
    #print(status)
    response = json.loads(request.body)
    #print(response)
    
    """ st = response["status"]
    print("response[status]")
    print(st) """

    print("response.get(status)")
    status = response.get("status")
    print(status)
    
    try:
        print(response.get("status") == 'OK')
        if response.get("status") == 'OK':
            print("Entró al if")
        
        data = response["data"]
        print(data)
        signature = data["signaturev2"]
        bankOrderCode = data["bankOrderCode"]
        creds = loadSecret()
        clientId = creds["client_id"]
        clientSecret = creds["client_secret"]
        originalCurrencyAmount = data["originalCurrencyAmount"]
        #print("CI: " + clientId)
        #print("CS: " + clientSecret)
        chekSignature = hashlib.sha256(str(bankOrderCode + clientId + clientSecret + originalCurrencyAmount).encode('utf-8'))
        #print("checked")
        encodehash = chekSignature.hexdigest()
        #print(encodehash)
        if signature == encodehash:
            #print("Confirmed")
            paymentcard = data["paymentcard"]
            order_number = paymentcard["reasonId"]
            #print(order_number)
            if order_number:
                order = get_object_or_404(Order, id=order_number) 
                order.status = Order.PROCESSED
                order.transaction_id = data["id"]
                order.save()
            else:
                print("Error al generar orden")
        else:
            print("No coinciden las firmas")
    except OSError:
        print("OSError --- status"+status)
   
    return request

# Donde redirecciona al usuario Tropipay después de pagar
def hit(request):
    order_number = request.session.get('order_number','')
    if order_number:
        order = Order.objects.filter(id=order_number)[0]
        if order.status == Order.PROCESSED: #SUBMITTED: # PROCESSED
            order.update_status(Order.PAIDED)
            order.save()
            receipt_url = reverse('checkout_receipt')
            return HttpResponseRedirect(receipt_url)
        else:
            fail_url = reverse('checkout_fail')
            return HttpResponseRedirect(fail_url)
    else:
        print("Error en el numero de la orden")

# El view de la página de pago
@login_required
def show_checkout(request, template_name='checkout/checkout.html'):
    MND = 'USD'
    if cart.is_empty(request):
        cart_url = reverse('show_cart')
        return HttpResponseRedirect(cart_url)
    if request.method == 'POST': 
        postdata = request.POST.copy()
        if postdata['submit'] == ' ':
            form = CheckoutForm(postdata)
            if form.is_valid():
                order_number = create_order(request, 2) 
                error_message = postdata.get('message','')
                if order_number['order_number'] == -1:
                    fail = reverse('show_cart')
                    return HttpResponseRedirect(fail)
                if order_number:
                    request.session['order_number'] = order_number['order_number']
                    response = createPaymentCardsJSON(request, order_number)
                    dicto = json.loads(response.content)
                    try:
                        url_pay = dicto["shortUrl"]
                        order = Order.objects.filter(id=order_number['order_number'])[0]
                        order.pay_url = url_pay
                        order.save()
                        order.update_status(order.PROCESSED)
                        order.save()
                        return HttpResponseRedirect(url_pay)
                    except Exception as e:
                        print(f"Error en: {e}")
                        if dicto["error"]["code"] in ["EXPIRED_TOKEN", "INVALID_CREDENTIAL", "FORBIDDEN_ERROR"]:
                            response = tPAccessToken()
                            dicto = json.loads(response.content)
                            creds = loadSecret()
                            creds["token"] = dicto.get('access_token')
                            #"Guardo el token actualizado en el fichero")
                            with open('secrets.txt', 'w') as archivo:
                                json.dump(creds, archivo)
                            #("Llamo por segunda vez al pago")
                            response2 = createPaymentCardsJSON(request, order_number)
                            try:
                                dicto2 = json.loads(response2.content)
                                url_pay = dicto2["shortUrl"]
                                order = Order.objects.filter(id=order_number['order_number'])[0]
                                order.pay_url = url_pay
                                order.save()
                                order.update_status(order.PROCESSED)
                                order.save()
                                return HttpResponseRedirect(url_pay)
                            except:
                                fail_url = reverse('checkout_fail')
                                return HttpResponseRedirect(fail_url)
                        else:
                            fail_url = reverse('checkout_fail')
                            return HttpResponseRedirect(fail_url)
            else:
                fail_url = reverse('checkout_fail')
                return HttpResponseRedirect(fail_url)
        """ else:
            form = CachForm(postdata)
            if form.is_valid():
                order_number = create_order(request, 1, True, True) # Crear la orden con tipo de transacción 1 usd en cach
                if order_number['order_number'] == -1:
                    fail = reverse('show_cart')
                    return HttpResponseRedirect(fail)
                error_message = postdata.get('message','')
                if order_number:
                    request.session['order_number'] = order_number['order_number']
                    order = Order.objects.filter(id=order_number['order_number'])[0]
                    order.transaction_id = 1 # 1 para pago en efectivo USD 
                    order.save()
                    order.update_status(Order.PAIDED)
                    order.update_status(Order.DELIVERED)
                    order.save()
                    receipt_url = reverse('checkout_receipt')
                    return HttpResponseRedirect(receipt_url) """
    else:
        form = CheckoutForm()
        form.name = request.user.first_name + request.user.last_name
    page_title = 'Checkout'
    cobra_efectivo = False
    cart_subtotal = cart.cart_subtotal(request)
    cart_delivery = cart.cart_delivery_price(request, cart_subtotal, MND)
    cart_total = cart_subtotal + cart_delivery
    st_name = cart.delivery_Store(request).name
    envio = False
    deli = cart.get_delivery(request)
    if deli == '3':
        envio = True 
    if (request.user.groups.filter(name='vendedor').exists() or request.user.is_superuser):
        cobra_efectivo = True
    return render(request, template_name, locals())

@login_required
def cach(request, template_name='checkout/cach.html'):
    MD = 'USD'
    if cart.is_empty(request):
        cart_url = reverse('show_cart')
        return HttpResponseRedirect(cart_url)
    if request.method == 'POST': 
        postdata = request.POST.copy()
        if postdata['submit'] == 'Confirmar pago':
            form = CachForm(postdata)
            if form.is_valid():
                user = request.user
                profile = get_object_or_404(Profile, user = user)
                MD = profile.MONEY_TYPE[profile.money_type][1]
                if MD == 'USD':
                    order_number = create_order(request, 1, True, True) # Crear la orden con tipo de transacción 1 usd en cach
                    if order_number['order_number'] == -1:
                        fail = reverse('show_cart')
                        return HttpResponseRedirect(fail)
                else:
                    order_number = create_order(request, 3, False, True)
                    if order_number['order_number'] == -1:
                        fail = reverse('show_cart')
                        return HttpResponseRedirect(fail)
                error_message = postdata.get('message','')
                if order_number:
                    request.session['order_number'] = order_number['order_number']
                    order = Order.objects.filter(id=order_number['order_number'])[0]
                    order.transaction_id = 1 # 1 para pago en efectivo USD 
                    order.save()
                    order.update_status(Order.PAIDED)
                    order.update_status(Order.DELIVERED)
                    order.save()
                    receipt_url = reverse('checkout_receipt')
                    return HttpResponseRedirect(receipt_url)
    else:
        form = CachForm()
        form.name = request.user.first_name + request.user.last_name
    page_title = 'Cach'
    cobra_efectivo = False
    cart_subtotal = round(cart.cart_subtotal(request), 2)
    cart_delivery = cart.cart_delivery_price(request, cart_subtotal, MD)
    cart_total = cart_subtotal + cart_delivery
    st_name = cart.delivery_Store(request).name
    envio = False
    deli = cart.get_delivery(request)
    if deli == '3':
        envio = True 
    if (request.user.groups.filter(name='vendedores').exists() or request.user.is_superuser):
        cobra_efectivo = True
    return render(request, template_name, locals())

# El view de la página de pago nacional
@login_required
def pagar(request, template_name='checkout/pagar.html'):
    MD = 'USD'
    if cart.is_empty(request):
        cart_url = reverse('show_cart')
        return HttpResponseRedirect(cart_url)
    if request.method == 'POST': 
        postdata = request.POST.copy()
        if postdata['submit'] == 'Efectuar pago':
            form = PagarForm(postdata)
            if form.is_valid():
                user = request.user
                profile = get_object_or_404(Profile, user = user)
                MD = profile.MONEY_TYPE[profile.money_type][1]
                order_number = create_order(request, 1, False, False) # Crear la orden con tipo de transacción 1 usd en cach
                if order_number['order_number'] == -1:
                    fail = reverse('show_cart')
                    return HttpResponseRedirect(fail)
                error_message = postdata.get('message','')
                if order_number:
                    request.session['order_number'] = order_number['order_number']
                    order = Order.objects.filter(id=order_number['order_number'])[0]
                    order.pay_url = order.get_transfer_pay_url()
                    order.update_status(Order.PROCESSED)
                    order.save()
                    pagarTransfer = order.pay_url #reverse(order.pay_url)
                    return HttpResponseRedirect(pagarTransfer)
    else:
        form = PagarForm()
        form.name = request.user.first_name + request.user.last_name
    page_title = 'Transfermovil'
    cobra_efectivo = False
    cart_subtotal = round(cart.cart_subtotal(request), 2)
    cart_delivery = cart.cart_delivery_price(request, cart_subtotal, MD)
    cart_total = cart_subtotal + cart_delivery
    st_name = cart.delivery_Store(request).name
    envio = False
    deli = cart.get_delivery(request)
    if deli == '3':
        envio = True 
    if (request.user.groups.filter(name='vendedor').exists() or request.user.is_superuser):
        cobra_efectivo = True
    return render(request, template_name, locals())

@login_required
def reserve(request, template_name='checkout/reserve.html'):
    MD = 'USD'
    if cart.is_empty(request):
        cart_url = reverse('show_cart')
        return HttpResponseRedirect(cart_url)
    if request.method == 'POST': 
        postdata = request.POST.copy()
        if postdata['submit'] == 'Reservar':
            form = ReserveForm(postdata)
            if form.is_valid():
                user = request.user
                profile = get_object_or_404(Profile, user = user)
                MD = profile.MONEY_TYPE[profile.money_type][1]
                order_number = create_order(request, 2, True, True) # Crear la orden con tipo de transacción 2(Reservar) usd en cach
                if order_number['order_number'] == -1:
                    fail = reverse('show_cart')
                    return HttpResponseRedirect(fail)
                error_message = postdata.get('message','')
                if order_number:
                    request.session['order_number'] = order_number['order_number']
                    order = Order.objects.filter(id=order_number['order_number'])[0]
                    print(f"Numero de orden: {order.pk}")
                    order.update_status(Order.PROCESSED)
                    order.save()
                    notification_user_sale(request)
                    notification_reserve(request)
                    receipt_url = order.get_paided_url()
                    return HttpResponseRedirect(receipt_url)
    else:
        form = ReserveForm()
        form.name = request.user.first_name + request.user.last_name
    page_title = 'Reservar'
    cobra_efectivo = False
    cart_subtotal = round(cart.cart_subtotal(request), 2)
    cart_delivery = cart.cart_delivery_price(request, cart_subtotal, MD)
    cart_total = cart_subtotal + cart_delivery
    st_name = cart.delivery_Store(request).name
    envio = False
    deli = cart.get_delivery(request)
    if deli == '3':
        envio = True 
    if (request.user.groups.filter(name='vendedor').exists() or request.user.is_superuser):
        cobra_efectivo = True
    return render(request, template_name, locals())

@login_required
def transfer(request, template_name='checkout/transfer.html', id=0):
    order = Order.objects.filter(id=id)[0]
    if request.method == 'POST': 
        postdata = request.POST.copy()
        if postdata['submit'] == 'Confirmar':
            if id == 0:
                order = Order.objects.filter(id=request.session['order_number'])[0]
            else:
                order = Order.objects.filter(id=id)[0]
            order.transaction_id = postdata['TransferId']
            order.update_status(Order.PAIDED)
            order.save()
            notification_user_sale(request)
            notification_sale(request)
            receipt_url = reverse('checkout_procesado')
            return HttpResponseRedirect(receipt_url)
    return render(request, template_name, locals())


# El view de la página de pago completado por plataforma internacional
@login_required
def receipt(request, template_name='checkout/receipt.html'):
    order_number = request.session.get('order_number','')
    order = Order.objects.filter(id=order_number)[0]
    if order_number and order.status == order.PAIDED:    
        order_items = OrderItem.objects.filter(order=order_number)
        orderN = order_number
        user = order.user
    else:
        cart_url = reverse('show_cart')
        return HttpResponseRedirect(cart_url)
    # Capturar el POST de un botón para generar pdf
    if request.method == 'POST':
        del request.session['order_number']
        return export_pdf(request, order_number)
    return render(request, template_name, locals())

# El view de la página de pago completado por transfermovil
@login_required
def confirmado(request, order_id, template_name='checkout/confirmado.html'):
    #order_number = request.session.get('order_number','')
    order = Order.objects.filter(id=order_id)[0]
    order_number = order.id
    if order.status == order.PROCESSED or order.status == order.PAIDED:    
        order_items = OrderItem.objects.filter(order=order_number)
        orderN = order_number
        user = order.user
    else:
        cart_url = reverse('show_cart')
        return HttpResponseRedirect(cart_url)
    # Capturar el POST de un botón para generar pdf
    if request.method == 'POST':
        del request.session['order_number']
        return export_pdf(request, order_number)
    user = request.user
    profile = get_object_or_404(Profile, user = user)
    MND = profile.MONEY_TYPE[profile.money_type][1]
    cart_subtotal = round(cart.cart_subtotal(request), 2)
    cart_delivery = cart.cart_delivery_price(request, cart_subtotal, MND)
    cart_total = cart_subtotal + cart_delivery
    st_name = cart.delivery_Store(request).name
    envio = False
    deli = cart.get_delivery(request)
    if deli == '3':
        envio = True
    return render(request, template_name, locals())

# El view de la lista de órdenes (compras) realizadas por el usuario
@login_required
def orders_list(request, template_name='checkout/orders_list.html'):
    if request.method == 'POST':
        postdata = request.POST.copy()
        if postdata['submit'] == 'Factura':
            order_number = postdata['order_id']
            return export_pdf(request, order_number)
    orders = Order.objects.filter(user=request.user)
    user_name = request.user.first_name + " " + request.user.last_name
    return render(request, template_name, locals())

# view de la lista de ordenes (compras) relizadas a la tienda
def admin_orders_list(request, template_name='checkout/orders_list.html'):
    if request.method == 'POST':
        postdata = request.POST.copy()
        if postdata['submit'] == 'Factura':
            order_number = postdata['order_id']
            return export_pdf(request, order_number)
        if postdata['submit'] == 'Detalles':
            order_id = postdata['order_id']
            template = 'checkout/details.html'
            return redirect(reverse('details'))
        return HttpResponseRedirect(receipt)
    orders = Order.objects.all()
    user_name = ""
    return render(request, template_name, locals())

# view de la página que se visualiza al usuario cuando hubo algún problema en el pago desde la pasarela.
def fail(request, template_name='checkout/fail.html'):
    order_number = request.session.get('order_number','')
    order = Order.objects.filter(id=order_number)[0]
    if order:
        order.status = Order.CANCELLED
        order.save()    
    return render(request, template_name, locals())

@login_required
def details(request, order_id, template_name='checkout/details.html'):
    order = Order.objects.filter(id=order_id)[0]
    subtotal = order.total - order.delivery_price    
    order_items = OrderItem.objects.filter(order=order_id)
    orderN = order_id
    user = order.user
    # Capturar el POST de un botón para generar pdf
    if request.method == 'POST':
        postdata = request.POST.copy()
        if postdata['submit'] == 'Generar Factura':
            return export_pdf(request, order_id)
        elif postdata['submit'] == 'Actualizar':
            form = UpdateStatusForm(request.POST)
            status = int(postdata['status'])
            order.update_status(status)
            order.save()
    else:
        form = UpdateStatusForm()
    return render(request, template_name, locals())

@login_required
def transfer_pay(request, order_id, template_name='checkout/transfer.html'):
    order = Order.objects.filter(id=order_id)[0]
    subtotal = order.total - order.delivery_price    
    order_items = OrderItem.objects.filter(order=order_id)
    orderN = order_id
    user = order.user
    if request.method == 'POST': 
        postdata = request.POST.copy()
        print(postdata)
        print(order_id)
        if postdata['submit'] == 'Confirmar':
            if order_id == 0:
                order = Order.objects.filter(id=request.session['order_number'])[0]
            else:
                order = Order.objects.filter(id=order_id)[0]
            order.transaction_id = postdata['TransferId']
            order.update_status(Order.PAIDED)
            order.save()
            notification_user_sale(request)
            notification_sale(request)
            receipt_url = order.get_paided_url()
            return HttpResponseRedirect(receipt_url)
    return render(request, template_name, locals())