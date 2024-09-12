from django.core.exceptions import ValidationError
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save, post_delete
from accounting.models import Reservation
from organization.models import ParkingSchedule


@receiver(pre_save, sender=Reservation)
def check_availability_before_reservation(sender, instance, **kwargs):
    """
    Esta señal se ejecuta antes de guardar una reserva para verificar si el parqueo tiene capacidad disponible en el horario seleccionado.
    """
    parking_schedule = instance.parkingSchedule

    if parking_schedule is None:
        raise ValidationError("No se ha seleccionado un horario válido para esta reserva.")

    # Contar cuántas reservas activas ya existen en este horario
    active_reservations = Reservation.objects.filter(
        parkingSchedule=parking_schedule, state='A'
    ).count()

    # Verificar si todavía hay espacio disponible en el parqueo
    if active_reservations >= parking_schedule.parking.capacity:
        raise ValidationError("El parqueo ya ha alcanzado su capacidad máxima para este horario.")


@receiver(post_save, sender=Reservation)
def update_parking_schedule_availability(sender, instance, created, **kwargs):
    """
    Esta señal se ejecuta cuando se crea o guarda una reserva.
    Si la reserva es creada y está activa, reducimos la capacidad del parqueo.
    """
    parking_schedule = instance.parkingSchedule

    if created and instance.state == 'A':  # Solo si la reserva está activa
        if parking_schedule.actualCapacity > 0:  # Verifica que la capacidad no sea negativa
            parking_schedule.actualCapacity -= 1
            parking_schedule.save()


@receiver(post_save, sender=Reservation)
def handle_reservation_cancellation(sender, instance, **kwargs):
    """
    Esta señal se ejecuta cuando se cancela una reserva. Si se cancela, liberamos el horario y aumentamos la capacidad.
    """
    parking_schedule = instance.parkingSchedule

    if instance.state == 'C':  # Si la reserva está cancelada
        if parking_schedule.actualCapacity < parking_schedule.parking.capacity:  # Verificar que no supere la capacidad máxima
            parking_schedule.actualCapacity += 1
            parking_schedule.save()


@receiver(post_delete, sender=Reservation)
def increase_capacity_on_reservation_delete(sender, instance, **kwargs):
    """
    Aumenta la capacidad del ParkingSchedule cuando se elimina una reserva activa.
    """
    parking_schedule = instance.parkingSchedule

    if instance.state == 'A':  # Solo aumentar si la reserva estaba activa
        if parking_schedule.actualCapacity < parking_schedule.parking.capacity:  # Verificar que no supere la capacidad máxima
            parking_schedule.actualCapacity += 1
            parking_schedule.save()
