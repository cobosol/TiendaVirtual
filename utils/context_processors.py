from django.shortcuts import render, redirect, get_object_or_404
from catalog.models import Category
from tienda import settings
from registration.models import Profile
from stores.models import Store

def tienda_generales(request):
    user = request.user
    MND = 'USD'
    distribuidor = 'False'
    productor = 'False'
    user = request.user
    marketing = 'False'
    adminAccess = 'False'
    comercial = 'False'
    vendedor = 'False'
    stores = Store.objects.all()
    if user.is_authenticated:
        profile = get_object_or_404(Profile, user = user)
        if user.groups.filter(name__in=['vendedores']):
            vendedor = 'True'
            adminAccess = 'True'
        if user.groups.filter(name__in=['marketing']):
            marketing = 'True'
            adminAccess = 'True'
        if user.groups.filter(name__in=['comercial']):
            comercial = 'True'
            adminAccess = 'True'
        MND = profile.MONEY_TYPE[profile.money_type][1]
        #TU = profile.CLIENT_TYPE[profile.client_type][1] 
    categories = Category.objects.filter(is_active=True)
    if not categories.exists():
        categories = None
    return {
        'active_categories': categories,
        'stores': stores,
        'vendedor': vendedor,
        'distribuidor' : distribuidor,
        'productor' : productor,
        'user' : request.user,
        'marketing' : marketing,
        'adminAccess' : adminAccess,
        'comercial' : comercial, 
        'MND': MND,
        'site_name': settings.SITE_NAME,
        'meta_keywords': settings.META_KEYWORDS,
        'meta_description': settings.META_DESCRIPTION,
        'request': request
        }
