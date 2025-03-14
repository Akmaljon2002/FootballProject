from rest_framework import serializers
from apps.bookings.models import Booking
from apps.users.models import CustomUser
from utils.exceptions import raise_error, ErrorCodes


class BookingSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), required=False)

    class Meta:
        model = Booking
        fields = '__all__'

    def validate(self, data):
        if data['start_time'] >= data['end_time']:
            raise_error(ErrorCodes.INVALID_DATE_RANGE, "Start time must be before end time.")

        if Booking.objects.filter(
            field=data['field'],
            start_time__lt=data['end_time'],
            end_time__gt=data['start_time']
        ).exists():
            raise_error(ErrorCodes.BOOKING_CONFLICT, "This time slot is already booked.")

        return data