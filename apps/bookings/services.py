from apps.bookings.models import Booking


class BookingService:
    def __init__(self, user):
        self.user = user

    def get_queryset(self):
        queryset = Booking.objects.all()
        if self.user.role == "admin":
            queryset = queryset
        elif self.user.role == "owner":
            queryset = queryset.filter(field__owner=self.user)
        else:
            queryset = queryset.filter(user=self.user)
        return queryset.order_by("-created_at")

    def perform_create(self, serializer):
        if self.user.role not in ["admin", "owner"]:
            serializer.save(user=self.user)
        else:
            serializer.save()
