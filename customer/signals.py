from django.core.exceptions import ValidationError
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.utils import timezone

from accounting.models import Reservation
from customer.models import Vehicle


@receiver(pre_save, sender=Vehicle)
def create_vehicle(sender, instance: Vehicle, **kwargs):
    if not instance.pk:
        if Vehicle.objects.filter(plate=instance.plate).exists():
            raise ValidationError("Ya existe vehiculo")

