from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from apps.fields import serializers as slr
from utils.exceptions import resp

create_field_schema = extend_schema(
    summary='Create Field',
    request=slr.FieldCreateSerializer(),
    responses=resp(201)
)

update_field_schema = extend_schema(
    summary='Update Field',
    request=slr.FieldUpdateSerializer(),
    responses=resp(200)
)

delete_field_schema = extend_schema(
    summary='Delete Field',
    request=None,
    responses=resp(204)
)

get_fields_schema = extend_schema(
    summary="Get Fields (Available + All Fields)",
    request=None,
    responses=resp(200, slr.FieldSerializer(many=True)),
    parameters=[
        OpenApiParameter(
            name="start_time",
            description="Start time of the desired booking period (format: YYYY-MM-DD HH:MM:SS).",
            required=False,
            type=OpenApiTypes.DATETIME
        ),
        OpenApiParameter(
            name="end_time",
            description="End time of the desired booking period (format: YYYY-MM-DD HH:MM:SS).",
            required=False,
            type=OpenApiTypes.DATETIME
        ),
        OpenApiParameter(
            name="lat",
            description="User's latitude for sorting fields by proximity.",
            required=False,
            type=OpenApiTypes.FLOAT
        ),
        OpenApiParameter(
            name="lon",
            description="User's longitude for sorting fields by proximity.",
            required=False,
            type=OpenApiTypes.FLOAT
        ),
        OpenApiParameter(
            name="owner",
            description="Filter by owner ID",
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

get_field_schema = extend_schema(
    summary='Field',
    request=None,
    responses=resp(200, slr.FieldSerializer)
)
