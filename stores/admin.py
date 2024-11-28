from django.contrib import admin
from .models import Store, Product_Sales

class StoreAdmin(admin.ModelAdmin):
    pass

class ProductSalesAdmin(admin.ModelAdmin):
    pass

admin.site.register(Product_Sales, ProductSalesAdmin)
admin.site.register(Store, StoreAdmin)
