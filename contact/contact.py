from django.core.mail import EmailMessage
from django.core.mail import send_mail
from tienda.settings import EMAIL_HOST_USER
from tienda.settings import EMAIL_RECEIPT
from ccheckout.models import Order

def notification_user_sale(request):
    name = request.user.first_name
    email = request.user.email
    subject = "Gracias por preferir nuestros productos. MUHIA es más que una solución"
    order_number = request.session.get('order_number','')
    if order_number:
        order = Order.objects.filter(id=order_number)[0]
    url_order = "http://127.0.0.1:8000/compra/compras/{}/".format(order.id)
    content = "Los detalles de su orden puede consultarlo en {}".format(url_order)
    e_mail = EmailMessage(
        subject,
        "Estimado {}: \n\n{}".format(name, content),
        EMAIL_HOST_USER, # Correo servidor
        [email] # Para quien va el mensaje
        )
    try:
        e_mail.send()
    except:
        pass

def notification_sale(request):
    name = request.user.first_name
    email = "ycoca@produccionesmuhia.ca"
    order_number = request.session.get('order_number','')
    if order_number:
        order = Order.objects.filter(id=order_number)[0]
    subject = "El usuario {} ha realizado la compra número {}".format(name, order.id)
    content = " El monto de la compra es: {} {} \n El número de transacción es: {}".format(order.total, order.currency, order.transaction_id)
    e_mail = EmailMessage(
        subject,
        "Estimado {}: \n\n{}".format(name, content),
        EMAIL_HOST_USER, # Correo servidor
        [email] # Para quien va el mensaje
        )
    try:
        e_mail.send()
    except:
        pass

def notification_reserve(request):
    name = "Juani"
    email = "ycoca@produccionesmuhia.ca"
    email2 = "ycocab@gmail.com"
    order_number = request.session.get('order_number','')
    if order_number:
        order = Order.objects.filter(id=order_number)[0]
    subject = "El usuario {} ha realizado la reservación con orden número {}".format(name, order.id)
    content = " El monto es de: {} {} ".format(order.total, order.currency)
    e_mail = EmailMessage(
        subject,
        "Estimado {}: \n\n{}".format(name, content),
        EMAIL_HOST_USER, # Correo servidor
        [email] # Para quien va el mensaje
        )
    e_mail2 = EmailMessage(
        subject,
        "Estimado {}: \n\n{}".format("ycocab", content),
        EMAIL_HOST_USER, # Correo servidor
        [email2] # Para quien va el mensaje
        )
    try:
        e_mail.send()
        e_mail2.send()
    except:
        pass
