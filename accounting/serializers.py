import requests
from django.conf import settings
from django.contrib.auth.models import Group
from django.template.defaultfilters import length

from customer.models import Vehicle
from .models import *
from rest_framework import serializers


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = "__all__"


class ReservationSerializer(serializers.ModelSerializer):
    vehicle = VehicleSerializer(required=False)
    automatic = serializers.BooleanField(required=False,write_only=True)

    class Meta:
        model = Reservation
        fields = "__all__"

    def create(self, validated_data):

        vehicle_data = {}
        if "vehicle" in validated_data:
            vehicle_data = validated_data.pop('vehicle')
        elif "automatic" in validated_data and validated_data["automatic"]:
            validated_data.pop("automatic")
            plate_domain = getattr(settings, "PLATE_RECOGNIZER_URI")

            response = requests.get(plate_domain+"/leer_placa")
            plate_result = response.json()
            print(plate_result)
            if "results" in plate_result and len(plate_result["results"]) > 0:
                vehicle_data["plate"] = plate_result["results"][0]["plate"]
                vehicle_data["color"] = "sin color"
            else:
                raise serializers.ValidationError({"msg":"no se pudo encontrar placa"})
        else:
            raise serializers.ValidationError("Debe proveer el placa del vehiculo")

        vehicle = Vehicle.objects.filter(plate=vehicle_data["plate"]).last()
        if vehicle is None:
            vehicle = Vehicle.objects.create(**vehicle_data)

        return Reservation.objects.create(vehicle=vehicle, **validated_data)

    def update(self, instance, validated_data):
        vehicle_data = validated_data.pop('vehicle')

        return super().update(instance, validated_data)

    def validate(self, data):
        # Verificar si el vehículo con la placa especificada existe
        plate = data.get('plate')
        try:
            vehicle = Vehicle.objects.get(plate=plate)
            data['vehicle'] = vehicle  # Asignar el vehículo al campo vehicle
        except Vehicle.DoesNotExist:
            raise serializers.ValidationError("El vehículo con la placa proporcionada no existe.")

        return data









