import django_filters
from accounting.models import Reservation

class ReservationFilter(django_filters.FilterSet):
    parkingSchedule__date = django_filters.DateFilter(field_name='parkingSchedule__date', lookup_expr='exact')
    parking = django_filters.NumberFilter(field_name='parking')
    user_name = django_filters.CharFilter(field_name='vehicle__user__name', lookup_expr='icontains')
    user_identification = django_filters.CharFilter(field_name='vehicle__user__identification', lookup_expr='icontains')
    vehicle_plate = django_filters.CharFilter(field_name='vehicle__plate', lookup_expr='icontains')

    class Meta:
        model = Reservation
        fields = ['state', 'parking', 'parkingSchedule__date', 'user_name', 'user_identification', 'vehicle_plate']