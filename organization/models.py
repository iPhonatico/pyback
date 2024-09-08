from django.db import models

# Create your models here.

class Parking(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    capacity = models.PositiveIntegerField(default=0)
    fee = models.DecimalField(decimal_places=2, max_digits=5)
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE, null=True, blank=True)


# class Schedule(models.Model):
#     start_timer = models.TimeField()
#     end_time = models.TimeField()
#
# class Horario_Parking(models.Model):
#     date = models.DateField()
#     capacity_available = models.PositiveIntegerField(default=0)
#     parking = models.ForeignKey('organization.Parking', on_delete=models.CASCADE)
#     horario = models.ForeignKey('organization.Horarios', on_delete=models.CASCADE)
#
#
#





    def __str__(self):  #para que aparezca el nombre en el admin
        return self.name
