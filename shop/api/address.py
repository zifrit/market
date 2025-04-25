from drf_spectacular.utils import (
    extend_schema,
    OpenApiExample,
    OpenApiParameter,
    OpenApiResponse,
)

from shop.models import Address
from rest_framework.viewsets import ModelViewSet
from shop.api.serializers import AddressSerializer, ExampleSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from context import swagger_json


class AddressViewSet(ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    filter_backends = [SearchFilter]
    search_fields = ["address"]

    @extend_schema(
        request=swagger_json.crud_address,
        responses={
            200: OpenApiResponse(
                response=ExampleSerializer,
                examples=[
                    OpenApiExample(
                        "post example",
                        value={
                            "coordinate": {
                                "sting_key1": "sting_value or int_value",
                                "sting_key2": "sting_value or int_value",
                            },
                            "address": "string",
                        },
                    )
                ],
            )
        },
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        request=swagger_json.crud_address,
        responses={
            200: OpenApiResponse(
                response=ExampleSerializer,
                examples=[
                    OpenApiExample(
                        "post example",
                        value={
                            "coordinate": {
                                "sting_key1": "sting_value or int_value",
                                "sting_key2": "sting_value or int_value",
                            },
                            "address": "string",
                        },
                    )
                ],
            )
        },
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        request=swagger_json.crud_address,
        responses={
            200: OpenApiResponse(
                response=ExampleSerializer,
                examples=[
                    OpenApiExample(
                        "post example",
                        value={
                            "coordinate": {
                                "sting_key1": "sting_value or int_value",
                                "sting_key2": "sting_value or int_value",
                            },
                            "address": "string",
                        },
                    )
                ],
            )
        },
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
