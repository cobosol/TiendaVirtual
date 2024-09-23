from django.contrib import admin
from registration.models import Profile
from registration.forms import ProfileForm

class ProfileAdmin(admin.ModelAdmin):
    pass

admin.site.register(Profile, ProfileAdmin)