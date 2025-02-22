from django.db import models
from django.urls import reverse
from .validators import valid_extension
import os
from django_ckeditor_5.fields import CKEditor5Field
from django.utils.text import slugify
from utils.models import Price

class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name="Nombre")
    slug = models.SlugField(max_length=50, unique=True, 
                            help_text='Valor único de cada producto creado a partir del nombre', 
                            verbose_name = "Código URL")
    image = models.ImageField(upload_to="Categorias", null=True, blank=True,
        verbose_name="Imagen")
    description = models.TextField(verbose_name = "Descripción")
    is_active = models.BooleanField(default=True, verbose_name = "Activo")
    is_feedstock = models.BooleanField(default=False, verbose_name = "Materia prima")
    meta_keywords = models.CharField("Meta Keywords", max_length=255, help_text= 'Conjunto de palabras clave separadas por coma')
    meta_description = models.CharField("Meta Description", max_length=255, help_text='Contenido de la descripción de las palabras clave')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'categories'
        ordering = ['-created_at']
        verbose_name = "Categoría"
        verbose_name_plural = 'Categorias'

    @property
    def get_image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        else:
            return "/static/img/catDefault.webp"

    def __unicode__(self):
        return self.name
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f"/catalogo/categoria/{self.slug}/"         

    @property
    def get_product_count(self):
        products = Product.objects.all()
        count = 0
        for prod in products:
            categories = prod.categories.all()
            for cat in categories: 
                if self.slug == cat.slug:
                    count += 1
        return count

def generate_path(instance, filename): 
    folder = "Ficha_" + str(instance.slug) 
    return os.path.join("Fichas", folder, filename)


class Product(models.Model):
    name = models.CharField(max_length=255, unique=True,
                            help_text='Nombre único para cada tipo de producto.', 
                            verbose_name = "Nombre único")
    gname = models.CharField(max_length=255, default="",
                             help_text='Nombre genérico del producto.',
                             verbose_name = "Producto")
    presentation = models.CharField(max_length=50, default="", help_text="Presentación (con unidad de medida).", 
                                    verbose_name="Presentación")
    slug = models.SlugField(max_length=255, unique=True, 
                            help_text='Valor único para URL, se crea automático',
                            default = 'URL', 
                            verbose_name = "Nombre para URL")
    """ marca """
    brand = models.CharField(max_length=50, verbose_name = "Marca")  
    """ código del producto """
    sku = models.CharField(max_length=50, 
                           help_text='Código específico del producto.', 
                           verbose_name = "Código")
    price = models.ForeignKey(Price, on_delete = models.PROTECT, blank=True, null=True, verbose_name="Configuración de precios del producto")
    price_base = models.DecimalField(max_digits=9,decimal_places=2, default = 0.00, verbose_name = "Precio USD")
    old_price = models.DecimalField(max_digits=9,decimal_places=2, blank=True, default=0.00, verbose_name = "Precio viejo")
    is_feedstock = models.BooleanField(default=False, verbose_name = "Materia prima")
    available_online = models.BooleanField(default=True, verbose_name = "Disponible para venta online")
    available_CUP = models.BooleanField(default=True, verbose_name = "Disponible en CUP")
    available_MLC = models.BooleanField(default=True, verbose_name = "Disponible en MLC")    
    image = models.ImageField(upload_to="Productos", null=True, blank=True,
        verbose_name="Imagen del producto")
    count = models.IntegerField(default=0, verbose_name="Cantidad", help_text="Cantidad del producto en inventarios")
    reserved = models.IntegerField(default=0, verbose_name="Reservados", help_text="Cantidad reservados para comprar")
    is_active = models.BooleanField(default=True, verbose_name = "Activo")
    """ más vendidos """
    is_bestseller = models.BooleanField(default=False, verbose_name = "Más vendido")
    """ Próxima venta """
    is_featured = models.BooleanField(default=False, verbose_name = "Próxima venta")
    """ Descuento por cantidad """
    #has_discount = models.BooleanField(default=False, verbose_name = "Descuento por cantidad")
    """ Ficha del producto """
    prod_datasheet = models.FileField(blank=True, null=True, upload_to=generate_path, validators=[valid_extension],
                                      verbose_name="Ficha técnica")
    """ Otra información de interés """
    description = CKEditor5Field('Descripción', config_name='extends')
    meta_keywords = models.CharField(max_length=255, help_text='Palabras clave para el SEO')
    meta_description = models.CharField(max_length=255, help_text='Contenido clave para el SEO')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField(Category, verbose_name = "Categorías")

    class Meta:
        db_table = 'products'
        ordering = ['name']
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)
        
    @property
    def get_image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        else:
            return "/static/img/prod_Default.webp"
    
    @property        
    def price_cup(self):
        price_actual = Price.objects.filter(is_active=True)[0]
        return self.price_base * price_actual.change_usd_cup
        
    @property
    def price_mlc(self):
        price_actual = Price.objects.filter(is_active=True)[0]
        return self.price_base * price_actual.change_usd_mlc
    
    @property
    def get_file_url(self):
        if self.prod_datasheet and hasattr(self.prod_datasheet, 'url'):
            return self.prod_datasheet.url
        else:
            return "/static/Fichas/FICHATECNICA.pdf"
    
    def get_price(self, MND):
        if MND == 'USD':
            return self.price_base
        if MND == 'CUP':
            return self.price_cup
        else:
            return self.price_mlc
        
    def __unicode__(self):
        return self.name
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f"/catalogo/producto/{self.slug}/"
    
    # Verifico si los que se van a reservar son menos que la cantidad del producto
    def set_reserved(self, reser):
        if reser <= self.count:
            return True
        return False

    def update_count(self, buyed):
        if buyed < self.reserved:
            self.reserved = self.reserved - buyed
            self.count = self.count - buyed 
            return True
        return False

    def sale_price(self):
        if self.old_price > self.price_base:
            return self.price_base
        else:
            return None
