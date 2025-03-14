import django_filters
from django.db.models import Q
from apps.fields.models import Field


class FieldFilter(django_filters.FilterSet):
    owner = django_filters.NumberFilter(field_name="owner_id")
    search = django_filters.CharFilter(method="filter_search")

    class Meta:
        model = Field
        fields = ["owner", "created_at"]

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) |
            Q(address__icontains=value)
        ).distinct()
