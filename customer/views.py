from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import Group

from django_filters.rest_framework import DjangoFilterBackend

from .models import *
from rest_framework import permissions, viewsets, filters

from .serializers import *


class ClientViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['email']
    search_fields = ['name']


class ClientByVehicleViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientByVehicleSerializer


class VehicleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import Group

from django_filters.rest_framework import DjangoFilterBackend

from .models import *
from rest_framework import permissions, viewsets, filters

from .serializers import *


class ClientViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    #PARA LEVANTAR AUTENTICACIÓNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['email']
    search_fields = ['name']



class VehicleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['color']
    filterset_fields = ['plate']



