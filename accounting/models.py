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

        super().save(*args, **kwargs)

    def pay_reservation(self):
        # Actualiza el estado a "Payed" y aumenta la capacidad del parqueo en 1
        if self.state == 'A':
            self.state = 'P'
            self.parking.actualCapacity += 1
            self.parking.save()
            self.save()

    def cancel_reservation(self):
        # Cambia el estado a "Cancel" sin modificar la capacidad del parqueo
        self.state = 'C'
        self.save()

    def get_user_from_plate(self):
        """
        Obtiene el usuario basado en el vehículo (que está relacionado con el usuario) usando la placa.
        """
        return self.vehicle.owner  # Asumiendo que 'owner' es el campo que relaciona vehículo con el usuario

    def __str__(self):
        return f'Reserva de {self.vehicle.plate} en {self.parking.name}'
