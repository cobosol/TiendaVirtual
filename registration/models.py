from django.db import models
from django.contrib.auth.models import User 
from django.dispatch import receiver
from django.db.models.signals import post_save

def custom_upload_to(instance, filename):
    old_instance = Profile.objects.get(pk=instance.pk)
    old_instance.avatar.delete()
    return 'profiles/' + filename
    
class Profile(models.Model):
    COMPRADOR = 1
    PRODUCTOR = 2
    COMERCIANTE = 3
    # set of possible order statuses
    CLIENT_TYPE = ((COMPRADOR,'Comprador ocasional'),
                   (PRODUCTOR,'Comprador de materias primas'),
                   (COMERCIANTE,'Comprador al mayor'),)
    user = models.OneToOneField(User, on_delete = models.CASCADE, verbose_name = "Usuario")
    avatar = models.ImageField(upload_to='profiles', null=True, blank=True, verbose_name = "Foto")
    bio = models.TextField(null=True, blank=True, verbose_name = "Biografía")
    client_type = models.IntegerField(choices=CLIENT_TYPE, default=COMPRADOR, verbose_name = "Tipo de cliente")
    link = models.URLField(max_length=200, null=True, blank=True, verbose_name = "Enlace")
    # Special User
    reeup = models.CharField(max_length=20, unique=True, null=True, blank = True,
                            help_text='', 
                            verbose_name = "Código REEUP")
    nit = models.CharField(max_length=20, unique=True, null=True, blank = True,
                            help_text='', 
                            verbose_name = "Código NIT")
    address = models.CharField(max_length=100, null=True, blank = True, 
                            verbose_name = "Dirección oficial")
    agency = models.CharField(max_length=100, null=True, blank = True, 
                            verbose_name = "Agencia bancaria")
    contract = models.CharField(max_length=50, null=True, blank = True, 
                            verbose_name = "Número de contrato")

    @property
    def name(self):
        return self.user.first_name
    
    @property
    def get_avatar_url(self):
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar.url 
        else:
            return "/static/images/Profile/silueta.jpg"

@receiver(post_save, sender=User)
def ensure_profile_exists(sender, instance, **kwargs):
    if kwargs.get('created', False):
        Profile.objects.get_or_create(user=instance)
        print("Se acaba de crear un usuario y su pefil enlazado.")
