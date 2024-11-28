from django.db import models
from django.contrib.auth.models import User, Group 
from django.dispatch import receiver
from django.db.models.signals import post_save
from stores.models import Store

def custom_upload_to(instance, filename):
    old_instance = Profile.objects.get(pk=instance.pk)
    old_instance.avatar.delete()
    return 'profiles/' + filename
    
class Profile(models.Model):
    # Tipo de cliente
    COMPRADOR = 0
    PRODUCTOR = 1
    DISTRIBUIDOR = 2
    VENDEDOR = 3

    CLIENT_TYPE = ((COMPRADOR,'Comprador'),
                   (PRODUCTOR,'Productor'),
                   (DISTRIBUIDOR,'Distribuidor'),
                   (VENDEDOR, 'Vendedor'),
                   )

    # Moneda preferida
    USD = 0
    CUP = 1
    MLC = 2

    MONEY_TYPE = ((USD,'USD'),
                   (CUP,'CUP'),
                   (MLC,'MLC'),
                   )
    
    user = models.OneToOneField(User, on_delete = models.CASCADE, verbose_name = "Usuario")
    cid = models.CharField(max_length=20, 
                            help_text='Número de identificación', 
                            verbose_name = "Número de identidad")
    avatar = models.ImageField(upload_to='profiles', null=True, blank=True, verbose_name = "Foto")
    bio = models.TextField(null=True, blank=True, verbose_name = "Biografía")
    client_type = models.IntegerField(choices=CLIENT_TYPE, default=COMPRADOR, help_text='Puede cambiarlo cuando desee en su perfil', verbose_name = "Tipo de cliente")
    money_type = models.IntegerField(choices=MONEY_TYPE, default=USD, help_text='En cualquier momento puede cambiarla', verbose_name = "Tipo de moneda")
    link = models.URLField(max_length=200, null=True, blank=True, verbose_name = "Enlace")
    phone = models.CharField(max_length=15, null=True, blank = True,
                            help_text='', 
                            verbose_name = "Número de móvil")
    ws = models.CharField(max_length=15, null=True, blank = True,
                            help_text='Número de teléfono para WhatsApp', 
                            verbose_name = "Número para WhatsApp")
    
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
    prefered_store = models.ForeignKey(Store, on_delete = models.SET_NULL, null=True, blank = True, 
                            verbose_name = "Forma de entrega preferida")

    class Meta:
        ordering = ['user']
        verbose_name = "Perfil"
        verbose_name_plural = "Perfiles"

    def __str__(self):
        return self.user.first_name

    """     def save(self, *args, **kwargs):
        print("Entre a save")
        super(Profile, self).save(*args, **kwargs)
        if self.client_type == self.PRODUCTOR:
            group = Group.objects.get(name='productores')
            self.user.groups.add(group)
            group2 = Group.objects.get(name='distribuidores')
            self.user.groups.remove(group2)
        elif self.client_type == self.DISTRIBUIDOR:
            group = Group.objects.get(name='distribuidores')
            self.user.groups.add(group)
            group2 = Group.objects.get(name='productores')
            self.user.groups.remove(group2)
        else:
            group = Group.objects.get(name='distribuidores')
            self.user.groups.remove(group)
            group2 = Group.objects.get(name='productores')
            self.user.groups.remove(group2)
        print("Verifique")
        super(Profile, self).save(*args, **kwargs) """

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
        print("Se acaba de crear un usuario y su perfil enlazado.")
