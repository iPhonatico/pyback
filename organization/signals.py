from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from accounting.models import Reservation

@receiver(post_save, sender=Reservation)
def handle_reservation_change(sender, instance, created, **kwargs):
    """
    Recalcula la capacidad del ParkingSchedule cuando se crea o cancela una reserva.
    """
    parking_schedule = instance.parkingSchedule

    if created and instance.state == 'A':
        # Si la reserva es nueva y activa, reduce la capacidad
        parking_schedule.actualCapacity -= 1
    elif instance.state == 'C':
        # Si la reserva es cancelada, aumenta la capacidad
        parking_schedule.actualCapacity += 1

    parking_schedule.save()


@receiver(post_delete, sender=Reservation)
def handle_reservation_delete(sender, instance, **kwargs):
    """
    Aumenta la capacidad del ParkingSchedule cuando se elimina una reserva activa.
    """
    if instance.state == 'A':  # Solo aumentar si la reserva estaba activa
        instance.parkingSchedule.actualCapacity += 1
        instance.parkingSchedule.save()