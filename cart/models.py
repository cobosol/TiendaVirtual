from typing import Any
from django.db import models
from catalog.models import Product
from stores.models import Store
import decimal
from utils.models import Price

class CartItem(models.Model):
    cart_id = models.CharField(max_length=50)
    date_added = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default=1)
    product = models.ForeignKey('catalog.Product', unique=False, on_delete=models.CASCADE)
    #price = models.ForeignKey('utils.Price', on_delete = models.CASCADE, blank=True, null=True, verbose_name="Cálculo de precio")

    class Meta:
        db_table = 'cart_items'
        ordering = ['date_added']
        
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def total_USD(self):
        price = Price.objects.filter(is_active=True)[0] # Capturo la configración de precio actual
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

