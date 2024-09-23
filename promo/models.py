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
    