from django.shortcuts import render
from .models import Store
from django.shortcuts import get_object_or_404

def show_stores(request, template_name="stores/stores.html"):
    stores = Store.objects.all()
    return render(request, template_name, locals())

def show_store(request, store_slug, template_name="stores/store.html"):
    store = get_object_or_404(Store, slug=store_slug)
    print(store_slug)
    address = store.address
    hours = store.hours
    image = store.get_image_url
    return render(request, template_name, locals())
