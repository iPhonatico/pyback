from datetime import timezone
from sched import scheduler

from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import Group
from .models import Parking
from rest_framework import permissions, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone

from .serializers import *
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from django.http import JsonResponse
from .filters import ParkingFilter
from rest_framework import status

class ParkingViewSet(viewsets.ModelViewSet):
    queryset = Parking.objects.all()
    serializer_class = ParkingSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ParkingFilter
    search_fields = ['name']
    filterset_fields = ['parking', 'schedule']  # Filtro por el campo 'parking'


    @action(detail=True, methods=['get'])
    def available_schedules(self, request, pk=None):
        """
        Devuelve los horarios disponibles para un parqueo específico con capacidad restante.
        """
        try:
            parking = self.get_object()
            available_schedules = ParkingSchedule.objects.filter(parking=parking, actualCapacity__gt=0)

            if not available_schedules.exists():
                return Response({"detail": "No hay horarios disponibles para este parqueo."},
                                status=status.HTTP_404_NOT_FOUND)

            # Crear respuesta con horarios disponibles
            result = []
            for schedule in available_schedules:
                result.append({
                    "parkingschedule_id": schedule.id,  # Agregamos el ID del ParkingSchedule
                    "date": schedule.date,
                    "schedule": {
                        "start_time": schedule.schedule.start_time,
                        "end_time": schedule.schedule.end_time,
                    },
                    "available_capacity": schedule.actualCapacity
                })

            return Response(result, status=status.HTTP_200_OK)

        except Parking.DoesNotExist:
            return Response({"detail": "El parqueo no existe."}, status=status.HTTP_404_NOT_FOUND)


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

    @action(detail=True, methods=['get'], url_path='future-schedules')
    def get_future_schedules(self, request, pk=None):
        """
        Devuelve los horarios futuros para un parqueo específico (mayores o iguales a la fecha actual).
        """
        parking_schedule = self.get_object()
        today = timezone.now().date()

        # Filtra los horarios mayores o iguales a la fecha actual
        future_schedules = ParkingSchedule.objects.filter(parking=parking_schedule.parking, date__gte=today)

        if not future_schedules.exists():
            return Response({"detail": "No hay horarios futuros disponibles para este parqueo."}, status=404)

        # Crear la respuesta con los horarios futuros
        result = []
        for schedule in future_schedules:
            result.append({
                "parkingschedule_id": schedule.id,
                "date": schedule.date,
                "schedule": {
                    "start_time": schedule.schedule.start_time,
                    "end_time": schedule.schedule.end_time,
                },
                "available_capacity": schedule.actualCapacity
            })

        return Response(result, status=200)