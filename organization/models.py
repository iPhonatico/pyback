from django.db import models
from django.core.exceptions import ValidationError
# Create your models here.

class Parking(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    capacity = models.PositiveIntegerField(default=0)
    actualCapacity = models.PositiveIntegerField()  # Capacidad actual del parqueo
    fee = models.DecimalField(decimal_places=2, max_digits=5)
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE, null=True, blank=True)
    available = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        # Al crear un nuevo parqueo, inicializar actualCapacity con la capacidad total si está vacío
        if not self.pk or self.actualCapacity == 0:  # Si es un parqueo nuevo o la capacidad actual es 0
            self.actualCapacity = self.capacity

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} - {self.address} ({self.actualCapacity}/{self.capacity} disponibles)'



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
    #available = models.BooleanField(default=True)  # Puedes eliminar este campo si ya no es necesario

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










