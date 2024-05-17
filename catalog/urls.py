from django.urls import path, re_path
from . import views
#from ppreview import views

urlpatterns = [
    path("", views.index, name='catalog_home'),
    path("categorias/", views.show_categories, name='catalog_categories'),
    path("categoria/<category_slug>/", views.show_category, name='catalog_category'),
    path("producto/<product_slug>/", views.show_product, name='catalog_product'),
]
