from django_filters.rest_framework import DjangoFilterBackend

from .models import *
from rest_framework import permissions, viewsets, filters

from .serializers import *





class VehicleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['color']
    filterset_fields = ['plate','user__id']












# class ClientViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows users to be viewed or edited.
#     """
#     queryset = Client.objects.all()
#     serializer_class = ClientSerializer
#     #PARA LEVANTAR AUTENTICACIÓNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN
#     permission_classes = [permissions.IsAuthenticated]
#     filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
#     filterset_fields = ['email']
#     search_fields = ['name']





