from django.db import models
from apps.fields.models import Field
from apps.users.models import CustomUser


class Booking(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="bookings")
    field = models.ForeignKey(Field, on_delete=models.CASCADE, related_name="bookings")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('field', 'start_time', 'end_time')
        verbose_name_plural = 'Bookings'

    def __str__(self):
        return f"{self.field.name} | {self.start_time} - {self.end_time}"


