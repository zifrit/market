from django.db.models import Avg, Count, Prefetch
from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
    OpenApiExample,
    OpenApiParameter,
)
from rest_framework.response import Response

from clo.permission import CustomBasePermission
from context import swagger_json
from shop.models import Shop, ShopRating, ShopWorkSchedules, ShopReport
from rest_framework import generics, status, mixins
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from shop.api.serializers import (
    ShowShopSerializer,
    CreateShopSerializer,
    ShopRatingSerializer,
    ShopWorkScheduleSerializer,
    UpdateShopSerializer,
    ShopReportSerializer,
    UpdateShopReportSerializer,
)
from clo.pagination import CustomPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter


class ShopViewSet(ModelViewSet, CustomBasePermission):
    queryset = (
        Shop.objects.prefetch_related("images", "ratings")
        .select_related("work_schedules", "address")
        .annotate(
            rating=Avg("ratings__rating"),
            total_human_images=Count("human_images"),
            total_products=Count("products"),
        )
    )
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    search_fields = ["name"]
    filterset_fields = ["is_active", "status"]
    ordering_fields = ["is_active"]
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.request.method in ["POST"]:
            return CreateShopSerializer
        elif self.request.method in ["PUT", "PATCH"]:
            return UpdateShopSerializer
        return ShowShopSerializer

    @extend_schema(
        description="""
        Поле additional_data отвечает за дополнительную информацию может помочь отличить один Магазин от другого.
        Формат поля json т.е 
        additional_data : {
            "sting_key1": sting_value or integer_value,
            "sting_key2": sting_value or integer_value,
            ...
        }
        """,
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(request=ShowShopSerializer)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        request=ShowShopSerializer,
        parameters=[
            OpenApiParameter(name="page", type=int, description="Номер страницы"),
        ],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class ListCreateShopRatingView(generics.ListCreateAPIView):
    queryset = ShopRating.objects.all()
    serializer_class = ShopRatingSerializer

    def get_queryset(self):
        return ShopRating.objects.filter(shop_id=self.kwargs["id"])

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["shop_id"] = self.kwargs.get("id")
        return context


class UpdateCreateWorkScheduleView(
    generics.UpdateAPIView, generics.CreateAPIView, CustomBasePermission
):
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


class ShopReportViewSet(ModelViewSet):
    queryset = ShopReport.objects.all()
    serializer_class = ShopReportSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["status"]


class ListCreateShopReportView(generics.ListCreateAPIView, CustomBasePermission):
    queryset = ShopReport.objects.all()
    serializer_class = ShopReportSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["status"]


class UpdateRetrieveShopReportView(
    generics.RetrieveUpdateAPIView, CustomBasePermission
):
    queryset = ShopReport.objects.all()
    serializer_class = ShopReportSerializer


class VerifyShopReportView(generics.UpdateAPIView, CustomBasePermission):
    queryset = ShopReport.objects.all()
    serializer_class = UpdateShopReportSerializer
