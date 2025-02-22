from typing import Any
from django.db import models
from django.contrib.auth.models import User
from catalog.models import Product
from stores.models import Store
from stores.models import Store
import decimal
from utils.models import Price

class DeliveryInfo(models.Model):
    # each individual substate
    ZONAENVIO = 0
    GUANABACOA = 1
    VILLAPANAMERICANA_BAHIA = 2
    REGLA = 3
    CASABLANCA = 4
    ALAMAR_COJIMAR = 5
    SANMIGUEL = 6
    LUYANO = 7
    TARARA_GUANABO_SANTAFE = 8
    HABANAVIEJA = 9
    CENTROHABANA = 10
    CAMPOFLORIDO = 11
    DIEZDEOCTUBRE = 12
    PLAZA = 13
    CERRO_ESQUINATEJAS = 14
    CERRO_CIUDADDEPORTIVA = 15 
    ARROYONARANJO = 16
    BOYEROS = 17
    PLAYA = 18
    MARIANAO = 19
    LALISA = 20
    COTORRO = 21

    #Costo
    C_ZONAENVIO = 15
    C_GUANABACOA = 3
    C_VILLAPANAMERICANA_BAHIA = 3
    C_REGLA = 3
    C_CASABLANCA = 4
    C_ALAMAR_COJIMAR = 4
    C_SANMIGUEL = 4
    C_LUYANO = 5
    C_TARARA_GUANABO_SANTAFE = 5
    C_HABANAVIEJA = 5
    C_CENTROHABANA = 5
    C_CAMPOFLORIDO = 6
    C_DIEZDEOCTUBRE = 6
    C_PLAZA = 6
    C_CERRO_ESQUINATEJAS = 7
    C_CERRO_CIUDADDEPORTIVA = 8 
    C_ARROYONARANJO = 10
    C_BOYEROS = 10
    C_PLAYA = 10
    C_MARIANAO = 10
    C_LALISA = 15
    C_COTORRO = 15

    # set of possible order statuses
    DELIVERY_ZONE = ((ZONAENVIO, '--------------------'),
                    (GUANABACOA, 'Guanabacoa'),
                    (VILLAPANAMERICANA_BAHIA, 'Villa Panamericana'),
                    (REGLA, 'Regla'),
                    (CASABLANCA, 'Casablanca'),
                    (ALAMAR_COJIMAR, 'Alamar/Cojímar'),
                    (SANMIGUEL, 'San Miguel'),
                    (LUYANO, 'Luyanó'),
                    (TARARA_GUANABO_SANTAFE, 'Tarará/Guanabo/Santa Fé'),
                    (HABANAVIEJA, 'Habana Vieja'),
                    (CENTROHABANA, 'Centro Habana'),
                    (CAMPOFLORIDO, 'Campo Florido'),
                    (DIEZDEOCTUBRE,'10 de octubre'),
                    (PLAZA, 'Plaza'),
                    (CERRO_ESQUINATEJAS, 'Cerro, Esquina de Tejas'),
                    (CERRO_CIUDADDEPORTIVA, 'Cerro, Ciudad Deportiva'), 
                    (ARROYONARANJO, 'Arroyo Naranjo'),
                    (BOYEROS, 'Boyeros'),
                    (PLAYA, 'Playa'),
                    (MARIANAO, 'Marianao'),
                    (LALISA, 'La Lisa'),
                    (COTORRO, 'Cotorro'),
                    )
    C_DELIVERY_ZONE = ((ZONAENVIO, '--------------------', C_ZONAENVIO),
                    (GUANABACOA, 'Guanabacoa', C_GUANABACOA),
                    (VILLAPANAMERICANA_BAHIA, 'Villa Panamericana', C_VILLAPANAMERICANA_BAHIA),
                    (REGLA, 'Regla', C_REGLA),
                    (CASABLANCA, 'Casablanca', C_CASABLANCA),
                    (ALAMAR_COJIMAR, 'Alamar/Cojímar', C_ALAMAR_COJIMAR),
                    (SANMIGUEL, 'San Miguel', C_SANMIGUEL),
                    (LUYANO, 'Luyanó', C_LUYANO),
                    (TARARA_GUANABO_SANTAFE, 'Tarará/Guanabo/Santa Fé', C_TARARA_GUANABO_SANTAFE),
                    (HABANAVIEJA, 'Habana Vieja', C_HABANAVIEJA),
                    (CENTROHABANA, 'Centro Habana', C_CENTROHABANA),
                    (CAMPOFLORIDO, 'Campo Florido', C_CAMPOFLORIDO),
                    (DIEZDEOCTUBRE,'10 de octubre', C_DIEZDEOCTUBRE),
                    (PLAZA, 'Plaza', C_PLAZA),
                    (CERRO_ESQUINATEJAS, 'Cerro, Esquina de Tejas', C_CERRO_ESQUINATEJAS),
                    (CERRO_CIUDADDEPORTIVA, 'Cerro, Ciudad Deportiva', C_CERRO_CIUDADDEPORTIVA), 
                    (ARROYONARANJO, 'Arroyo Naranjo', C_ARROYONARANJO),
                    (BOYEROS, 'Boyeros', C_BOYEROS),
                    (PLAYA, 'Playa', C_PLAYA),
                    (MARIANAO, 'Marianao', C_MARIANAO),
                    (LALISA, 'La Lisa', C_LALISA),
                    (COTORRO, 'Cotorro', C_COTORRO),
                    )
    
    client = models.ForeignKey(User, unique=False, on_delete=models.CASCADE)
    storeDelivery = models.ForeignKey('stores.Store', unique=False, on_delete=models.CASCADE)
    deliveryZone = models.IntegerField(choices=DELIVERY_ZONE, default=ZONAENVIO, verbose_name = "Zona de envío")

    # Nombre de la zona a partir del valor
    @property
    def getDeliveryZone(self):
        return self.DELIVERY_ZONE[self.deliveryZone][1]

    # Calcular envío Habana
    def calculate_deliveryHabana(self):
        cart_delivery = decimal.Decimal('0.00')
        cart_delivery += self.C_DELIVERY_ZONE[self.deliveryZone][2] 
        return cart_delivery
        """ if int(self.deliveryZone) == int(self.GUANABACOA):
            valor = 3
            valorD = decimal.Decimal(valor)
            return valorD
        elif self.deliveryZone == self.HABANADELESTE:
            print("Habana del este")
            return decimal.Decimal('4.00')
        else:
            valor = 15
            valorD = decimal.Decimal(valor)
            return valorD """

class CartItem(models.Model):
    cart_id = models.CharField(max_length=50)
    date_added = models.DateTimeField(auto_now_add=True)
    quantity = models.DecimalField(max_digits=9, decimal_places=2, default=1.00, verbose_name = "Cantidad del producto")
    product = models.ForeignKey('catalog.Product', unique=False, on_delete=models.CASCADE)
    #price = models.ForeignKey('utils.Price', on_delete = models.CASCADE, blank=True, null=True, verbose_name="Cálculo de precio")

    class Meta:
        db_table = 'cart_items'
        ordering = ['date_added']
        
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def total_USD(self):
        price = Price.objects.filter(is_active=True)[0] # Capturo la configración de precio actual
        print("En total USD")
        if self.quantity >= price.min_quantity_whole:
            porciento = 1-price.whole_discount/100
            discount = self.product.price_base*decimal.Decimal(porciento)
            total = self.quantity*decimal.Decimal(discount) 
            return decimal.Decimal(total)
        total = self.quantity * self.product.price_base
        return decimal.Decimal(total)
    
    def total_CUP(self):
        price = Price.objects.filter(is_active=True)[0] # Capturo la configración de precio actual
        if self.quantity >= price.min_quantity_whole:
            porciento = 1-price.whole_discount/100
            discount = self.product.price_cup*decimal.Decimal(porciento)
            total = self.quantity*decimal.Decimal(discount)
            return decimal.Decimal(total)
        total = self.quantity * self.product.price_cup
        return decimal.Decimal(total)
    
    def total_MLC(self):
        price = Price.objects.filter(is_active=True)[0] # Capturo la configración de precio actual
        if self.quantity >= price.min_quantity_whole:
            porciento = 1-price.whole_discount/100
            discount = self.product.price_mlc*decimal.Decimal(porciento)
            total = self.quantity*decimal.Decimal(discount)
            return decimal.Decimal(total)
        total = self.quantity * self.product.price_mlc
        return decimal.Decimal(total)
    
    def discount_message(self):
        price = Price.objects.filter(is_active=True)[0] # Capturo la configración de precio actual
        text = ""
        if price.whole_discount > 0:
            to_whole = price.min_quantity_whole - self.quantity
            porciento = price.whole_discount
            product = self.product.gname
            if to_whole > 0:
                if to_whole == 1:
                    text = "Te falta " + str(to_whole) + " del producto " + str(product) + " para nuestra oferta especial del " + str(porciento) + "%"
                else:
                    text = "Te faltan " + str(to_whole) + " del producto " + str(product) + " para nuestra oferta especial del " + str(porciento) + "%"
            elif to_whole == 0:
                text = "Gracias por acojerse a nuestras ofertas especiales"
        return text

    def name(self):
        return self.product.name
        
    def price_USD(self):
        price = self.product.get_price('USD')
        return decimal.Decimal(price)
    
    def price_CUP(self):
        price = self.product.get_price('CUP')
        return decimal.Decimal(price)
    
    def price_MLC(self):
        price = self.product.get_price('MLC')
        return decimal.Decimal(price)
    
    def get_absolute_url(self):
        return self.product.get_absolute_url()

    def augment_quantity(self, quantity):
        new_quantity = self.quantity + int(quantity)
        if new_quantity <= self.product.count:
            self.quantity = new_quantity
            self.save()
            return True
        else:
            self.quantity = self.product.count
            self.save()
            return False

    @property
    def int_quantity(self, quantity=0.00):
        if quantity == 0.00:
            return int(self.quantity)
        else:
            self.quantity = quantity
            

