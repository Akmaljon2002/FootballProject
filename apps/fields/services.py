from django.db import models
from rest_framework.response import Response
from apps.orders.choices import OrderStatusChoice
from apps.orders.filters import OrderFilter
from apps.orders import serializers as slr
from apps.orders import models as orders_models
from apps.transaction.choices import TransactionType
from apps.transaction.models import Transaction
from utils.exceptions import raise_error, ErrorCodes
from utils.pagination import BaseService, BaseServicePagination


class OrderService(BaseServicePagination):

    def create_order(self):
        serializer = slr.OrderCreateSerializer(
            data=self.request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=201)

    def update_order(self, pk):
        serializer = slr.OrderUpdateSerializer(
            self._get_order(pk),
            data=self.request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=200)

    def get_orders(self):
        user = self.request.user

        if user.role == "driver":
            orders = orders_models.Order.objects.filter(
                models.Q(status=OrderStatusChoice.PENDING) | models.Q(driver=user)
            ).order_by('-created_at')
        else:
            orders = orders_models.Order.objects.all().order_by('-created_at')
        filterset = OrderFilter(self.request.GET, queryset=orders)
        if filterset.is_valid():
            orders = filterset.qs
        results = self.paginate(orders)
        serializer = slr.OrderSerializer(
            results,
            many=True,
            context={'request': self.request}
        )
        return self.paginated_response(serializer.data)

    def get_order(self, pk):
        serializer = slr.OrderSerializer(
            self._get_order(pk)
        )
        return Response(serializer.data)

    def delete_order(self, pk):
        order = self._get_order(pk)
        order.delete()
        return Response(status=204)

    def _get_order(self, pk):
        try:
            order = orders_models.Order.objects.get(id=pk)
        except orders_models.Order.DoesNotExist:
            raise_error(
                ErrorCodes.ORDER_NOT_FOUND,
                "Order not found."
            )
        return order

    def accept_order(self, pk):
        order = self._get_order(pk)

        if order.driver is not None:
            raise_error(
                ErrorCodes.ORDER_ALREADY_TAKEN,
                "This order is already accepted by another driver."
            )

        driver = self.request.user
        seat_price = order.seat_option.price * order.passenger_count

        if driver.balance < seat_price:
            raise_error(
                ErrorCodes.INSUFFICIENT_BALANCE,
                "Insufficient balance to accept this order."
            )

        Transaction.objects.create(
            driver=driver,
            order=order,
            amount=-seat_price,
            transaction_type=TransactionType.DEDUCTION
        )

        driver.balance -= seat_price
        driver.save()

        order.driver = driver
        order.status = OrderStatusChoice.ACCEPTED
        order.save()

        return Response(status=200)