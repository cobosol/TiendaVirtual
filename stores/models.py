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
    price_usd = models.FloatField(verbose_name="Precio de entrega en USD", default=0)
    price_cup = models.FloatField(verbose_name="Precio de entrega en CUP", default=0)
    price_mlc = models.FloatField(verbose_name="Precio de entrega en MLC", default=0)
    address = models.CharField(max_length=255, verbose_name="Dirección de entrega")

    class Meta:
        verbose_name = "almacén"
        verbose_name_plural = "almacenes"    

    @property
    def products(self):
        prod_sales = Product_Sales.objects.filter(store=self)
        if prod_sales.exists():
            return prod_sales
        else:
            return None
    
    @property
    def get_image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        else:
            return "/static/tiendas/TiendaDefault.jpg"
    
    # Revisar este método. No debe hacer falta, este resultado sale del atributo de Producto
    def product_count(self, product):
        products = Product_Sales.objects.filter(store=self)
        c = 0
        for p in products:
            if p.gname == product:
                c+=1
        return c
    
    def get_absolute_url(self):
        return f"/tiendas/{self.slug}/"

    # Actualiza la cantidad de Producto a partir de los productos por almacen    
    def update_prod_count2(self, prod):
        products_by_store = Product_Sales.objects.filter(product=prod)
        prod.count = 0
        for ps in products_by_store:
            prod.count = prod.count + ps.count 
        prod.save()
    
    def update_prod_count(self, prod, count):
        products = Product_Sales.objects.filter(store=self)
        for p in products:
            if p.product == prod:
                if p.update_available(count):
                    p.save()
                    return True
        return False

    def __unicode__(self):
        return self.name
    
    def __str__(self):
        return self.name

class Product_Sales(models.Model):
    products_store = models.CharField(max_length=255,
                            help_text='Nombre único para cada tipo de producto en cada almacén.', 
                            verbose_name = "Nombre único", default = "nombre")
    product = models.ForeignKey(Product, on_delete = models.CASCADE, verbose_name="Producto a vender")
    store = models.ForeignKey(Store, on_delete=models.CASCADE, verbose_name="Almacén de ventas" )
    count = models.IntegerField(default=0, blank=False, null=False, verbose_name="Cantidad del producto en el almacén")
    available = models.IntegerField(default=0, blank=False, null=False, verbose_name="Cantidad a la venta")
    reserved = models.IntegerField(default=0, verbose_name="Cantidad de reservados, sin pagar")
    sold = models.IntegerField(default=0, blank=True, null=True, verbose_name="Cantidad de vendidos por entregar")

    class Meta:
        verbose_name = "producto en venta"
        verbose_name_plural = "productos en venta"
        ordering = ['store']

    def __unicode__(self):
        return self.products_store
    
    def save(self):
        super (Product_Sales, self).save()
        self.store.update_prod_count2(self.product)

    def update_available(self, buyed):
        if buyed < self.available:
            self.available = self.available - buyed
            return True
        return False
    
    def __str__(self):
        return self.products_store
    
    def update_count(self):
        self.product.update_count2()
        
