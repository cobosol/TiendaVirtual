from django.urls import path, re_path
from . import views

urlpatterns = [
    path("carrito/", views.show_cart, name='show_cart'),
]
