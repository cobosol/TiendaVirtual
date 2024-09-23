from django.contrib import admin
from .models import Banner

class BannerAdmin(admin.ModelAdmin):
    pass

admin.site.register(Banner, BannerAdmin)