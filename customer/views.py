from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import Group
from .models import *
from rest_framework import permissions, viewsets

from .serializers import *


class ClientViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    # permission_classes = [permissions.IsAuthenticated]


class VehicleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

