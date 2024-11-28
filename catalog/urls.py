from django.urls import path, re_path
from . import views
from catalog.views import show_search, gestion_productos,eliminar_producto,crear_producto,actualizar_producto, gestion_productos_almacen,eliminar_producto_almacen,crear_producto_almacen,actualizar_producto_almacen
from . import views
#from ppreview import views

urlpatterns = [
    path("", views.index, name='catalog_home'),
    path("categorias/", views.show_categories, name='catalog_categories'),
    path("categoria/<category_slug>/", views.show_category, name='catalog_category'),
    path("producto/<product_slug>/", views.show_product, name='catalog_product'),
    path("productos/<productSearch>/", views.show_search, name='product_search'),
    path('gestion/', views.i_admin, name='gestion'),
    path('productos/', gestion_productos.as_view( template_name="catalog/products_admin.html"), name='productos'),
    path('productos/eliminar/<int:pk>', eliminar_producto.as_view(), name='eliminar_producto'),
    path('productos/crear', crear_producto.as_view(template_name = "catalog/producto_crear.html"), name='crear_producto'),
    path('productos/editar/<int:pk>', actualizar_producto.as_view(template_name = "catalog/producto_actualizar.html"), name='actualizar_producto'),
    #path('productos_almacen/', gestion_productos_almacen.as_view( template_name="catalog/productos_almacen_admin.html"), name='productos_almacen'),
    path('productos_almacen/', views.gestion_productos_almacen, name='productos_almacen'),
    path('productos_almacen/eliminar/<int:pk>', eliminar_producto_almacen.as_view(), name='eliminar_producto_almacen'),
    path('productos_almacen/crear', crear_producto_almacen.as_view(template_name = "catalog/producto_almacen_crear.html"), name='crear_producto_almacen'),
    path('productos_almacen/editar/<int:pk>', actualizar_producto_almacen.as_view(template_name = "catalog/producto_almacen_actualizar.html"), name='actualizar_producto_almacen'),
]
