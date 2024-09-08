from django.db import models
from django.core.exceptions import ValidationError
# Create your models here.

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

    def save(self, *args, **kwargs):
        # Al crear un nuevo horario, inicializar actualCapacity con la capacidad total del parqueo
        if not self.pk or self.actualCapacity == 0:
            self.actualCapacity = self.parking.capacity

        super().save(*args, **kwargs)

    def clean(self):
        overlapping_schedule = ParkingSchedule.objects.filter(
            date=self.date,
            parking=self.parking,
            schedule__start_time__lt=self.schedule.end_time,
            schedule__end_time__gt=self.schedule.start_time
        ).exclude(pk=self.pk)

        if overlapping_schedule.exists():
            raise ValidationError('El horario solapa con otro horario asignado a este parqueo.')

    def __str__(self):
        return f'{self.parking} - {self.schedule}'










