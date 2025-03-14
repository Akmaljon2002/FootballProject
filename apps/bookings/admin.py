from django.contrib import admin
from apps.bookings.models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('field', 'user', 'start_time', 'end_time', 'created_at')
    list_filter = ('field', 'start_time', 'end_time')
    search_fields = ('user__username', 'field__name')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
    date_hierarchy = 'start_time'
    list_per_page = 20
