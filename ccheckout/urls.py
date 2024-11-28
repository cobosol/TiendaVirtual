from django.urls import path, re_path
from . import views

urlpatterns = [
    path("", views.show_checkout, name='checkout'),
    path("pagar/", views.pagar, name='pagar'),
    path("transfer/", views.transfer, name='transfer'), 
    path("efectivo/", views.cach, name='efectivo'),    
    path("recibo/", views.receipt, name='checkout_receipt'),
    path("procesado/<order_id>/", views.confirmado, name='checkout_procesado'),
    path('pdf/', views.export_pdf, name='export_pdf'),
    path("fallo/", views.fail, name='checkout_fail'),
    path("exito/", views.hit, name='checkout_hit'),
    path("compras/", views.orders_list, name='orders_list'),
    path("compras/<order_id>/", views.details, name='details'),
    path("transfer/<order_id>/", views.transfer_pay, name='transfer_pay'),
    path("notification/", views.payment_notification, name='notification'),
    path("gestion/", views.admin_orders_list, name='admin_orders_list'),
]
