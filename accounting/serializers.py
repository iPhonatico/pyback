from django.contrib.auth.models import Group
from .models import *
from rest_framework import serializers

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = "__all__"


