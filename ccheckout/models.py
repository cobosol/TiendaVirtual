from django.db import models
from django import forms
from django.contrib.auth.models import User
from catalog.models import Product
from stores.models import Store
import decimal

""" class DeliveryType(models.Model):
    name_id = models.CharField(max_length=50, verbose_name = "Nombre del tipo de entrega")
    description = models.CharField(max_length=250, verbose_name = "Descripción")
    price = models.DecimalField(max_digits=9,decimal_places=2, verbose_name = "Costo")
    services_hours = models.CharField(max_length=50, verbose_name = "Horario de entrega")
    shipping_country = models.CharField(max_length=50, verbose_name = "País")
    shipping_zip = models.CharField(max_length=10, verbose_name = "Código postal") 

    def __str__(self):
        return self.name_id
    
    class Meta:
        verbose_name = "Tipo de entrega" """


class Order(models.Model):
    # each individual status
    SUBMITTED = 0
    PROCESSED = 1
    SHIPPED = 2
    CANCELLED = 3
    ENTREGADA = 4
    DEVUELTA = 5
    # set of possible order statuses
    ORDER_STATUSES = ((SUBMITTED,'Solicitada'),
                      (PROCESSED,'Procesando'),
                      (SHIPPED,'Transportando'),
                      (CANCELLED,'Cancelada'),
                      (ENTREGADA,'Entregada'),
                      (DEVUELTA, 'Devuelta'),
                      )
    
    # order info
    date = models.DateTimeField(auto_now_add=True, verbose_name = "Fecha")
    status = models.IntegerField(choices=ORDER_STATUSES, default=SUBMITTED, verbose_name = "Estado")
    ip_address = models.GenericIPAddressField(verbose_name = "Dirección ip")
    last_updated = models.DateTimeField(auto_now=True, verbose_name = "Última actualización")
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, verbose_name = "Usuario")
    transaction_id = models.CharField(max_length=20, verbose_name = "Id de la transacción")
    delivery_price = models.IntegerField(verbose_name="Precio de envío", default=0)

    # contact info
    email = models.EmailField(max_length=50, verbose_name = "Correo electrónico")
    phone = models.CharField(max_length=20, verbose_name = "Teléfono")
    
    # delivery information
    delivery_name = models.CharField(max_length=50, verbose_name = "Nombre para la entrega", null = True, blank = True)
    delivery_ci = models.CharField(max_length=25, verbose_name="Número de identidad", null=True, blank=True)
    delivery_address_1 = models.CharField(max_length=250, verbose_name = "Dirección", null = True, blank = True)
    delivery_address_2 = models.CharField(max_length=250, verbose_name = "Dirección alternativa", null = True, blank = True)
    delivery_state = models.CharField(max_length=50, verbose_name = "Municipio", null = True, blank = True)
#   delivery_type = models.ForeignKey(DeliveryType, on_delete=models.SET_NULL, verbose_name = "Tipo de entrega", null=True)  
    

    """ shipping_address_1 = models.CharField(max_length=50, verbose_name = "Dirección")
    shipping_address_2 = models.CharField(max_length=50, blank=True, verbose_name = "Dirección alternativa") """

    # billing information
    """     billing_name = models.CharField(max_length=50, verbose_name = "Nombre para facturación")
    billing_address_1 = models.CharField(max_length=50, verbose_name = "Dirección")
    billing_address_2 = models.CharField(max_length=50, blank=True, verbose_name = "Dirección alterntiva")
    billing_city = models.CharField(max_length=50, verbose_name = "Ciudad")
    billing_state = models.CharField(max_length=50, verbose_name = "Municipio")
    billing_country = models.CharField(max_length=50, verbose_name = "País")
    billing_zip = models.CharField(max_length=10, verbose_name = "Código postal") """
    
    class Meta:
        verbose_name = "Orden de compra"

    def __unicode__(self):
        return 'Orden #' + str(self.id)
    
    @property
    def total_items(self):
        total = decimal.Decimal('0.00')
        order_items = OrderItem.objects.filter(order=self)
        for item in order_items:
            total += item.total
        return total
    
    @property
    def total(self):
        return self.total_items + self.delivery_price

    @property
    def statusS(self):
        return self.ORDER_STATUSES[self.status][1]
    
    @property
    def first_name(self):
        return self.user.first_name
    
    @property
    def products_list(self):
        order_items = OrderItem.objects.filter(order=self)
        products = []
        for item in order_items:
            product = item.product.name
            products.append(product)
        return products
    
    """ @property
    def delivery_name(self):
        return self.delivery_type.name_id """
    
    """ @property
    def delivery_description(self):
        return self.delivery_type.description
    
    @property
    def delivery_price(self):
        return self.delivery_type.price
    
    @property
    def delivery_services_hours(self):
        return self.delivery_type.services_hours """


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name = "Producto")
    quantity = models.IntegerField(default=1, verbose_name = "Cantidad")
    price = models.DecimalField(max_digits=9,decimal_places=2, verbose_name = "Precio")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name = "Orden")
    store_name = models.CharField(max_length=250, default="Envío Habana", verbose_name = "Forma de entrega")

    @property
    def total(self):
        return self.quantity * self.price

    @property
    def name(self):
        return self.product.name

    @property
    def sku(self):
        return self.product.sku

    def __unicode__(self):
        return self.product.name + ' (' + self.product.sku + ')'
    
    def get_absolute_url(self):
        return self.product.get_absolute_url()
    


