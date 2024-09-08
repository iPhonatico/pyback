from django.db import models

# Create your models here.
class Reservation(models.Model):
    state_choices = (("P","Payed"),("A","Active"),("C","Cancel"))

    payAmount = models.DecimalField(decimal_places=2, max_digits=5, default=0)
    state = models.CharField(max_length=1,default="A", choices=state_choices)
    parking = models.ForeignKey('organization.Parking', on_delete=models.CASCADE)
    #client = models.ForeignKey('customer.Client', on_delete=models.CASCADE, related_name="reservations", null=True, blank=True)
    vehicle = models.ForeignKey('customer.Vehicle', on_delete=models.CASCADE)
    parkingSchedule = models.ForeignKey('organization.ParkingSchedule', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.vehicle.plate)