from django.contrib import admin
from utils.models import Price

class PriceAdmin(admin.ModelAdmin):
    pass

admin.site.register(Price, PriceAdmin)