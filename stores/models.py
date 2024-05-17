from django.db import models
from catalog.models import Product

class Store(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Nombre de almacén")
    slug = models.SlugField(max_length=50, unique=True, default = name, null = True, blank = True,
                            help_text='Valor único de cada tipo de entrega, creado a partir del nombre.', 
                            verbose_name = "código para URL")
    image = models.ImageField(upload_to="Tiendas", null=True, blank=True,
                              verbose_name="Imagen del punto de venta")
    hours = models.CharField(max_length=255, verbose_name="Horario de entrega")
    price = models.FloatField(verbose_name="Precio de entrega", default=0)
    address = models.CharField(max_length=255, verbose_name="Dirección de entrega")

    class Meta:
        verbose_name = "almacén"
        verbose_name_plural = "almacenes"    

    @property
    def products(self):
        return Product_Sales.objects.filter(store=self)
    
    @property
    def get_image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        else:
            return "/static/tiendas/TiendaDefault.jpg"
    
    def product_count(self, product):
        products = Product_Sales.objects.filter(store=self)
        c = 0
        for p in products:
            if p.gname == product:
                c+=1
        return c
    
    def get_absolute_url(self):
        return f"/tiendas/{self.slug}/"

    
    """     def products(self, product):
        products_stores = Product_Sales.objects.filter(product)
        c = 0
        for p in products:
            if p.gname == product:
                c+=1
        return c """
    

    def __unicode__(self):
        return self.name
    
    def __str__(self):
        return self.name

class Product_Sales(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE, verbose_name="Producto a vender")
    store = models.ForeignKey(Store, on_delete=models.CASCADE, verbose_name="Almacén de ventas" )
    available = models.IntegerField(default=0, blank=False, null=False, verbose_name="Cantidad a la venta")
    reserved = models.IntegerField(default=0, blank=True, null=True, verbose_name="Cantidad de vendidos sin entregar")

    class Meta:
        verbose_name = "producto en venta"
        verbose_name_plural = "productos en venta"
        ordering = ['product']

    def __unicode__(self):
        return self.product.name
    
    def updateAvailable(reserve):
        available = available - reserve
        reserved = reserved + reserve
        print(reserved)
    
    def __str__(self):
        return self.product.name
