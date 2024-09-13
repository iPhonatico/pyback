import requests
from django.conf import settings
from rest_framework import serializers
from customer.models import Vehicle
from organization.models import Parking
from .models import Reservation
from django.utils import timezone
from organization.models import ParkingSchedule
from datetime import timedelta


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = "__all__"
    extra_fields = ['user_id']  # Añadir campo adicional

    def get_user_id(self, obj):
        # Accede al usuario relacionado con el vehículo
        return obj.vehicle.user.id if obj.vehicle.user else None


class ReservationSerializer(serializers.ModelSerializer):
    vehicle = VehicleSerializer(required=False)
    automatic = serializers.BooleanField(required=False, default=False)  # Por defecto es False

    class Meta:
        model = Reservation
        fields = "__all__"

    def validate(self, data):
        vehicle_data = data.get('vehicle')

        # Verifica que el vehículo esté en los datos
        if vehicle_data is None:
            raise serializers.ValidationError("Debe proporcionar el vehículo.")

        # Busca el vehículo en la base de datos
        vehicle = Vehicle.objects.filter(plate=vehicle_data.get('plate')).last()
        if vehicle is None:
            raise serializers.ValidationError("El vehículo no existe.")

        # Verificar si ya existe una reserva activa o pagada para este vehículo en el mismo ParkingSchedule
        parking_schedule = data.get('parkingSchedule')
        existing_reservation = Reservation.objects.filter(
            vehicle=vehicle,
            parkingSchedule=parking_schedule,
            state__in=['A', 'P']  # Activo o pagado
        ).exists()

        if existing_reservation:
            raise serializers.ValidationError(
                "Ya existe una reserva activa o pagada para este vehículo en el mismo horario."
            )

        # Validar la capacidad disponible en el horario
        if parking_schedule.actualCapacity <= 0:
            raise serializers.ValidationError("No hay capacidad disponible para este horario.")

        return data

    def create(self, validated_data):
        vehicle_data = validated_data.pop('vehicle')
        vehicle = Vehicle.objects.get_or_create(plate=vehicle_data['plate'], defaults=vehicle_data)[0]

        # Crear la reserva manualmente y reducir la capacidad
        reservation = Reservation.objects.create(
            vehicle=vehicle,
            **validated_data
        )

        # Reducir la capacidad del parkingSchedule
        parking_schedule = validated_data.get('parkingSchedule')
        parking_schedule.actualCapacity -= 1
        parking_schedule.save()

        return reservation

    def update(self, instance, validated_data):
        if "vehicle" in validated_data:
            vehicle_data = validated_data.pop("vehicle")
            vehicle = Vehicle.objects.filter(plate=vehicle_data.get("plate")).last()
            if vehicle is None:
                vehicle = Vehicle.objects.create(**vehicle_data)
            instance.vehicle = vehicle

        return super().update(instance, validated_data)


class AutomaticReservationSerializer(serializers.ModelSerializer):
    plate = serializers.CharField(write_only=True)
    parking = serializers.PrimaryKeyRelatedField(queryset=Parking.objects.all())
    automatic = serializers.BooleanField(default=True)

    class Meta:
        model = Reservation
        fields = ['plate', 'parking', 'automatic']

    def validate(self, data):
        plate = data.get('plate').strip().upper()
        parking = data.get('parking')

        # Buscar o crear el vehículo por la placa
        vehicle, created = Vehicle.objects.get_or_create(plate=plate)

        # Obtener la hora actual (ajustar según la zona horaria)
        now = timezone.now() - timedelta(hours=5)
        now_time = now.time()

        # Verificar si hay un horario disponible para el parqueo
        current_schedule = ParkingSchedule.objects.filter(
            parking=parking,
            schedule__start_time__lte=now_time,
            schedule__end_time__gte=now_time,
            actualCapacity__gt=0
        ).first()

        if not current_schedule:
            raise serializers.ValidationError("No hay horarios disponibles en este momento.")

        # Verificar si ya existe una reserva para este vehículo en el mismo horario
        last_reservation = Reservation.objects.filter(
            vehicle=vehicle,
            parkingSchedule=current_schedule,
            state__in=['A', 'P']  # Activo o pagado
        ).exists()

        # No permitir otra reserva si ya existe una activa o pagada
        if last_reservation:
            raise serializers.ValidationError(
                "Ya existe una reserva activa o pagada para este vehículo en el mismo horario."
            )

        # Asignar el vehículo y el horario actual a los datos
        data['vehicle'] = vehicle
        data['parkingSchedule'] = current_schedule
        return data

    def create(self, validated_data):
        # Crear la reserva automáticamente
        reservation = Reservation.objects.create(
            vehicle=validated_data['vehicle'],
            parking=validated_data['parking'],
            parkingSchedule=validated_data['parkingSchedule'],
            automatic=True,
            state="A",  # Estado Activo
            payAmount=validated_data['parking'].fee
        )

        # Reducir la capacidad del parkingSchedule
        parking_schedule = validated_data.get('parkingSchedule')
        parking_schedule.actualCapacity -= 1
        parking_schedule.save()

        return reservation