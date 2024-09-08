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
    Esta señal se ejecuta antes de guardar una reserva para verificar si el parqueo tiene capacidad disponible en el horario seleccionado.
    """

    # Si la reserva es automática, ya debería haberse asignado el horario
    if instance.automatic and instance.parkingSchedule is not None:
        return  # No es necesario verificar la disponibilidad

    parking_schedule = instance.parkingSchedule

    if parking_schedule is None:
        raise ValidationError("No se ha seleccionado un horario válido para esta reserva.")

    # Contar cuántas reservas activas ya existen en este horario
    active_reservations = Reservation.objects.filter(
        parkingSchedule=parking_schedule, state='A'
    ).count()

    # Verificar si todavía hay espacio disponible en el parqueo
    if active_reservations >= instance.parking.capacity:
        raise ValidationError("El parqueo ya ha alcanzado su capacidad máxima para este horario.")

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