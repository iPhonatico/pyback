from datetime import datetime

from django.core.exceptions import ValidationError
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.utils import timezone

from accounting.models import Reservation


@receiver(post_save, sender=Reservation)
def create_reservation_post(sender, instance:Reservation, created, **kwargs):
    if created and instance.parkingSchedule.date < timezone.now().date():
        raise ValidationError("La reserva no puede iniciar en el pasado")
    if created and instance.parking.available > 0:
        instance.parking.available -= 1
        instance.parking.save()

    elif created:
        raise ValidationError("El parqueadero está lleno")

    # if created:
    #    print("Creado", instance)
    # else:
    #    print("Actualizado", instance)
    #

@receiver(pre_save, sender=Reservation)
def create_reservation_pre(sender, instance: Reservation, **kwargs):
    if instance.pk:
        old_reservation = Reservation.objects.get(id=instance.id)
        if old_reservation.state == "A" and instance.state == "P":
            print("se ha pagado la reserva")
            instance.parking.current_spaces += 1
            instance.parking.save()
    else:

        print(instance.state)
        last = Reservation.objects.filter(vehicle__plate=instance.vehicle.plate).last()
        if instance.state == "A" and last and last.state == "A":
            raise ValidationError("Ya existe una reserva activa para este vehiculo")