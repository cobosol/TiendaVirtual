from django.db import models
from django import forms
from django.contrib.auth.models import User
from catalog.models import Product
from stores.models import Store, Product_Sales
import decimal
from utils.models import Price

# Crear una clase delivery que incluya todas las definiciones de los envios.
# El municipio con los precios (diccionario), descuentos por monto...

class Order(models.Model):
    # each individual status
    SUBMITTED = 0
    PROCESSED = 1
    PAIDED = 2
    SHIPPED = 3
    CANCELLED = 4
    DELIVERED = 5
    RETURNED = 6
    CONFIRMED = 7
    # set of possible order statuses
    ORDER_STATUSES = ((SUBMITTED,'Solicitada'),
                      (PROCESSED,'Procesada'),
                      (PAIDED,'Pagada'),
                      (SHIPPED,'Transportando'),
                      (CANCELLED,'Cancelada'),
                      (DELIVERED,'Entregada'),
                      (RETURNED, 'Devuelta'),
                      (CONFIRMED, 'Confirmada'),
                      )
    
    # each individual substate
    GUANABACOA = 0
    HABANADELESTE = 1
    CERRO = 2
    COTORRO = 3
    DIEZDEOCTUBRE = 4
    HABANAVIEJA = 5
    CENTROHABANA = 6
    SANMIGUEL = 7
    BOYEROS = 8
    MARIANAO = 9
    LALISA = 10
    PLAZA = 11
    PLAYA = 12
    REGLA = 13
    ARROYO = 14

    # set of possible order statuses
    SUBSTATE = ((GUANABACOA,'Guanabacoa'),
                      (HABANADELESTE,'La Habana del Este'),
                      (CERRO,'Cerro'),
                      (COTORRO,'Cotorro'),
                      (DIEZDEOCTUBRE,'Diez de Octubre'),
                      (HABANAVIEJA,'La Habana Vieja'),
                      (CENTROHABANA, 'Centro Habana'),
                      (SANMIGUEL, 'San Miguel del Padrón'),
                      (BOYEROS,'Boyeros'),
                      (MARIANAO,'Marianao'),
                      (LALISA,'La Lisa'),
                      (PLAZA,'Plaza de la Revolución'),
                      (PLAYA, 'Playa'),
                      (REGLA, 'Regla'),
                      (ARROYO, 'Arroyo Naranjo'),
                      )
    

    # order info
    date = models.DateTimeField(auto_now_add=True, verbose_name = "Fecha")
    status = models.IntegerField(choices=ORDER_STATUSES, default=SUBMITTED, verbose_name = "Estado")
    ip_address = models.GenericIPAddressField(verbose_name = "Dirección ip")
    last_updated = models.DateTimeField(auto_now=True, verbose_name = "Última actualización")
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, verbose_name = "Usuario")
    transaction_id = models.CharField(max_length=20, help_text="Ciudad del banco de la tarjeta", verbose_name = "Nro. Transacción")
    delivery_price = models.IntegerField(verbose_name="Precio de envío", default=0)
    store_name = models.CharField(max_length=200, default="Envío Habana", verbose_name = "Nombre del tipo de entrega")
    pay_url = models.URLField(verbose_name="URL de pago", default="")
    currency = models.CharField(max_length=3, default="USD", verbose_name = "Tipo de moneda")
    price = models.ForeignKey(Price, on_delete = models.PROTECT, blank = True, null=True, verbose_name="Valores para el cálculo del Precio de la compra")

    # payment info
    payment_name = models.CharField(max_length=50, verbose_name = "Nombre del titular", null = True, blank = True)
    payment_phone = models.CharField(max_length=20, verbose_name = "Teléfono móvil")
    payment_email = models.EmailField(max_length=50, verbose_name = "Correo electrónico")
    payment_city = models.CharField(max_length=20, verbose_name = "Ciudad del banco", help_text="Ciudad del banco de la tarjeta")
    payment_postCode = models.CharField(max_length=20, verbose_name = "Código Postal")
    
    # delivery information
    delivery_name = models.CharField(max_length=50, verbose_name = "Nombre para la entrega", null = True, blank = True)
    delivery_ci = models.CharField(max_length=25, verbose_name="Número de identidad", null=True, blank=True)
    delivery_phone = models.CharField(max_length=20, verbose_name = "Teléfono")
    delivery_ws = models.CharField(max_length=20, verbose_name = "Teléfono WhatsApp")
    delivery_street = models.CharField(default = " ", max_length=100, verbose_name = "Calle", null = True, blank = True)
    delivery_apto = models.CharField(default = " ", max_length=100, verbose_name = "Número/Apartamento", null = True, blank = True)
    delivery_between = models.CharField(default = " ", max_length=100, verbose_name = "Entre calles", null = True, blank = True)
    delivery_state = models.CharField(max_length=50, verbose_name = "Provincia", default="La Habana")
    delivery_substate = models.IntegerField(choices=SUBSTATE, default=GUANABACOA, verbose_name = "Municipio")
    #delivery_substate = models.CharField(max_length=50, verbose_name = "Municipio", null = True, blank = True)
    #delivery_address_1 = models.CharField(max_length=250, verbose_name = "Dirección", null = True, blank = True)
    delivery_address_2 = models.CharField(max_length=250, verbose_name = "Dirección alternativa", null = True, blank = True)
    
    delivery = models.ForeignKey('stores.Store', unique=False, null = True, verbose_name = "Tipo de entrega", blank = True, on_delete=models.SET_NULL)
    
    class Meta:
        verbose_name = "Orden de compra"

    def __unicode__(self):
        return 'Orden #' + str(self.id)
    
    @property
    def total_items(self):
        total = decimal.Decimal('0.00')
        order_items = OrderItem.objects.filter(order=self)
        for item in order_items:
            t = item.total
            total = total + decimal.Decimal(t)
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
    
    def get_absolute_url(self):
        return f"/compra/compras/{self.id}/"
    
    def get_transfer_pay_url(self):
        return f"/compra/transfer/{self.id}/"
    
    def get_paided_url(self):
        return f"/compra/procesado/{self.id}/"
    
    @property
    def paid(self):
        if self.status == self.PAIDED:
            return True
        return False
    
    @property
    def products_list(self):
        order_items = OrderItem.objects.filter(order=self)
        products = []
        for item in order_items:
            product = item.product.name
            count = item.quantity
            count_produc = str(count) + " " + str(product)
            products.append(count_produc)
        return products

    # Al crear la orden de compra:
    # Disminuye los disponibles en Productos por Almacen
    # Incrementar la cantidad de reservados en Productos por Almacen
    # Devuelve Falso si en ese almacen algún producto no tiene disponible la cantidad solicitada. 
    def products_reserved(self):
        order_items = OrderItem.objects.filter(order=self)
        st = self.delivery
        all_available = True
        products_Sales = st.products
        for item in order_items:
           for prod in products_Sales:
               if item.product == prod.product:
                   prod.reserved = prod.reserved + item.quantity
                   prod.available = prod.available - item.quantity
                   prod.save()
                   if prod.available < 0:
                       all_available = False
                   break
        return all_available
               
    # Al pagar:
    # Incrementar la cantidad de vendidos sin entregar
    # Disminuye la cantidad de reservados
    # Devuelve falso si los reservados son menos de 0
    def products_sold(self):
        order_items = OrderItem.objects.filter(order=self)
        st = self.delivery
        products_Sales = st.products
        all_available = True
        for item in order_items:
           for prod in products_Sales:
               if item.product == prod.product:
                   prod.sold = prod.sold + item.quantity
                   prod.reserved = prod.reserved - item.quantity
                   prod.save()
                   if prod.reserved < 0:
                       all_available = False
                   break
        return all_available

    # Al entregar producto: 
    # Decrementar la cantidad de cantidad de vendidos sin entregar en el almacen.
    # Decreentar la cantidad en Producto
    # Decrementar los reservados en el Producto
    # Devuelve falso si alguno de los valores se hace negativo 
    def products_delivered(self):
        order_items = OrderItem.objects.filter(order=self)
        st = self.delivery
        products_Sales = st.products
        all_available = True
        for item in order_items:
            for prod_s in products_Sales:
                if item.product == prod_s.product:
                    prod_s.sold = prod_s.sold - item.quantity
                    prod_s.count = prod_s.count - item.quantity
                    if prod_s.count < 0 or prod_s.sold < 0:
                        all_available = False
                    prod_s.save()
                    break
            prod = item.product
            st.update_prod_count2(prod)
            prod.reserved = prod.reserved - item.quantity
            if prod.reserved < 0:
                all_available = False
            prod.save()
        return all_available
    
    # Al cancelar una orden: 
    # Decrementar la cantidad de reservados en el almacen.
    # Aumenta la cantidad de disponibles en el almacen.
    # Decrementar los reservados en el Producto
    # Devuelve falso si alguno de los valores se hace negativo 
    def order_cancelled(self):
        order_items = OrderItem.objects.filter(order=self)
        st = self.delivery
        products_Sales = st.products
        all_available = True
        for item in order_items:
            for prod in products_Sales:
                if item.product == prod.product:
                    prod.reserved = prod.reserved - item.quantity
                    prod.available = prod.available + item.quantity
                    prod.save()
                    if prod.reserved < 0 :
                        all_available = False
                    break
            prod = item.product
            prod.reserved = prod.reserved - item.quantity
            if prod.reserved < 0:
                all_available = False
            prod.save()
        return all_available
    
    # Al hacer una devolución de la orden: 
    # Decrementar la cantidad de reservados en el almacen.
    # Aumenta la cantidad de disponibles en el almacen.
    # Decrementar los reservados en el Producto
    # Devuelve falso si alguno de los valores se hace negativo 
    def order_returned(self):
        order_items = OrderItem.objects.filter(order=self)
        st = self.delivery
        products_Sales = st.products
        all_available = True
        for item in order_items:
            for prod in products_Sales:
                if item.product == prod.product:
                    prod.count = prod.count + item.quantity
                    prod.available = prod.available + item.quantity
                    prod.save()
                    break
            prod = item.product
            st.update_prod_count2(prod)
            prod.save()
        return all_available

    def verify_order_items(self):
        print("Entro a verificar")
        order_items = OrderItem.objects.filter(order=self)
        for item in order_items:
            disp = item.product.count - item.product.reserved
            if item.quantity >= disp:
                return False
        for item in order_items:
            print("Entro a actualizar reservados")
            item.product.reserved = item.product.reserved + item.quantity
            item.product.save()
        return True

    def update_status(self, new_status):   
        self.status = new_status     
        if new_status == self.SUBMITTED:
            self.products_reserved()
        elif new_status == self.PROCESSED:
            if not self.verify_order_items():
                self.status = self.CANCELLED
        elif new_status == self.PAIDED:
            self.products_sold()
        elif new_status == self.DELIVERED:
            self.products_delivered()
        elif new_status == self.CANCELLED:
            self.order_cancelled()
        elif new_status == self.RETURNED:
            self.order_returned()

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name = "Producto")
    quantity = models.DecimalField(max_digits=9,decimal_places=2,default=1.00, verbose_name = "Cantidad")
    price = models.DecimalField(max_digits=9,decimal_places=2, verbose_name = "Precio")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name = "Orden")
    store_name = models.CharField(max_length=250, default="Envío Habana", verbose_name = "Forma de entrega")

    @property
    def total(self):
        #MND = self.order.currency
        price = self.product.price
        if price:
            if self.quantity >= price.min_quantity_whole:
                porciento = decimal.Decimal('0.00')
                porciento = 1-price.whole_discount/100
                precio = decimal.Decimal('0.00')
                precio = self.price * decimal.Decimal(porciento)
                print(self.quantity)
                return self.quantity * precio
            else:
                return self.quantity * self.price
        else:
            return -1


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
    
    def update_status(self, status):
        return True
    


