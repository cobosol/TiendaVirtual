from django.urls import path, re_path
from . import views

urlpatterns = [
    path("", views.show_checkout, name='checkout'),
    path("recibo/", views.receipt, name='checkout_receipt'),
    path('pdf/', views.export_pdf, name='export_pdf'),
    path("fallo/", views.fail, name='checkout_fail'),
    path("exito/", views.hit, name='checkout_hit'),
    path("exitoStripe/", views.hitS, name='checkout_hit2'),
    path("compras/", views.orders_list, name='orders_list'),
    path("notification/", views.payment_notification, name='notification'),
    path("gestion/", views.admin_orders_list, name='admin_orders_list'),
]
