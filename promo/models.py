from django.db import models

class Banner(models.Model):
    title = models.CharField(max_length=200, 
        verbose_name="Título del Banner")
    description = models.TextField(
        verbose_name="Descripción")
    is_active = models.BooleanField(default=True, verbose_name = "Activo")
    main =  models.BooleanField(default=False, verbose_name = "Principal", help_text="Puede estar marcado un solo banner como principal")
    image = models.ImageField(verbose_name="Imagen", 
        upload_to="Banners")

    class Meta:
        verbose_name = "banner"
        verbose_name_plural = "banners"
        ordering = ['-title']

    def __str__(self):
        return self.title
    
class Offer(models.Model):
    title = models.CharField(max_length=200, verbose_name="Título de la oferta. Primer texto")
    mainText = models.CharField(max_length=200, verbose_name="Texto principal")
    button = models.CharField(max_length=200, verbose_name="Texto del botón")
    butonLink = models.URLField(verbose_name="Enlace del botón")
    description = models.TextField(verbose_name="Descripción")
    is_active = models.BooleanField(default=True, verbose_name = "Activa")
    main =  models.BooleanField(default=False, verbose_name = "Principal", help_text="Puede estar marcada una sola como principal")
    second =  models.BooleanField(default=False, verbose_name = "Secundaria", help_text="Puede estar marcada una sola como secundaria")
    image = models.ImageField(verbose_name="Imagen", upload_to="Offers")


    class Meta:
        verbose_name = "offer"
        verbose_name_plural = "offers"
        ordering = ['-title']

    def __str__(self):
        return self.title