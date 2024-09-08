import requests
from django.conf import settings
from rest_framework import serializers
from customer.models import Vehicle
from organization.models import Parking
from .models import Reservation
from django.utils import timezone
from organization.models import ParkingSchedule


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = "__all__"


class ReservationSerializer(serializers.ModelSerializer):
    vehicle = VehicleSerializer(required=False)
    automatic = serializers.BooleanField(required=False, write_only=True)

    class Meta:
        model = Reservation
        fields = "__all__"

    def create(self, validated_data):
        vehicle_data = {}

        # Verifica si se ha proporcionado un vehículo o si debe usarse el reconocimiento automático
        if "vehicle" in validated_data:
            vehicle_data = validated_data.pop('vehicle')
        elif "automatic" in validated_data and validated_data["automatic"]:
            # Si se usa el reconocimiento automático, eliminar el campo 'automatic'
            validated_data.pop("automatic")
            plate_domain = getattr(settings, "PLATE_RECOGNIZER_URI")

            try:
                # Realiza la solicitud al servicio externo para reconocimiento de placas
                response = requests.get(f"{plate_domain}/leer_placa")
                response.raise_for_status()  # Levanta una excepción si la respuesta HTTP es un error
                plate_result = response.json()

                if "results" in plate_result and len(plate_result["results"]) > 0:
                    # Extrae la placa del primer resultado y asigna un color predeterminado
                    vehicle_data["plate"] = plate_result["results"][0]["plate"]
                    vehicle_data["color"] = "sin color"
                else:
                    raise serializers.ValidationError({"msg": "No se pudo encontrar la placa"})
            except requests.RequestException as e:
                # Maneja cualquier error relacionado con la solicitud HTTP
                raise serializers.ValidationError({"msg": f"Error al comunicarse con el servicio de placas: {str(e)}"})
        else:
            raise serializers.ValidationError("Debe proporcionar el vehículo o usar reconocimiento automático.")

        # Busca o crea el vehículo basado en la placa
        vehicle = Vehicle.objects.filter(plate=vehicle_data.get("plate")).last()
        if vehicle is None:
            vehicle = Vehicle.objects.create(**vehicle_data)

        # Crea la reserva con los datos validados y el vehículo encontrado o creado
        return Reservation.objects.create(vehicle=vehicle, **validated_data)

    def update(self, instance, validated_data):
        # Actualización de la reserva, pero ignora el vehículo
        if "vehicle" in validated_data:
            vehicle_data = validated_data.pop("vehicle")

            # Actualiza el vehículo si es necesario (si tienes una lógica específica para esto)
            vehicle = Vehicle.objects.filter(plate=vehicle_data.get("plate")).last()
            if vehicle is None:
                vehicle = Vehicle.objects.create(**vehicle_data)
            instance.vehicle = vehicle

        # Actualiza los otros campos de la reserva
        return super().update(instance, validated_data)


class AutomaticReservationSerializer(serializers.ModelSerializer):
    plate = serializers.CharField(write_only=True)
    color = serializers.CharField(write_only=True)
    parking = serializers.PrimaryKeyRelatedField(queryset=Parking.objects.all())
    automatic = serializers.BooleanField(default=True)

    class Meta:
        model = Reservation
        fields = ['plate', 'color', 'parking', 'automatic']

    def validate(self, data):
        plate = data.get('plate').strip().upper()
        parking = data.get('parking')

        # Buscar o crear el vehículo por la placa
        vehicle, created = Vehicle.objects.get_or_create(plate=plate, defaults={'color': data.get('color')})

        # Obtener la hora actual
        now = timezone.now().time()
        print(f"Hora actual: {now}")  # Para depuración, elimina esto después

        # Verificar si hay un horario con capacidad disponible para el parqueo
        current_schedule = ParkingSchedule.objects.filter(
            parking=parking,
            schedule__start_time__lte=now,
            schedule__end_time__gte=now,
            actualCapacity__gt=0  # Asegúrate de que haya capacidad en el horario
        ).first()

        if not current_schedule:
            raise serializers.ValidationError("No hay horarios disponibles en este momento.")

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
            state="A",  # Reserva en estado activo
            payAmount=validated_data['parking'].fee  # Calcular el monto automáticamente
        )
        return reservation