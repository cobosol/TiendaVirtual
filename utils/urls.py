from django.urls import path, re_path
from .views import gestion_precios, eliminar_precio, crear_precio, actualizar_precio
#from ppreview import views

urlpatterns =[
    path('', gestion_precios.as_view( template_name="utils/precio_admin.html"), name='precios'),
    path('eliminar/<int:pk>', eliminar_precio.as_view(), name='eliminar_precio'),
    path('crear', crear_precio.as_view(template_name = "utils/precio_crear.html"), name='crear_precio'),
    path('editar/<int:pk>', actualizar_precio.as_view(template_name = "utils/precio_actualizar.html"), name='actualizar_producto'),
]