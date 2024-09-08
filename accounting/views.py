from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import Group
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied

from .models import *
from rest_framework import permissions, viewsets, status

from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework import filters



from rest_framework.response import Response
from .serializers import ReservationSerializer



class ReservationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['state']
    search_fields = ['vehicle__plate']

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """
        Acción personalizada para cancelar una reserva.
        """
        reservation = self.get_object()

        try:
            reservation.cancel_reservation()
            return Response({'status': 'Reserva cancelada'}, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


    # Acción personalizada para marcar una reserva como pagada
    @action(detail=True, methods=['post'])
    def pay(self, request, pk=None):
        reservation = self.get_object()

        try:
            reservation.pay_reservation()  # Llama al método para marcar la reserva como pagada
            return Response({'status': 'Reserva pagada'}, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)







    # permission_classes =

    # def get_queryset(self):
    #     user =  self.request.user
    #     if not user.groups.filter(name='admin').exists():
    #         raise PermissionDenied()
    #
    #     queryset = Reservation.objects.all()
    #     return queryset


