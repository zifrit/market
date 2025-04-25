from django.db.models import Avg
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from rest_framework.response import Response

from context import swagger_json
from shop.models import Shop, ShopRating, ShopWorkSchedules
from rest_framework import generics, status
from rest_framework.viewsets import ModelViewSet
from shop.api.serializers import (
    ShopSerializer,
    ShopRatingSerializer,
    ShopWorkScheduleSerializer,
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter


class ShopViewSet(ModelViewSet):
    queryset = (
        Shop.objects.prefetch_related("images", "ratings")
        .select_related("work_schedules")
        .annotate(rating=Avg("ratings__rating"))
    )
    serializer_class = ShopSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    search_fields = ["name"]
    filterset_fields = ["is_active", "status"]
    ordering_fields = ["is_active"]

    @extend_schema(
        description="""
        Поле additional_data отвечает за дополнительную информацию может помочь отличить один Магазин от другого.
        Формат поля json т.е 
        additional_data : {
            "sting_key1": sting_value or integer_value,
            "sting_key2": sting_value or integer_value,
            ...
        }
        """
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class ListCreateShopRatingView(generics.ListCreateAPIView):
    queryset = ShopRating.objects.all()
    serializer_class = ShopRatingSerializer


class UpdateCreateWorkScheduleView(generics.UpdateAPIView, generics.CreateAPIView):
    queryset = ShopWorkSchedules.objects.all()
    serializer_class = ShopWorkScheduleSerializer

    @extend_schema(
        request=swagger_json.work_schedule_retrieve,
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    @extend_schema(
        request=swagger_json.work_schedule_retrieve,
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
