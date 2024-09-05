from django.db import models

# Create your models here.

class Client(models.Model):
    name = models.CharField(max_length=100)
    indentification = models.CharField(max_length=10)
    address = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=10, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)

    parking = models.ForeignKey('organization.Parking', on_delete=models.CASCADE)
    vehicles = models.ManyToManyField('customer.Vehicle')

    def __str__(self):  #para que aparezca el nombre en el admin
        return self.name




class Vehicle(models.Model):
    plate = models.CharField(max_length=10)
    color = models.CharField(max_length=100)


    def __str__(self):  #para que aparezca el nombre en el admin
        return self.plate

