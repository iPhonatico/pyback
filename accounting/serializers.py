import requests
from django.conf import settings
from django.contrib.auth.models import Group
from django.template.defaultfilters import length

from customer.models import Vehicle
from organization.models import Parking, Schedule
from .models import *
from rest_framework import serializers
from django.utils import timezone
from datetime import datetime



class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = "__all__"


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'

    def create(self, validated_data):
        vehicle_data = {}
        if "vehicle" in validated_data:
            vehicle_data = validated_data.pop('vehicle')
        elif "automatic" in validated_data and validated_data["automatic"]:
            validated_data.pop("automatic")
            plate_domain = getattr(settings, "PLATE_RECOGNIZER_URI")

            response = requests.get(plate_domain + "/leer_placa")
            plate_result = response.json()
            print(plate_result)
            if "results" in plate_result and len(plate_result["results"]) > 0:
                vehicle_data["plate"] = plate_result["results"][0]["plate"]
                vehicle_data["color"] = "sin color"
            else:
                raise serializers.ValidationError({"msg": "no se pudo encontrar placa"})
        else:
            raise serializers.ValidationError("Debe proveer la placa del vehículo")

        vehicle = Vehicle.objects.filter(plate=vehicle_data["plate"]).last()
        if vehicle is None:
            vehicle = Vehicle.objects.create(**vehicle_data)

        parking_id = validated_data.get("parking")
        if not parking_id:
            raise serializers.ValidationError("Debe proveer el ID del parking")

        parking = Parking.objects.get(id=parking_id)
        current_time = timezone.now()

        # Verificar si hay espacio disponible
        schedules = Schedule.objects.filter(parking=parking, start_time__lte=current_time, end_time__gte=current_time)
        space_available = False

        for schedule in schedules:
            if schedule.reservations.count() < parking.capacity:
                space_available = True
                validated_data['schedule'] = schedule
                break

        if not space_available:
            raise serializers.ValidationError("No hay espacio disponible en el parking en este momento")

        return Reservation.objects.create(vehicle=vehicle, **validated_data)









