from django.shortcuts import render
from django.shortcuts import get_object_or_404
from catalog.models import Category, Product
from django.template import RequestContext
from django.urls import reverse
from cart import cart
from django.http import HttpResponseRedirect
from catalog.forms import ProductAddToCartForm
from stores.models import Store, Product_Sales
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def index(request, template_name="index.html"):
    context = {'name':'Tienda Virtual MUHIA'}
    return render(request, template_name, context)

def show_category(request, category_slug, template_name="catalog/category.html"):
    c = get_object_or_404(Category, slug=category_slug)
    products = c.product_set.all()
    page_title = c.name
    meta_keywords = c.meta_keywords
    meta_description = c.meta_description
    product = get_object_or_404(Product, pk=1)

    # Add to cart
    """     if request.method == 'POST':
        try:
            postdata = request.POST.copy()
            if postdata['submit'] == 'Carrito':
                form = ProductAddToCartForm(request, postdata)
                form.quantity = postdata['quantity']
                #check if posted data is valid
                if form.is_valid():
                    #add to cart and redirect to cart page 
                    cart.add_to_cart(request)
                    # if test cookie worked, get rid of it
                    if request.session.test_cookie_worked():
                        request.session.delete_test_cookie()
                    url = reverse('show_cart')
                    return HttpResponseRedirect(url)
                else:
                    print(form.errors.as_data)
            else:
                form = ProductAddToCartForm(request=request)
                # assign the hidden input the product slug
                form.fields['product_slug'].widget.attrs['value'] = product_slug
                quantity = postdata['quantity']
                form.fields['quantity'].widget.attrs['value'] = postdata['quantity']
        except Exception:
            print("Error en el envío de información")
    else:
        # it’s a GET, create the unbound form. Note request as a kwarg
        print("No POST")
    form = ProductAddToCartForm(request=request)
    # assign the hidden input the product slug
    form.fields['product_slug'].widget.attrs['value'] = product_slug
    form.fields['quantity'].widget.attrs['value'] = quantity
    # set the test cookie on our first GET request
    request.session.set_test_cookie() """
    return render(request, template_name, locals())

def show_categories(request, template_name="catalog/categories.html"):

    return render(request, template_name, locals())

def validateCount(postdata, products_stores):
    dely = postdata['delivery_type']
    s = get_object_or_404(Store, pk=dely)
    for ps in products_stores:
        if ps.store.slug == s.slug:
            if int(postdata['quantity']) > ps.available:
                return False
            return True
    return False

def get_Product_Store(postdata, products_stores):
    dely = postdata['delivery_type']
    s = get_object_or_404(Store, pk=dely)
    for ps in products_stores:
        if ps.store.slug == s.slug:
            return ps
    return 0

# new product view, with POST vs GET detection
def show_product(request, product_slug, template_name="catalog/product.html"):
    p = get_object_or_404(Product, slug=product_slug)    
    products_stores = Product_Sales.objects.filter(product=p)
    categories = p.categories.all()
    page_title = p.name
    meta_keywords = p.meta_keywords
    meta_description = p.meta_description
    quantity = 1
    delivery = 1
    # need to evaluate the HTTP method
    if request.method == 'POST':
        try:
            postdata = request.POST.copy()
            """             form = ProductAddToCartForm(request=request)
            # assign the hidden input the product slug
            form.fields['product_slug'].widget.attrs['value'] = product_slug
            quantity = postdata['quantity']
            form.fields['quantity'].widget.attrs['value'] = postdata['quantity'] """
            print(postdata)
            if postdata['submit'] == 'Comprar':
                ps = get_Product_Store(postdata, products_stores)
                if not(validateCount(postdata, products_stores)):
                    print("No valida la cantidad ")
                    messages.warning(request, "Está solicitando más cantidad de la disponible para ese tipo de entrega")
                else:
                    form = ProductAddToCartForm(request, postdata)
                    form.quantity = postdata['quantity']
                    form.delivery_type = postdata['delivery_type']
                    #check if posted data is valid """
                    if form.is_valid():
                        #add to cart and redirect to cart page 
                        cart.add_to_cart(request)
                        # if test cookie worked, get rid of it
                        if request.session.test_cookie_worked():
                            request.session.delete_test_cookie()
                        url = reverse('show_cart')
                        return HttpResponseRedirect(url)
                    else:
                        messages.error(request,form.errors.as_data)
            else:
                form = ProductAddToCartForm(request=request)
                # assign the hidden input the product slug
                form.fields['product_slug'].widget.attrs['value'] = product_slug
#                form.fields['delivery_type'].widget.attrs['value'] = 'EnvioHabana'
                quantity = postdata['quantity']
                delivery = postdata['delivery_type']
                form.fields['quantity'].widget.attrs['value'] = postdata['quantity']
                form.fields['delivery_type'].widget.attrs['value'] = postdata['delivery_type']
        except Exception:
            messages.error(request,"Error desconocido en el envío de información")
    form = ProductAddToCartForm(request=request)
    # assign the hidden input the product slug
    form.fields['product_slug'].widget.attrs['value'] = product_slug
    #print(postdata)
    #... valores = mismafunción.widget.attrs['value']
    form.fields['quantity'].widget.attrs['value'] = quantity
    # set the test cookie on our first GET request
    request.session.set_test_cookie()
    return render(request, template_name, locals())
