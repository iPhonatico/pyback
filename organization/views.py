from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import Group
from .models import Parking
from rest_framework import permissions, viewsets

from .serializers import *


class ParkingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Parking.objects.all()
    serializer_class = ParkingSerializer
    #permission_classes = [permissions.IsAuthenticated]

