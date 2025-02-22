from django.db import models

""" def not_other_active():
    try:
        all_prices = Price.objects.all()
        if all_prices:
            for price in all_prices:
                price.is_active = False
        return True
    except:
        return False """


class Price(models.Model):
    #usd = models.DecimalField(max_digits=9,decimal_places=2, default = 0.00, verbose_name = "Precio base USD")
    change_usd_cup = models.IntegerField(default = 120, verbose_name="Cambio USD a CUP")
    change_usd_mlc = models.DecimalField(max_digits=9,decimal_places=2, default = 1.00, verbose_name="Cambio USD a MLC")
    whole_discount = models.IntegerField(default = 30, verbose_name="Porciento de descuento para ventas mayoristas (cantidad de productos)")
    min_quantity_whole = models.IntegerField(default = 20, verbose_name="Cantidad mínima para ventas mayoristas.(Unidades de un mismo producto)")
    amunt_discount = models.IntegerField(default = 10, verbose_name="Porciento de descuento para ventas mayoristas. (Monto de la compra)")
    min_quantity_amount = models.IntegerField(default = 4200, verbose_name="Monto mínimo para descuento mayorista (En USD)")
    min_delivery_free = models.IntegerField(default = 250, verbose_name="Monto mínimo para envío gratis.")
    is_active = models.BooleanField(default=False, verbose_name = "Actual")
    updated = models.DateTimeField(auto_now=True)
    
    """def __init__(self):
         if not_other_active():
            self.is_active = True 
      pass"""

    def get_min_delivery_free(self, MND='USD'):
        if MND == 'CUP':
            return self.min_delivery_free*self.change_usd_cup
        if MND == 'MLC':
            return self.min_delivery_free*self.change_usd_mlc
        return self.min_delivery_free

    def __unicode__(self):
        return str(self.updated.date())
    
    def __str__(self):
        return str(self.updated.date())