from django.contrib import admin
from .models import Order, OrderItem
#, DeliveryType

class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ('__unicode__','date','status','transaction_id','user')
    list_filter = ('status','date')
    search_fields = ('delivery_email', 'delivery_ci', 'delivery_name', 'id','transaction_id')
    inlines = [OrderItemInline,]
    fieldsets = (('Comprador', {'fields': ('user','status','payment_email','payment_phone', 'pay_url')}),
                 ('Entrega', {'fields':('delivery_name','delivery_address_1','delivery_address_2','delivery_state', 'delivery_price')})
                 )

admin.site.register(Order, OrderAdmin)
