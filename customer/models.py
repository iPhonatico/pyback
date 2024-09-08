from django.db import models
from django.contrib.auth.hashers import make_password

# Create your models here.

class Client(models.Model):
    name = models.CharField(max_length=100)
    identification = models.CharField(max_length=10)
    address = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=10, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    state = models.BooleanField(default=True)
    parking = models.ForeignKey('organization.Parking', on_delete=models.CASCADE)
    vehicles = models.ManyToManyField('customer.Vehicle')
    password = models.CharField(max_length=128, null=True, blank=True, default="password")

    def __str__(self):  #para que aparezca el nombre en el admin
        return self.name
    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)
        super(Client, self).save(*args, **kwargs)




class Vehicle(models.Model):
    plate = models.CharField(max_length=10)
    color = models.CharField(max_length=100)
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE, null=True, blank=True)
    #parking = models.ForeignKey('authentication.User', on_delete=models.CASCADE)



    def __str__(self):  #para que aparezca el nombre en el admin
        return self.plate

