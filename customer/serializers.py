from django.contrib.auth.models import Group

from accounting.serializers import ReservationSerializer
from .models import *
from rest_framework import serializers



class VehicleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vehicle
        fields = "__all__"



    # def create(self, validated_data):
    #     validated_data['password'] = make_password(validated_data['password'])
    #     return super(ClientSerializer, self).create(validated_data)


