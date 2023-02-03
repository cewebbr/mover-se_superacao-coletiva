from django.contrib.auth.models import AbstractUser
from django.db import models
from tinymce.models import HTMLField


class User(AbstractUser):
    profile_picture = models.ImageField(
        verbose_name='Foto de Perfil', upload_to='users/profile_prictures/%Y/%m/%d/', null=True, blank=True)

    about = HTMLField(
        verbose_name="Sobre", blank=True)

    phone_number = models.CharField(
        verbose_name="Telefone", max_length=255, blank=True)
    cell_phone_number = models.CharField(
        verbose_name="Celular", max_length=255, blank=True)

    zip = models.CharField(verbose_name="CEP", max_length=255, blank=True)
    city = models.CharField(verbose_name="Cidade", max_length=255, blank=True)
    state = models.CharField(verbose_name="Estado", max_length=255, blank=True)
    country = models.CharField(verbose_name="País", max_length=255, blank=True)
    address = models.TextField(verbose_name="Endereço", blank=True)

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = "Usuários"
