from rest_framework import serializers

from apps.orders.choices import OrderStatusChoice
from apps.orders.models import Order


class OrderCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = [
            'route',
            'phone',
            'seat_option',
            'price',
            'passenger_count',
            'urgency',
            'description',
        ]


class OrderUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = [
            'route',
            'phone',
            'seat_option',
            'price',
            'passenger_count',
            'urgency',
            'description',
        ]


class OrderSerializer(serializers.ModelSerializer):
    phone = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            'id',
            'route',
            'phone',
            'seat_option',
            'price',
            'passenger_count',
            'urgency',
            'description',
            'status',
            'driver',
            'created_at'
        ]

    def get_phone(self, obj):
        request = self.context.get('request')

        if request and request.user.role == 'driver' and obj.status == OrderStatusChoice.PENDING:
            return None

        return obj.phone


class OrderAcceptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'driver', 'status']
        read_only_fields = ['id', 'driver', 'status']