from django.db import models

# Create your models here.

class Parking(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    capacity = models.PositiveIntegerField(default=0)
    morning_fee = models.DecimalField(decimal_places=2, max_digits=5)
    evening_fee = models.DecimalField(decimal_places=2, max_digits=5, null=True, blank=True)
    current_spaces = models.PositiveIntegerField(default=0)

    def __str__(self):  #para que aparezca el nombre en el admin
        return self.name
