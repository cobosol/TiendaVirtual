from django.contrib import admin
from .models import Order, OrderItem
#, DeliveryType

class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ('__unicode__','date','status','transaction_id','user')
    list_filter = ('status','date')
    search_fields = ('email', 'delivery_ci', 'delivery_name', 'id','transaction_id')
    inlines = [OrderItemInline,]
    fieldsets = (('Basics', {'fields': ('user','status','email','phone')}),
                 ('Delivery', {'fields':('delivery_name','delivery_address_1','delivery_address_2','delivery_state', 'delivery_price')})
                 )

""" class DeliveryTypeAdmin(admin.ModelAdmin):
    model = DeliveryType """

admin.site.register(Order, OrderAdmin)
#admin.site.register(DeliveryType, DeliveryTypeAdmin)
