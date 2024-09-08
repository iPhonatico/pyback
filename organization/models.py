from django.db import models

# Create your models here.

class Parking(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    capacity = models.PositiveIntegerField(default=0)
    fee = models.DecimalField(decimal_places=2, max_digits=5)
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE, null=True, blank=True)
    available = models.BooleanField(default=True)
    def __str__(self):  #para que aparezca el nombre en el admin
        return self.name

class Schedule(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return str(self.start_time) + " - " + str(self.end_time)

class ParkingSchedule(models.Model):
    date = models.DateField()
    parking = models.ForeignKey('organization.Parking', on_delete=models.CASCADE)
    schedule = models.ForeignKey('organization.Schedule', on_delete=models.CASCADE)
    available = models.BooleanField(default=True)
    def __str__(self):
        return str(self.parking) + " - " + str(self.schedule)









