from django.shortcuts import render, redirect
from .forms import ContactForm
from django.urls import reverse
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from tienda.settings import EMAIL_HOST_USER
from tienda.settings import EMAIL_RECEIPT

def contact(request):
    contact_form = ContactForm 
    if request.method == "POST":
        contact_form = contact_form(data=request.POST)
        if contact_form.is_valid:
            name = request.POST.get('name', '')
            email = request.POST.get('email', '')
            content = request.POST.get('content', '')
            e_mail = EmailMessage(
                "MUHIA: Nuevo mensaje de la tienda",
                "De {} <{}>\n\n{}".format(name, email, content),
                EMAIL_HOST_USER,
                [EMAIL_RECEIPT]
            )
            subject = "MUHIA: Nuevo mensaje de la tienda"
            try:
                print("A enviar")
                e_mail.send()
                #send_mail(subject = subject, message = content, from_email = 'ycoca@produccionesmuhia.ca', recipient_list = ["informatica@produccionesmuhia.ca", "ycocab@gmail.com", "ycoca@uci.cu"], fail_silently = False, auth_user = 'ycoca@produccionesmuhia.ca', auth_password = 'TestingCorreo2024++', connection = 'produccionesmuhia.ca:465')
                #send_mail(subject, content, email, ['ycoca@produccionesmuhia.ca'], auth_user = 'tienda@produccionesmuhia.ca', auth_password = '', connection = 'produccionesmuhia.ca:465')
                
                """          EmailMessage('Contact Form Submission from {}'.format(name),content,'informatica@produccionesmuhia.ca',
                             ['ycoca@produccionesmuhia.ca'],[],reply_to=[email]).send() """
                print("enviado")
                return redirect(reverse('contact') + "?ok")
            except:
                return redirect(reverse('contact') + "?fail")
    return render(request, "contact/contactos.html", {'form':contact_form})
