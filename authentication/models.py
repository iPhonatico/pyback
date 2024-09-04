from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

from organization.models import Parking


class User(AbstractUser):    #heredo de abstract user
    email = models.EmailField(unique=True)
    parking = models.ForeignKey(Parking, on_delete=models.CASCADE, null=True)