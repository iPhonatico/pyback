from django.contrib.auth.models import Group

from accounting.models import Reservation
from accounting.serializers import ReservationSerializer
from .models import *
from rest_framework import serializers



class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = "__all__"
    extra_fields = ['user_id']  # Añadir campo adicional

    def get_user_id(self, obj):
        return obj.user.id if obj.user else None

    def update(self, instance, validated_data):
        # Guardar el estado anterior del vehículo antes de actualizar
        old_status = instance.status
        new_status = validated_data.get('status', instance.status)

        # Actualizar los datos del vehículo
        instance = super().update(instance, validated_data)

        # Verificar si el estado cambió de True a False
        if old_status and not new_status:
            # Si el estado cambió de True a False, cancelar las reservas activas
            active_reservations = Reservation.objects.filter(vehicle=instance, state='A')

            for reservation in active_reservations:
                # Cambiar el estado de la reserva a 'C' (cancelado)
                reservation.state = 'C'
                reservation.save()

                # Nota: No incrementamos actualCapacity aquí, porque ya se hace en las señales

        return instance
    # def create(self, validated_data):
    #     validated_data['password'] = make_password(validated_data['password'])
    #     return super(ClientSerializer, self).create(validated_data)


