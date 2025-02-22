from django.urls import path
from . import views
from promo.views import gestion_banners, eliminar_banner, crear_banner, actualizar_banner, gestion_offers, eliminar_offer, crear_offer, actualizar_offer

urlpatterns = [
    #path('', views.banner, name="banners"),
    path('banners', gestion_banners.as_view( template_name="promo/banners_admin.html"), name='banners'),
    path('banner/eliminar/<int:pk>', eliminar_banner.as_view(), name='eliminar_banner'),
    path('banner/crear', crear_banner.as_view(template_name = "promo/banner_crear.html"), name='crear_banner'),
    path('banner/editar/<int:pk>', actualizar_banner.as_view(template_name = "promo/banner_actualizar.html"), name='actualizar_banner'),
    path('offers', gestion_offers.as_view( template_name="promo/offer_admin.html"), name='offers'),
    path('offer/eliminar/<int:pk>', eliminar_offer.as_view(), name='eliminar_offer'),
    path('offer/crear', crear_offer.as_view(template_name = "promo/offer_crear.html"), name='crear_offer'),
    path('offer/editar/<int:pk>', actualizar_offer.as_view(template_name = "promo/offer_actualizar.html"), name='actualizar_banner'),
]