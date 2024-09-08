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


