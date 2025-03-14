import django_filters
from django.db.models import Q

from apps.orders.choices import OrderStatusChoice
from apps.orders.models import Order


class OrderFilter(django_filters.FilterSet):
    route = django_filters.NumberFilter(field_name="route_id")
    status = django_filters.ChoiceFilter(
        field_name="status",
        choices=OrderStatusChoice.choices
    )
    seat_option = django_filters.NumberFilter(field_name="seat_option_id")
    passenger_count = django_filters.NumberFilter(field_name="passenger_count")
    date = django_filters.CharFilter(method="filter_date")
    search = django_filters.CharFilter(method="filter_search")

    class Meta:
        model = Order
        fields = ["route", "seat_option", "passenger_count", "status", "created_at"]

    def filter_date(self, queryset, name, value):
        try:
            if len(value) == 10:
                year, month, day = map(int, value.split("-"))
                return queryset.filter(created_at__year=year, created_at__month=month, created_at__day=day)
            elif len(value) == 7:
                year, month = map(int, value.split("-"))
                return queryset.filter(created_at__year=year, created_at__month=month)
            elif len(value) == 4:
                return queryset.filter(created_at__year=int(value))
        except ValueError:
            return queryset.none()

        return queryset

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(urgency__icontains=value) |
            Q(description__icontains=value)
        )
