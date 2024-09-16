from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.



class Vehicle(models.Model):
    plate = models.CharField(max_length=10)
    color = models.CharField(max_length=100, null=True, blank=True)
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE, null=True, blank=True)
    status = models.BooleanField(default=True, null=True, blank=True)




    def __str__(self):  #para que aparezca el nombre en el admin
        return self.plate

