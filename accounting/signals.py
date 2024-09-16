from django.core.exceptions import ValidationError
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save, post_delete
from accounting.models import Reservation
from organization.models import ParkingSchedule

