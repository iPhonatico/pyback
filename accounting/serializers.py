from django.contrib.auth.models import Group

from customer.models import Vehicle
from .models import *
from rest_framework import serializers


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = "__all__"


class ReservationSerializer(serializers.ModelSerializer):
    vehicle = VehicleSerializer()

    class Meta:
        model = Reservation
        fields = "__all__"

    def create(self, validated_data):
        vehicle_data = validated_data.pop('vehicle')
        print(vehicle_data)
        vehicle = Vehicle.objects.filter(plate=vehicle_data["plate"]).last()
        if vehicle is None:
            vehicle = Vehicle.objects.create(**vehicle_data)

        return Reservation.objects.create(vehicle=vehicle, **validated_data)

    def update(self, instance, validated_data):
        vehicle_data = validated_data.pop('vehicle')

        return super().update(instance, validated_data)







