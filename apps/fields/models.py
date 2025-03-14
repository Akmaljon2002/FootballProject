from django.db import models
from apps.users.models import CustomUser


class Field(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="fields")
    name = models.CharField(max_length=255)
    address = models.TextField()
    contact = models.CharField(max_length=50)
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    images = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Fields'
