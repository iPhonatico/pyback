from sched import scheduler

from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import Group
from .models import Parking
from rest_framework import permissions, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets, filters

from .serializers import *

class ParkingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Parking.objects.all()
    serializer_class = ParkingSerializer
    #permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']



class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = SchedulingSerializer



class ParkingScheduleViewSet(viewsets.ModelViewSet):
    queryset = ParkingSchedule.objects.all()
    serializer_class = ParkingSlotSerializer






