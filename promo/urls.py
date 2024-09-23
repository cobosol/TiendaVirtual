from django.urls import path
from . import views
from promo.views import gestion_banners, eliminar_banner, crear_banner, actualizar_banner

urlpatterns = [
    #path('', views.banner, name="banners"),
    path('banners', gestion_banners.as_view( template_name="promo/banners_admin.html"), name='banners'),
    path('banner/eliminar/<int:pk>', eliminar_banner.as_view(), name='eliminar_banner'),
    path('banner/crear', crear_banner.as_view(template_name = "promo/banner_crear.html"), name='crear_banner'),
    path('banner/editar/<int:pk>', actualizar_banner.as_view(template_name = "promo/banner_actualizar.html"), name='actualizar_banner'),
 
]