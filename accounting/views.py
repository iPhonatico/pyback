from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import Group
from .models import *
from rest_framework import permissions, viewsets

from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters


class ReservationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['state',"vehicle__plate"]
    search_fields = ['vehicle__plate']
    # permission_classes = [permissions.IsAuthenticated]


