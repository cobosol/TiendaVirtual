from django.shortcuts import render, redirect, get_object_or_404
from catalog.models import Category
from tienda import settings
from registration.models import Profile

def tienda_generales(request):
    user = request.user
    MND = 'USD'
    TU = 'Comprador'
    if user.is_authenticated:
        profile = get_object_or_404(Profile, user = user)
        MND = profile.MONEY_TYPE[profile.money_type][1]
        TU = profile.CLIENT_TYPE[profile.client_type][1] 
    categories = Category.objects.filter(is_active=True)
    if not categories.exists():
        categories = None
    return {
        'active_categories': categories,
        'MND': MND,
        'TU': TU,
        'site_name': settings.SITE_NAME,
        'meta_keywords': settings.META_KEYWORDS,
        'meta_description': settings.META_DESCRIPTION,
        'request': request
        }
