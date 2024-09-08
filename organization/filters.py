import django_filters
from .models import Parking

class ParkingFilter(django_filters.FilterSet):
    # Filtra por el nombre del parqueo
    name = django_filters.CharFilter(field_name="name", lookup_expr='icontains')

    # Filtra por fecha de los horarios (schedule) a través del modelo ParkingSchedule
    schedule_date = django_filters.DateFilter(field_name="parkingschedule__date")

    # Filtra por ID de usuario
    user_id = django_filters.NumberFilter(field_name="user__id")

    class Meta:
        model = Parking
        fields = ['name', 'schedule_date', 'user_id']
