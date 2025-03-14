from django.contrib import admin
from django.utils.html import format_html
from .models import Field


@admin.register(Field)
class FieldAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'address', 'contact', 'price_per_hour', 'show_images', 'latitude', 'longitude')
    list_filter = ('owner', 'price_per_hour')
    search_fields = ('name', 'address', 'contact', 'owner__username')
    ordering = ('-id',)

    def show_images(self, obj):
        if obj.images:
            return format_html('<img src="{}" width="50" height="50" style="border-radius:5px;" />', obj.images[0])
        return "No Image"

    show_images.short_description = "Image Preview"
