from cart.models import CartItem
from catalog.models import Product
from stores.models import Store
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from cart import cart
from stores.models import Product_Sales
from registration.models import Profile

import decimal
import random

# not needed yet but we will later
CART_ID_SESSION_KEY = 'cart_id'
SESSION_DELIVERY = 'delivery'

# Pedir el delivery  por defecto envio habana pk = 3
def get_delivery(request, delivery='3'):
    if request.session.get(SESSION_DELIVERY,'') == '':
        request.session[SESSION_DELIVERY] = delivery
    return request.session[SESSION_DELIVERY]

# Asignar el delivery por defecto envio habana pk = 3
def set_delivery(request, delivery='3'):
    request.session[SESSION_DELIVERY] = delivery

# get the current user's cart id, sets new one if blank
def _cart_id(request):
    if request.session.get(CART_ID_SESSION_KEY,'') == '':
        request.session[CART_ID_SESSION_KEY] = _generate_cart_id()
    return request.session[CART_ID_SESSION_KEY]

def _generate_cart_id():
    cart_id = ''
    characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()'
    cart_id_length = 50
    for y in range(cart_id_length):
        cart_id += characters[random.randint(0, len(characters)-1)]
    return cart_id

# return all items from the current user's cart
def get_cart_items(request):
    return CartItem.objects.filter(cart_id=_cart_id(request))

def get_stores(request):
    return Store.objects.all()

def get_Product_Store(request, product_slug, dely='3'):
    p = get_object_or_404(Product, slug=product_slug)    
    products_stores = Product_Sales.objects.filter(product=p)
    s = get_object_or_404(Store, pk=dely)
    for ps in products_stores:
        if ps.store.slug == s.slug:
            return ps
    return 0

def delivery_Store(request):
    delivery = get_delivery(request)
    s = get_object_or_404(Store, pk=delivery)
    return s
    
def delivery_name(request):
    delivery = get_delivery(request)
    s = get_object_or_404(Store, pk=delivery)
    return s.name

# add an item to the cart
def add_to_cart(request, p_slug, quantity=1):
    postdata = request.POST.copy()
    p = get_object_or_404(Product, slug=p_slug)
    cart_products = get_cart_items(request)
    product_in_cart = False
    # check to see if item is already in cart
    for cart_item in cart_products:
        if cart_item.product.id == p.id:
            # update the quantity if found
            cart_item.augment_quantity(quantity)
            product_in_cart = True
    if not product_in_cart:
        # create and save a new cart item
        ci = CartItem()
        ci.product = p
        ci.quantity = quantity
        ci.cart_id = _cart_id(request)
        ci.save()
    delivery = cart.get_delivery(request)
    if p.set_reserved(quantity):
        p.save()
        return True
    return False 

# returns the total number of items in the user's cart
def cart_distinct_item_count(request):
    return get_cart_items(request).count()

def get_single_item(request, item_id):
    return get_object_or_404(CartItem, id=item_id, cart_id=_cart_id(request))

# update quantity for single item
def update_cart(request):
    postdata = request.POST.copy()
    item_id = postdata['item_id']
    quantity = postdata['quantity']
    cart_item = get_single_item(request, item_id)
    if cart_item:
        if int(quantity) != cart_item.quantity:
            dif = int(quantity) - cart_item.quantity
            cart_item.quantity = int(quantity)
            cart_item.product.set_reserved(dif)
            cart_item.product.save()
            cart_item.save()
        else:
            remove_from_cart(request)

# remove a single item from cart Rvisar porue ya actulice productos por otra parte creo
def remove_from_cart(request):
    postdata = request.POST.copy()
    item_id = postdata['item_id']
    quantity = postdata['quantity']
    cart_item = get_single_item(request, item_id)
    if cart_item:
        prod = cart_item.product
        prod.set_reserved(int(quantity))
        prod.save()
        cart_item.delete()

# gets the total cost for the current cart
def cart_subtotal(request):
    cart_total = decimal.Decimal('0.00')
    cart_products = get_cart_items(request)
    user = request.user
    MND = 'USD'
    if (user.is_authenticated):
        profile = get_object_or_404(Profile, user = user)
        MND = profile.MONEY_TYPE[profile.money_type][1] 
    for cart_item in cart_products:
            cart_total += cart_item.product.get_price(MND) * cart_item.quantity
    return cart_total

def cart_delivery_price(request):
    cart_delivery = decimal.Decimal('0.00')
    cart_products = get_cart_items(request)
    stores = get_stores(request)
    MND = 'USD'
    user = request.user
    if (user.is_authenticated):
        profile = get_object_or_404(Profile, user = user)
        MND = profile.MONEY_TYPE[profile.money_type][1]
    for s in stores:
        if s == cart.delivery_Store(request):
            if MND == 'USD':
                cart_delivery = cart_delivery + decimal.Decimal(s.price_usd)
            elif MND == 'CUP':
                cart_delivery = cart_delivery + decimal.Decimal(s.price_cup)
            else:
                cart_delivery = cart_delivery + decimal.Decimal(s.price_mlc)
            break
    return cart_delivery

def is_empty(request):
    return cart_distinct_item_count(request) == 0

def empty_cart(request):
    user_cart = get_cart_items(request)
    request.session[SESSION_DELIVERY] = ''    
    user_cart.delete()
