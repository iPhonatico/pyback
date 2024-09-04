from django.db import models

# Create your models here.
class Reservation(models.Model):
    state_choices = (("P","Payed"),("A","Active"),("C","Cancel"))

    fechaHoraInicio = models.DateTimeField()
    fechaHoraFin = models.DateTimeField()
    state = models.CharField(max_length=1,default="A", choices=state_choices)
    parking = models.ForeignKey('organization.Parking', on_delete=models.CASCADE)
    client = models.ForeignKey('customer.Client', on_delete=models.CASCADE)
    vehicle = models.ForeignKey('customer.Vehicle', on_delete=models.CASCADE)

