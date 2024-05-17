from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_stores, name="stores"),
    path("<store_slug>/", views.show_store, name='store'),
]
