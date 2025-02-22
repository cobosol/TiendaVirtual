from cart.models import CartItem
from catalog.models import Product
from stores.models import Store
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from cart import cart
from cart.models import DeliveryInfo
from stores.models import Product_Sales, Store
from registration.models import Profile
from utils.models import Price
from django.contrib import messages

import decimal
import random

# not needed yet but we will later
CART_ID_SESSION_KEY = 'cart_id'
SESSION_DELIVERY = 'delivery'

# Pedir el delivery por defecto envio habana pk = 3
def get_delivery(request, delivery='3'):
    if request.session.get(SESSION_DELIVERY,'') == '':
        if request.user.is_authenticated:
            user = request.user
            profile = get_object_or_404(Profile, user = user)
            #print(profile.prefered_store)
            store = profile.prefered_store
            if (store):
                set_delivery(request, str(store.pk))
            else:
                set_delivery(request, str(3))
        else:
           set_delivery(request, delivery)
           #request.session[SESSION_DELIVERY] = delivery
    try:
        deliveryInfo = get_object_or_404(DeliveryInfo, client=request.user)
    except:
        deliveryInfo = DeliveryInfo()
        deliveryInfo.client = request.user
        deliveryInfo.storeDelivery = get_object_or_404(Store, pk=delivery)
        deliveryInfo.deliveryZone = 0
        deliveryInfo.save() 
    return request.session[SESSION_DELIVERY]

# Asignar el delivery por defecto envio habana pk = 3
def set_delivery(request, delivery, zone=0):
    request.session[SESSION_DELIVERY] = delivery
    deliveryInfo = get_object_or_404(DeliveryInfo, client=request.user)
    deliveryInfo.deliveryZone = zone
    deliveryInfo.save()



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

def verify_cart_items(request):
    cartItems = CartItem.objects.filter(cart_id=_cart_id(request))
    for item in cartItems:
        disp = item.product.count - item.product.reserved
        if item.quantity >= disp:
            text = "Ya no hay esa disponibilidad para el producto {}.".format(item.product.name)
            messages.warning(request, text)
            return False
    return True


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

""" def discount_message(request):
    item_id = postdata['item_id']
    cart_item = cart.get_single_item(request, item_id)
    print(item_id)
    to_whole = price.min_quantity_whole - quantity
    product = cart_item.product.gname
    text = "Te faltan " + str(to_whole) + " de " + str(product) + " para nuestros descuentos mayoristas"
     """

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
    if request.user.is_authenticated:
        """ messages.warning(request, "Advertencia")
        messages.error(request, "Error")
        messages.info(request, "Info")
        messages.success(request, "Exito") """
        postdata = request.POST.copy()
        p = get_object_or_404(Product, slug=p_slug)
        cart_products = get_cart_items(request)
        product_in_cart = False
        # check to see if item is already in cart
        for cart_item in cart_products:
            if cart_item.product.id == p.id:
                # update the quantity if found
                if not cart_item.augment_quantity(quantity):
                    messages.warning(request, "No hay más disponibilidad del producto")
                else:
                    messages.success(request, f"Incrementó la cantidad del producto {p.name} en el carrito")
                product_in_cart = True
        if not product_in_cart: #
            # create and save a new cart item
            if p.count >= decimal.Decimal(quantity):
                ci = CartItem()
                ci.product = p
                ci.quantity = quantity
                ci.cart_id = _cart_id(request)
                ci.save()
                delivery = cart.get_delivery(request)
                p.save()
                messages.success(request, "Producto adicionado correctamente al carrito")
                return True
            else:
                messages.warning(request, "No existe esa disponibilidad del producto")
                return False
        else:
            return True
    else:
        messages.error(request, "Debe estar autenticado para efectuar compras")
        url = '/accounts/login/'
        return HttpResponseRedirect(url)       

# returns the total number of items in the user's cart
def cart_distinct_item_count(request):
    return get_cart_items(request).count()

def get_single_item(request, item_id):
    return get_object_or_404(CartItem, id=item_id, cart_id=_cart_id(request))

# update quantity for single item
def update_cart(request):
    if request.user.groups.filter(name__in=['vendedores', 'comercial']):
        postdata = request.POST.copy()
        item_id = postdata['item_id']
        quantity = postdata['quantity']
        cart_item = get_single_item(request, item_id)
        if cart_item:
            try:
                if decimal.Decimal(quantity) != decimal.Decimal(cart_item.quantity):
                    #dif = int(quantity) - cart_item.quantity
                    if cart_item.product.count >= decimal.Decimal(quantity):
                        cart_item.quantity = decimal.Decimal(quantity)
                        #cart_item.product.save()
                        cart_item.save()
                    else:
                        text = "No existe esa cantidad del producto {}.".format(cart_item.product.name)
                        messages.warning(request, text)
                        return False
            except:
                text = "Error en el formato de la cantidad del producto {}.".format(cart_item.product.name)
                messages.error(request, text)
                return False
        try:
            if decimal.Decimal(quantity) <= 0:
                remove_from_cart(request)
            return cart_item.quantity
        except:
            text = "Error al eliminar del carrito el producto {}.".format(cart_item.product.name)
            messages.info(request, text)
    else:
        postdata = request.POST.copy()
        item_id = postdata['item_id']
        quantity = postdata['quantity']
        int_quantity = int(quantity)
        if int(quantity) - int_quantity == 0:
            cart_item = get_single_item(request, item_id)
            if cart_item:
                if int(quantity) != cart_item.quantity:
                    #dif = int(quantity) - cart_item.quantity
                    if cart_item.product.count >= int(quantity):
                        cart_item.quantity = int(quantity)
                        #cart_item.product.save()
                        cart_item.save()
                    else:
                        text = "No existe esa cantidad del producto {}.".format(cart_item.product.name)
                        messages.info(request, text)
            if int(quantity) <= 0:
                remove_from_cart(request)
            return cart_item.quantity
        else:
            text = "La cantidad debe ser un número entero"
            print(text)
            messages.info(request, text)

# remove a single item from cart Rvisar porue ya actulice productos por otra parte creo
def remove_from_cart(request):
    postdata = request.POST.copy()
    item_id = postdata['item_id']
    quantity = postdata['quantity']
    cart_item = get_single_item(request, item_id)
    if cart_item:
        """     prod = cart_item.product
        prod.set_reserved(int(quantity))
        prod.save() """
        cart_item.delete()

# gets the total cost for the current cart
def cart_subtotal(request):
    cart_total = decimal.Decimal('0.00')
    print("A llamar a Price en cart_subtotal")
    price = Price.objects.filter(is_active=True)[0] # Capturo la configración de precio actual
    cart_products = get_cart_items(request)
    user = request.user
    MND = 'USD'
    TU = 'Comprador'
    if (user.is_authenticated):
        profile = get_object_or_404(Profile, user = user)
        MND = profile.MONEY_TYPE[profile.money_type][1]
        TU = profile.CLIENT_TYPE[profile.client_type][1]
    if MND == 'USD': 
        for cart_item in cart_products:
            cart_total += cart_item.total_USD()
        min_quantity_amount = price.min_quantity_amount
    elif MND == 'CUP':
        for cart_item in cart_products:
            cart_total += cart_item.total_CUP()
        min_quantity_amount = price.min_quantity_amount*price.change_usd_cup
    else:
        for cart_item in cart_products:
            cart_total += cart_item.total_MLC()
        min_quantity_amount = price.min_quantity_amount*price.change_usd_mlc
    if cart_total >= min_quantity_amount:
        porciento = 1-price.amunt_discount/100
        return cart_total*decimal.Decimal(porciento)
    elif TU == 'Distribuidor':
        falta = decimal.Decimal('0.00')
        falta += min_quantity_amount-cart_total
        porciento = price.amunt_discount
        c = round(falta, 2)
        text = "Le faltan $" + str(c) + " del monto total, para acceder a nuestra oferta especial del " + str(porciento) + "%"
        messages.info(request, text)
    return cart_total

def cart_delivery_price(request, amount, MND):
    price = Price.objects.filter(is_active=True)[0] # Capturo la configración de precio actual
    user = request.user
    try:
        deliveryObj = get_object_or_404(DeliveryInfo, client=user)
    except:
        deliveryObj = DeliveryInfo()
        deliveryObj.client = request.user
        deliveryObj.storeDelivery = get_object_or_404(Store, pk=3)
        deliveryObj.deliveryZone = 0
        deliveryObj.save()
    cart_delivery = decimal.Decimal('0.00')
    if amount >= price.get_min_delivery_free(MND):
        return cart_delivery 
    else:
        if amount > 0:
            falta = price.get_min_delivery_free(MND) - amount
            c = round(falta, 2)
            text = "Le faltan $" + str(c) + " del monto total, para acceder a nuestra oferta de envío gratis."
            messages.info(request, text)
    cart_products = get_cart_items(request)
    stores = get_stores(request)
    MND = 'USD'
    if (user.is_authenticated):
        profile = get_object_or_404(Profile, user = user)
        MND = profile.MONEY_TYPE[profile.money_type][1]
    for s in stores:
        if s == cart.delivery_Store(request):
            if MND == 'USD':
                if s.price_usd > 0:
                    cart_delivery = cart_delivery + deliveryObj.calculate_deliveryHabana()
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
