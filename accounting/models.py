from django.db import models
from django.core.exceptions import ValidationError

class Reservation(models.Model):
    state_choices = (("P", "Payed"), ("A", "Active"), ("C", "Cancel"))

    payAmount = models.DecimalField(decimal_places=2, max_digits=5, default=0)
    state = models.CharField(max_length=1, default="A", choices=state_choices)
    parking = models.ForeignKey('organization.Parking', on_delete=models.CASCADE)
    vehicle = models.ForeignKey('customer.Vehicle', on_delete=models.CASCADE)  # El usuario se obtiene del vehículo
    parkingSchedule = models.ForeignKey('organization.ParkingSchedule', on_delete=models.CASCADE, null=True, blank=True)
    automatic = models.BooleanField(default=False)

    def clean(self):
        # Verifica si ya existe una reserva para el mismo vehículo y horario
        overlapping_reservation = Reservation.objects.filter(
            vehicle=self.vehicle,
            parkingSchedule=self.parkingSchedule
        ).exclude(pk=self.pk)

        if overlapping_reservation.exists():
            raise ValidationError('Este vehículo ya tiene una reserva en este horario.')

    def calculate_payment(self):
        # Calcula el pago basado en la tarifa del parqueo
        return self.parking.fee

    def save(self, *args, **kwargs):
        # Si no se ha especificado el monto a pagar, usar la tarifa del parqueo
        if not self.payAmount:
            self.payAmount = self.calculate_payment()
        print(f"Se está llamando a save() para la reserva. ID: {self.id}, Estado: {self.state}")
        super().save(*args, **kwargs)

    def pay_reservation(self):
        """
        Marca la reserva como pagada si está activa y guarda los cambios.
        """
        if self.state == 'A':  # Solo si la reserva está activa
            self.state = 'P'
            self.save()  # Al guardar, la señal se activará para liberar espacio en el parqueo
        else:
            raise ValidationError("Solo las reservas activas pueden ser pagadas.")



    def cancel_reservation(self):
        """
        Cancela la reserva cambiando su estado a "C" (Cancel) y ejecuta las señales correspondientes
        para liberar la capacidad del parqueo y el horario.
        """
        if self.state == "A":  # Solo las reservas activas pueden ser canceladas
            self.state = "C"
            self.save()  # Al guardar, la señal se activará para liberar el horario y la capacidad
        else:
            raise ValidationError("Solo las reservas activas pueden ser canceladas.")


    def __str__(self):
        return f'Reserva de {self.vehicle.plate} en {self.parking.name}'