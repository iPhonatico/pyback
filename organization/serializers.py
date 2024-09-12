from django.contrib.auth.models import Group


from authentication.serializers import UserSerializer
from .models import *
from rest_framework import serializers





class ParkingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parking
        fields = '__all__'




class SchedulingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'


class ParkingScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingSchedule
        fields = ['date', 'parking', 'schedule', 'actualCapacity']

    def validate(self, data):
        parking = data.get('parking')
        schedule = data.get('schedule')
        date = data.get('date')

        # Verificar si ya existe un ParkingSchedule con los mismos parking y schedule para la misma fecha
        if ParkingSchedule.objects.filter(parking=parking, schedule=schedule, date=date).exists():
            raise serializers.ValidationError("Ya existe un horario para este parqueo en esta fecha y horario.")

        return data

