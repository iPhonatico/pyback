from django.db import models


# Create your models here.



class Vehicle(models.Model):
    plate = models.CharField(max_length=10)
    color = models.CharField(max_length=100)
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE, null=True, blank=True)




    def __str__(self):  #para que aparezca el nombre en el admin
        return self.plate

