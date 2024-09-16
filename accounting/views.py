from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from .models import *
from rest_framework import viewsets, status
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.response import Response
from accounting.filters import ReservationFilter
from datetime import datetime, timedelta
from django.utils.timezone import make_aware, now

class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ReservationFilter  # Asignar el filtro personalizado
    filterset_fields = ['parking']  # Permitir filtrar por parqueo

    # Agregar búsqueda por nombre de usuario e identificación del vehículo
    search_fields = ['vehicle__plate', 'vehicle__user__name', 'vehicle__user__identification']

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        reservation = self.get_object()
        try:
            reservation.cancel_reservation()
            return Response({'status': 'Reserva cancelada'}, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def calcular_valor_a_pagar(self, request, pk=None):
        """
        Calcula el valor total a pagar según el tiempo transcurrido de la reserva.
        """
        reservation = self.get_object()
        parking = reservation.parking  # Obtener el parqueadero asociado
        parking_fee = parking.fee  # Tarifa del parqueadero

        # Obtener la hora actual y la hora de finalización de la reserva
        now_time = now() - timedelta(hours=5)  # Ajustar zona horaria si es necesario
        end_time = make_aware(datetime.combine(reservation.parkingSchedule.date, reservation.parkingSchedule.schedule.end_time))

        # Inicialmente, el valor adicional por horas excedidas es 0
        total_payment = reservation.payAmount

        # Si la hora actual es mayor que el tiempo final de la reserva, calcular el exceso
        if now_time > end_time:
            exceeded_time = now_time - end_time
            # Calcular cuántas horas (o fracción) se excedió
            exceeded_hours = exceeded_time.total_seconds() / 3600
            # Redondear hacia arriba para cobrar fracciones de horas
            extra_hours = int(exceeded_hours) + (1 if exceeded_hours % 1 else 0)
            total_payment += extra_hours * parking_fee

        # Devolver el monto total a pagar
        return Response({
            "reservation_id": reservation.id,
            "total_payment": total_payment,
            "original_fee": reservation.payAmount,
            "extra_hours": extra_hours if now_time > end_time else 0
        })

    @action(detail=True, methods=['post'])
    def pay(self, request, pk=None):
        """
        Acción personalizada para procesar el pago de una reserva.
        Valida que el monto enviado por el usuario coincida con el valor calculado.
        """
        reservation = self.get_object()

        # Verificar que la reserva esté activa
        if reservation.state != 'A':
            return Response({'error': 'La reserva ya está pagada o cancelada.'}, status=status.HTTP_400_BAD_REQUEST)

        # Obtener el valor enviado en la solicitud
        pay_amount = request.data.get('payAmount')

        if not pay_amount:
            return Response({'error': 'Debe proporcionar el monto a pagar.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            pay_amount = float(pay_amount)
        except ValueError:
            return Response({'error': 'El monto proporcionado no es válido.'}, status=status.HTTP_400_BAD_REQUEST)

        # Calcular el valor correcto a pagar llamando a calcular_valor_a_pagar
        payment_response = self.calcular_valor_a_pagar(request, pk)
        total_to_pay = payment_response.data['total_payment']

        # Verificar que el valor a pagar coincida con el cálculo
        if pay_amount != total_to_pay:
            return Response({'error': 'El monto proporcionado no coincide con el monto a pagar.'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Actualizar el estado de la reserva a pagada y liberar un espacio
        reservation.state = 'P'
        reservation.save()

        # Aumentar la capacidad actual del parqueo
        reservation.parkingSchedule.actualCapacity += 1
        reservation.parkingSchedule.save()

        return Response({'status': 'Reserva pagada con éxito'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def by_user(self, request):
        """
        Filtra las reservas por el usuario autenticado.
        """
        user = request.user
        # Ordenar por la fecha y hora del parkingSchedule
        reservations = Reservation.objects.filter(vehicle__user=user).order_by('parkingSchedule__date', 'parkingSchedule__schedule__start_time')
        serializer = self.get_serializer(reservations, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_parking(self, request):
        """
        Filtra las reservas por parqueadero específico.
        """
        parking_id = request.query_params.get('parking', None)
        if parking_id is None:
            return Response({"error": "Debe proporcionar un id de parqueadero."}, status=400)

        # Ordenar por la fecha y hora del parkingSchedule
        reservations = Reservation.objects.filter(parking__id=parking_id).order_by('parkingSchedule__date', 'parkingSchedule__schedule__start_time')
        serializer = self.get_serializer(reservations, many=True)
        return Response(serializer.data)