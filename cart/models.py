from django.db import models
from catalog.models import Product
from stores.models import Store
import decimal

class CartItem(models.Model):
    cart_id = models.CharField(max_length=50)
    date_added = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default=1)
    product = models.ForeignKey('catalog.Product', unique=False, on_delete=models.CASCADE)

    class Meta:
        db_table = 'cart_items'
        ordering = ['date_added']
        
    def total_USD(self):
        total = self.quantity * self.product.price_base
        return decimal.Decimal(total)
    
    def total_CUP(self):
        total = self.quantity * self.product.price_cup
        return decimal.Decimal(total)
    
    def total_MLC(self):
        total = self.quantity * self.product.price_mlc
        return decimal.Decimal(total)

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
        self.quantity = self.quantity + int(quantity)
        self.save()
