from django.contrib import admin

from organization.models import Parking, Schedule, ParkingSchedule

# Register your models here.

admin.site.register(Parking)
admin.site.register(Schedule)
admin.site.register(ParkingSchedule)