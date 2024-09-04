from django.contrib.auth.models import Group
from .models import *
from rest_framework import serializers



class VehicleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vehicle
        fields = "__all__"


class ClientSerializer(serializers.ModelSerializer):
    vehicles = VehicleSerializer(many=True, read_only=True) #puede tener muchos vehiculos
    class Meta:
        model = Client
        fields = "__all__"


