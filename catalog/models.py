from django.db import models
from django.urls import reverse
from .validators import valid_extension
import os
from django_ckeditor_5.fields import CKEditor5Field

class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name="Nombre")
    slug = models.SlugField(max_length=50, unique=True, 
                            help_text='Valor único de cada producto creado a partir del nombre', 
                            verbose_name = "Código URL")
    image = models.ImageField(upload_to="Categorias", null=True, blank=True,
        verbose_name="Imagen")
    description = models.TextField(verbose_name = "Descripción")
    is_active = models.BooleanField(default=True, verbose_name = "Activo")
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
            return "/static/catalog/images/categories/catDefault.jpg"

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
                            help_text='Nombre único para cada tipo de producto, incluye presentación (500ml, 1l, Tonelada).', 
                            verbose_name = "Nombre único")
    gname = models.CharField(max_length=255, default="",
                             help_text='Nombre genérico del producto.',
                             verbose_name = "Producto")
    presentation = models.CharField(max_length=50, default="", help_text="Presentación (con unidad de medida).", 
                                    verbose_name="Presentación")
    slug = models.SlugField(max_length=255, unique=True, 
                            help_text='Valor único para la página de los productos, creada a partir del nombre único.', 
                            verbose_name = "Nombre para URL")
    """ marca """
    brand = models.CharField(max_length=50, verbose_name = "Marca")  
    """ código del producto """
    sku = models.CharField(max_length=50, 
                           help_text='Código específico del producto.', 
                           verbose_name = "Código")
    price = models.DecimalField(max_digits=9,decimal_places=2, verbose_name = "Precio")
    old_price = models.DecimalField(max_digits=9,decimal_places=2, blank=True, default=0.00, verbose_name = "Precio viejo")
    image = models.ImageField(upload_to="Productos", null=True, blank=True,
        verbose_name="Imagen del producto")
    is_active = models.BooleanField(default=True, verbose_name = "Activo")
    """ más vendidos """
    is_bestseller = models.BooleanField(default=False, verbose_name = "Más vendido")
    """ Próxima venta """
    is_featured = models.BooleanField(default=False, verbose_name = "Próxima venta")
    """ Ficha del producto """
    prod_datasheet = models.FileField(blank=True, null=True, upload_to=generate_path, validators=[valid_extension],
                                      verbose_name="Ficha técnica del producto")
    """ Presentación del producto (500ml, 1l, Tonelada) """
    """     unit = models.CharField(max_length=10, default="unidades", verbose_name = "unidad de medida") """
    """ Cantidad total """
    """     quantity = models.IntegerField(verbose_name = "cantidad") """
    """ Otra información de interés """
    description = CKEditor5Field('Descripción', config_name='extends')
    meta_keywords = models.CharField(max_length=255, help_text='Comma-delimited set of SEO keywords for meta tag')
    meta_description = models.CharField(max_length=255, help_text='Content for description meta tag')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField(Category, verbose_name = "Categorías")

    class Meta:
        db_table = 'products'
        ordering = ['-created_at']
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        
    @property
    def get_image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        else:
            return "/static/catalog/images/products/main/prod_Default.jpg"
        
    @property
    def get_file_url(self):
        if self.prod_datasheet and hasattr(self.prod_datasheet, 'url'):
            return self.prod_datasheet.url
        else:
            return "/static/Fichas/FICHATECNICA.pdf"
        

    def __unicode__(self):
        return self.name
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f"/catalogo/producto/{self.slug}/"

    def sale_price(self):
        if self.old_price > self.price:
            return self.price
        else:
            return None
