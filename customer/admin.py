from django.contrib import admin

from customer.models import Client, Vehicle

# Register your models here.

admin.site.register(Client)
admin.site.register(Vehicle)