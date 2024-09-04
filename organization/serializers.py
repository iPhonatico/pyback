from django.contrib.auth.models import Group
from .models import *
from rest_framework import serializers

class ParkingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parking
        fields = '__all__'


