from django.db import models
from django.core.exceptions import ValidationError
# Create your models here.

from accounting.models import Reservation

class Parking(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    capacity = models.PositiveIntegerField(default=0)  # Capacidad total del parqueo
    fee = models.DecimalField(decimal_places=2, max_digits=5)
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE, null=True, blank=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name} - {self.address} (Capacidad: {self.capacity})'





class Schedule(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()

    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError('La hora de inicio debe ser antes de la hora de fin')

    def __str__(self):
        return f'{self.start_time} - {self.end_time}'



class ParkingSchedule(models.Model):
    date = models.DateField()
    parking = models.ForeignKey('organization.Parking', on_delete=models.CASCADE)
    schedule = models.ForeignKey('organization.Schedule', on_delete=models.CASCADE)
    actualCapacity = models.PositiveIntegerField(default=0)  # Capacidad actual para este horario específico

    def recalculate_capacity(self):
        """
        Recalcula la capacidad actual restando las reservas activas en este horario.
        """
        active_reservations = Reservation.objects.filter(parkingSchedule=self, state='A').count()
        self.actualCapacity = self.parking.capacity - active_reservations
        self.save()

    def save(self, *args, **kwargs):
        # Inicializar la capacidad actual con la capacidad total del parqueo solo al crear un nuevo registro
        if not self.pk:  # Solo cuando se crea el objeto
            self.actualCapacity = self.parking.capacity

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.parking} - {self.schedule}'









