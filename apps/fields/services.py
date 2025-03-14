from rest_framework.response import Response
from apps.fields.filters import FieldFilter
from apps.fields import serializers as slr
from apps.fields import models as fields_models
from utils.exceptions import raise_error, ErrorCodes
from utils.functions import haversine_distance
from utils.pagination import BaseServicePagination


class FieldService(BaseServicePagination):

    def create_field(self):
        serializer = slr.FieldCreateSerializer(
            data=self.request.data,
            context={'request': self.request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=201)

    def update_field(self, pk):
        serializer = slr.FieldUpdateSerializer(
            self._get_field(pk),
            data=self.request.data,
            partial=True,
            context={'request': self.request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=200)

    def get_fields(self):
        start_time = self.request.query_params.get('start_time')
        end_time = self.request.query_params.get('end_time')
        lat = self.request.query_params.get('lat')
        lon = self.request.query_params.get('lon')

        fields = fields_models.Field.objects.all().order_by('-created_at')

        if start_time and end_time:
            fields = fields.exclude(
                bookings__start_time__lt=end_time,
                bookings__end_time__gt=start_time
            )

        filterset = FieldFilter(self.request.GET, queryset=fields)
        if filterset.is_valid():
            fields = filterset.qs

        if lat and lon:
            lat, lon = float(lat), float(lon)

            for field in fields:
                field.distance = haversine_distance(lat, lon, float(field.latitude), float(field.longitude))

            fields = sorted(fields, key=lambda x: x.distance)

        results = self.paginate(fields)
        serializer = slr.FieldSerializer(results, many=True, context={'request': self.request})

        return self.paginated_response(serializer.data)

    def get_field(self, pk):
        serializer = slr.FieldSerializer(
            self._get_field(pk)
        )
        return Response(serializer.data)

    def delete_field(self, pk):
        field = self._get_field(pk)
        field.delete()
        return Response(status=204)

    def _get_field(self, pk):
        try:
            field = fields_models.Field.objects.get(id=pk)
        except fields_models.Field.DoesNotExist:
            raise_error(
                ErrorCodes.FIELD_NOT_FOUND,
                "Field not found."
            )
        return field