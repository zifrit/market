from django.utils import timezone
from drf_spectacular.utils import (
    extend_schema,
    OpenApiExample,
    OpenApiParameter,
    OpenApiResponse,
)
from rest_framework import status
from rest_framework.response import Response

from clo.permission import CustomBasePermission
from shop.models import Address
from rest_framework.viewsets import ModelViewSet
from shop.api.serializers import AddressSerializer, ExampleSerializer
from rest_framework.filters import SearchFilter
from clo.pagination import CustomPagination
from context import swagger_json


class AddressViewSet(ModelViewSet, CustomBasePermission):
    queryset = Address.objects.filter(delete_at__isnull=True)
    serializer_class = AddressSerializer
    filter_backends = [SearchFilter]
    search_fields = ["address"]
    pagination_class = CustomPagination

    @extend_schema(
        request=swagger_json.crud_address,
        parameters=[
            OpenApiParameter(name="page", type=int, description="Номер страницы"),
        ],
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

    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.delete_at = timezone.now()
        obj.save()
        print(obj)
        return Response(status=status.HTTP_204_NO_CONTENT)
