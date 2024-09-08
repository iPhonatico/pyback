import django_filters
from accounting.models import Reservation

class ReservationFilter(django_filters.FilterSet):
    parkingSchedule__date = django_filters.DateFilter(field_name='parkingSchedule__date', lookup_expr='exact')
    parking = django_filters.NumberFilter(field_name='parking')

    class Meta:
        model = Reservation
        fields = ['state', 'parking', 'parkingSchedule__date']  # Asegúrate de que 'date' no esté duplicado

