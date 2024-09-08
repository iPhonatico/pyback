from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from accounting.models import Reservation

@receiver(post_save, sender=Reservation)
def handle_reservation_change(sender, instance, created, **kwargs):
    parking_schedule = instance.parkingSchedule
    print(f"Reserva creada o modificada para el horario {parking_schedule.id}. Capacidad antes de la actualización: {parking_schedule.actualCapacity}")

    if created and instance.state == 'A':
        parking_schedule.actualCapacity -= 1
        print(f"Reserva creada. Capacidad después de la actualización: {parking_schedule.actualCapacity}")
    elif instance.state == 'C':
        parking_schedule.actualCapacity += 1
        print(f"Reserva cancelada. Capacidad después de la actualización: {parking_schedule.actualCapacity}")

    parking_schedule.save()

@receiver(post_delete, sender=Reservation)
def handle_reservation_delete(sender, instance, **kwargs):
    """
    Aumenta la capacidad del ParkingSchedule cuando se elimina una reserva activa.
    """
    if instance.state == 'A':  # Solo aumentar si la reserva estaba activa
        instance.parkingSchedule.actualCapacity += 1
        instance.parkingSchedule.save()
