from django.contrib import admin
from cart.models import CartItem

class CartItemAdmin(admin.ModelAdmin):
    list_per_page = 20

admin.site.register(CartItem, CartItemAdmin)