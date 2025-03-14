from django.db.models import QuerySet
from rest_framework.request import Request
from rest_framework.pagination import PageNumberPagination


class Pagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 50


class BaseService:
    def __init__(self, request: Request):
        self.request: Request = request

    def query(self, param: str, default=None):
        return self.request.GET.get(param, default)


class BaseServicePagination:
    def __init__(self, request: Request):
        self.request: Request = request
        self.pagination = Pagination()

    def query(self, param: str, default=None):
        return self.request.GET.get(param, default)

    def paginate(self, queryset: QuerySet):
        return self.pagination.paginate_queryset(
            queryset,
            self.request
        )

    def paginated_response(self, data: list):
        return self.pagination.get_paginated_response(
            data
        )
