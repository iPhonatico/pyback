from datetime import datetime

from django.core.exceptions import ValidationError
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.utils import timezone

from accounting.models import Reservation
from organization.models import ParkingSchedule, Parking  # Asegúrate de que los imports sean correctos


@receiver(post_save, sender=Reservation)
def update_parking_schedule_availability(sender, instance, created, **kwargs):
    """
    Esta señal se ejecuta cuando se crea o guarda una reserva.
    Si la reserva es creada y está activa, marcamos el horario como no disponible y reducimos la capacidad del parqueo.
    """
    if created and instance.state == 'A':  # Solo si la reserva está activa
        parking_schedule = instance.parkingSchedule
        parking_schedule.available = False  # Marcar el horario como no disponible
        parking_schedule.save()

        # Reducir la capacidad del parqueo en 1
        parking = instance.parking
        parking.actualCapacity -= 1
        parking.save()


@receiver(pre_save, sender=Reservation)
def check_availability_before_reservation(sender, instance, **kwargs):
    """
    Esta señal se ejecuta antes de guardar una reserva para verificar si el horario está disponible.
    Si el horario no está disponible o no hay capacidad en el parqueo, lanzamos un error.
    """
    # Solo verificar disponibilidad si la reserva está activa o se está creando
    if instance.state == 'A':
        parking_schedule = instance.parkingSchedule
        if not parking_schedule.available:
            raise ValueError("El horario seleccionado no está disponible.")

        # Verificar si el parqueo tiene capacidad disponible
        parking = instance.parking
        if parking.actualCapacity <= 0:
            raise ValueError("No hay capacidad disponible en el parqueo.")


@receiver(post_save, sender=Reservation)
def handle_reservation_cancellation(sender, instance, **kwargs):
    """
    Esta señal se ejecuta cuando se cancela una reserva. Si se cancela, liberamos el horario y aumentamos la capacidad.
    """
    if instance.state == 'C':  # Si la reserva está cancelada
        parking_schedule = instance.parkingSchedule
        parking_schedule.available = True  # Liberar el horario
        parking_schedule.save()

        # Aumentar la capacidad del parqueo en 1
        parking = instance.parking
        parking.actualCapacity += 1
        parking.save()


@receiver(post_save, sender=Reservation)
def handle_reservation_payment(sender, instance, **kwargs):
    """
    Esta señal se ejecuta cuando se paga una reserva. Si la reserva está pagada, aumentamos la capacidad del parqueo.
    """
    if instance.state == 'P':  # Si la reserva está pagada
        parking = instance.parking
        parking.actualCapacity += 1
        parking.save()