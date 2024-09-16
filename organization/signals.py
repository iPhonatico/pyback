from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from accounting.models import Reservation


@receiver(post_save, sender=Reservation)
def handle_reservation_change(sender, instance, created, **kwargs):
    """
    Señal que se ejecuta cuando se crea o actualiza una reserva.
    Ajusta la capacidad del parking_schedule en función del estado de la reserva.
    """
    parking_schedule = instance.parkingSchedule
    print(f"Post_save signal triggered for Reservation ID: {instance.id}, Created: {created}, State: {instance.state}")

    # Si la reserva fue creada y está activa (estado 'A'), reduce la capacidad
    if created and instance.state == 'A':
        print(f"Reserva activa creada. Capacidad antes de la actualización: {parking_schedule.actualCapacity}")
        parking_schedule.actualCapacity -= 1
        print(f"Reserva activa creada. Capacidad después de la actualización: {parking_schedule.actualCapacity}")

    # Si la reserva fue actualizada a cancelada (estado 'C'), aumenta la capacidad
    elif not created and instance.state == 'C':
        print(f"Reserva cancelada. Capacidad antes de la actualización: {parking_schedule.actualCapacity}")
        parking_schedule.actualCapacity += 1
        print(f"Reserva cancelada. Capacidad después de la actualización: {parking_schedule.actualCapacity}")

    # Guarda los cambios en el parking_schedule
    parking_schedule.save()


@receiver(post_delete, sender=Reservation)
def handle_reservation_delete(sender, instance, **kwargs):
    """
    Señal que se ejecuta cuando se elimina una reserva.
    Solo aumenta la capacidad si la reserva eliminada estaba activa (estado 'A').
    """
    parking_schedule = instance.parkingSchedule

    print(f"Post_delete signal triggered for Reservation ID: {instance.id}, State: {instance.state}")

    # Solo aumentar capacidad si la reserva estaba activa ('A')
    if instance.state == 'A':
        parking_schedule.actualCapacity += 1
        parking_schedule.save()
        print(f"Reserva eliminada. Capacidad después de la eliminación: {parking_schedule.actualCapacity}")