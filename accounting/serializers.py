import requests
from django.conf import settings
from rest_framework import serializers

from authentication.serializers import UserSerializer
from customer.models import Vehicle
from organization.models import Parking
from organization.serializers import ParkingSerializer
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
    automatic = serializers.BooleanField(required=False, default=False)
    parking = ParkingSerializer(read_only=True)  # Relación con el modelo Parking
    schedule_time = serializers.SerializerMethodField()  # Para mostrar la fecha y la hora del horario
    user = serializers.SerializerMethodField()  # Para mostrar la información del usuario

    class Meta:
        model = Reservation
        fields = ['id', 'payAmount', 'state', 'parking', 'vehicle', 'parkingSchedule', 'automatic', 'schedule_time', 'user']

    def get_schedule_time(self, obj):
        return {
            "date": obj.parkingSchedule.date,
            "start_time": obj.parkingSchedule.schedule.start_time,
            "end_time": obj.parkingSchedule.schedule.end_time
        }

    def get_user(self, obj):
        if obj.vehicle and obj.vehicle.user:
            return {
                "id": obj.vehicle.user.id,
                "first_name": obj.vehicle.user.first_name,
                "last_name": obj.vehicle.user.last_name,
                "email": obj.vehicle.user.email,
                "identification": obj.vehicle.user.identification,
                "address": obj.vehicle.user.address,
                "phone": obj.vehicle.user.phone
            }
        return None

    def validate(self, data):
        vehicle_data = data.get('vehicle')
        parking_schedule = data.get('parkingSchedule')

        # Verifica si el vehículo tiene el estado activo
        vehicle = Vehicle.objects.filter(plate=vehicle_data.get('plate')).last()
        if vehicle is None:
            raise serializers.ValidationError("El vehículo no existe.")
        if not vehicle.status:
            raise serializers.ValidationError("No se pueden realizar reservaciones con un vehículo deshabilitado.")

        # Verificar si ya existe una reserva activa o pagada
        existing_reservation = Reservation.objects.filter(
            vehicle=vehicle,
            parkingSchedule=parking_schedule,
            state__in=['A', 'P']  # Activo o pagado
        ).exists()
        if existing_reservation:
            raise serializers.ValidationError("Ya existe una reserva activa o pagada para este vehículo en este horario.")

        # Validar la capacidad disponible en el horario (si el schedule tiene capacidad)
        if parking_schedule.actualCapacity <= 0:
            raise serializers.ValidationError("No hay capacidad disponible para este horario.")

        return data

    def create(self, validated_data):
        vehicle_data = validated_data.pop('vehicle')
        vehicle = Vehicle.objects.get_or_create(plate=vehicle_data['plate'], defaults=vehicle_data)[0]

        # Crear la reserva sin tocar la capacidad, eso será manejado por la señal
        reservation = Reservation.objects.create(vehicle=vehicle, **validated_data)
        return reservation


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


        return reservation