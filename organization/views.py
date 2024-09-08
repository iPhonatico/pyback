from sched import scheduler

from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import Group
from .models import Parking
from rest_framework import permissions, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets, filters

from .serializers import *
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from django.http import JsonResponse
class ParkingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Parking.objects.all()
    serializer_class = ParkingSerializer
    #permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    permission_classes = [IsAuthenticated, DjangoModelPermissions]



class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = SchedulingSerializer
    #permission_classes = [IsAuthenticated, DjangoModelPermissions]



class ParkingScheduleViewSet(viewsets.ModelViewSet):
    queryset = ParkingSchedule.objects.all()
    serializer_class = ParkingScheduleSerializer
    filter_backends = [DjangoFilterBackend]  # Activa los filtros
    filterset_fields = ['parking', 'schedule']  # Filtro por el campo 'parking'

    def recalculate_all_schedules(request):
        if request.method == "POST":
            # Obtener todos los horarios
            schedules = ParkingSchedule.objects.all()

            # Recalcular la capacidad para cada uno
            for schedule in schedules:
                schedule.recalculate_capacity()

            return JsonResponse({"status": "Capacidades recalculadas con éxito"}, status=200)

        return JsonResponse({"error": "Método no permitido"}, status=405)










