from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import Group
from rest_framework.exceptions import PermissionDenied

from .models import *
from rest_framework import permissions, viewsets

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

    # permission_classes =

    # def get_queryset(self):
    #     user =  self.request.user
    #     if not user.groups.filter(name='admin').exists():
    #         raise PermissionDenied()
    #
    #     queryset = Reservation.objects.all()
    #     return queryset


