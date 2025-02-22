from django.contrib import admin
from .models import Banner, Offer

class BannerAdmin(admin.ModelAdmin):
    pass

class OfferAdmin(admin.ModelAdmin):
    pass

admin.site.register(Banner, BannerAdmin)

admin.site.register(Offer, OfferAdmin)