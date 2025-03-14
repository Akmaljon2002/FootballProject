from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from apps.bookings.serializers import BookingSerializer
from apps.bookings.services import BookingService


class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return BookingService(self.request.user).get_queryset()

    def perform_create(self, serializer):
        BookingService(self.request.user).perform_create(serializer)