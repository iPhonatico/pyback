from django.contrib.auth.models import Group

from accounting.serializers import ReservationSerializer
from .models import *
from rest_framework import serializers



class VehicleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vehicle
        fields = "__all__"


class ClientByVehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = "nombre"




class ClientSerializer(serializers.ModelSerializer):
    vehicles = VehicleSerializer(many=True, read_only=True) #puede tener muchos vehiculos
    reservations = ReservationSerializer(many=True, read_only=True)
    class Meta:
        model = Client
        fields = "__all__"

    def update(self, instance, validated_data):


        # Asumiendo que hay una lógica específica para manejar el campo 'status'
        status_data = validated_data.pop('status', None)
        instance = super(ClientSerializer, self).update(instance, validated_data)

        # Procesar el campo 'status' si es necesario
        if status_data:
            instance.status = status_data
            instance.save()

        return instance



