from drf_spectacular.utils import extend_schema, OpenApiParameter
from apps.orders import serializers as slr
from apps.orders.choices import OrderStatusChoice
from utils.exceptions import resp

create_order_schema = extend_schema(
    summary='Create Order',
    request=slr.OrderCreateSerializer(),
    responses=resp(201)
)

update_order_schema = extend_schema(
    summary='Update Order',
    request=slr.OrderUpdateSerializer(),
    responses=resp(200)
)

delete_order_schema = extend_schema(
    summary='Delete Order',
    request=None,
    responses=resp(204)
)

get_orders_schema = extend_schema(
    summary='Orders',
    request=None,
    responses=resp(200, slr.OrderSerializer),
    parameters=[
        OpenApiParameter(
            name="status",
            description="Filter by order status",
            required=False,
            type=str,
            enum=[choice.value for choice in OrderStatusChoice]
        ),
        OpenApiParameter(
            name="route",
            description="Filter by route ID",
            required=False,
            type=str
        ),
        OpenApiParameter(
            name="seat_option",
            description="Filter by seat_option ID",
            required=False,
            type=str
        ),
        OpenApiParameter(
            name="passenger_count",
            description="Filter by passenger_count",
            required=False,
            type=int
        ),
        OpenApiParameter(
            name="date",
            description="Filter by exam creation date",
            required=False,
            type=str
        ),
        OpenApiParameter(
            name="search",
            description="Search by name and description",
            required=False,
            type=str
        ),
        OpenApiParameter(
            name="page",
            description="Page number for pagination",
            required=False,
            type=int
        ),
        OpenApiParameter(
            name="limit",
            description="Number of results per page",
            required=False,
            type=int
        ),
    ]
)

get_order_schema = extend_schema(
    summary='Order',
    request=None,
    responses=resp(200, slr.OrderSerializer)
)

accept_order_schema = extend_schema(
    summary='Accept Order',
    request=None,
    responses=resp(200)
)