from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import CustomUserManager
from organization.models import Parking


class User(AbstractUser):
    email = models.EmailField(unique=True)
    identification = models.CharField(max_length=10)
    address= models.CharField(max_length=254, null=True, blank=True)
    phone = models.CharField(max_length=10, null=True, blank=True)
    state= models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']  # O los campos que consideres necesarios

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email  # Usar el correo como nombre de usuario
        super(User, self).save(*args, **kwargs)