from django.core.exceptions import ValidationError
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.utils import timezone

from accounting.models import Reservation


@receiver(post_save, sender=Reservation)
def create_reservation(sender, instance:Reservation, created, **kwargs):
    if instance.fechaHoraInicio < timezone.now():
        raise ValidationError("La reserva no puede iniciar en el pasado")
    if created and instance.parking.current_spaces > 0:
        instance.parking.current_spaces -= 1
        instance.parking.save()

    elif created:
        raise ValidationError("El parqueadero está lleno")

    # if created:
    #    print("Creado", instance)
    # else:
    #    print("Actualizado", instance)
    #

@receiver(pre_save, sender=Reservation)
def create_reservation(sender, instance: Reservation, **kwargs):
    old_reservation = Reservation.objects.get(id=instance.id)
    if old_reservation.state == "A" and instance.state == "P":
        print("se ha pagado la reserva")
        instance.parking.current_spaces += 1
        instance.parking.save()