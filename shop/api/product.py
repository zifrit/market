from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiParameter
from rest_framework import generics
from rest_framework.response import Response

from clo.permission import (
    CustomBasePermission,
)
from shop.filters import ProductFilter
from shop.models import (
    Product,
    Brands,
    Categories,
    Sizes,
    Colors,
    ProductRating,
    HumanImage,
    ProductHumanImages,
    ProductImages,
    HumanImageImages,
)
from rest_framework.viewsets import ModelViewSet
from shop.api.serializers import (
    ProductSerializers,
    BrandsSerializer,
    CategorySerializer,
    SizeSerializer,
    ColorsSerializer,
    ViewProductSerializers,
    RetrieveProductSerializers,
    ProductRatingSerializers,
    HumanImageSerializer,
    ViewHumanImageSerializer,
)
from clo.pagination import CustomPagination
from context import swagger_json
from django.db.models import Avg, Prefetch
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter

from shop.services.custom_view import CustomModelViewSet, CustomDestroyAPIView


class ProductViewSet(CustomModelViewSet, CustomBasePermission):
    queryset = (
        Product.objects.select_related("brands", "category", "shop")
        .prefetch_related(
            "sizes",
            "color",
            "ratings",
            "favorites",
            Prefetch(
                "images",
                queryset=ProductImages.objects.select_related("color").filter(
                    delete_at__isnull=True
                ),
            ),
        )
        .annotate(rating=Avg("ratings__rating"))
    )
    serializer_class = ProductSerializers
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    search_fields = ["name", "shop__name", "brands__name", "category__name"]
    filterset_class = ProductFilter
    ordering_fields = ["price", "enabled"]
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.request.method == "GET":
            if self.kwargs.get("pk"):
                return RetrieveProductSerializers
            return ViewProductSerializers
        return ProductSerializers

    @extend_schema(
        examples=[
            OpenApiExample("get example", value=swagger_json.product_list_retrieve)
        ]
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        parameters=[
            OpenApiParameter(name="page", type=int, description="Номер страницы"),
        ],
        examples=[
            OpenApiExample("get example", value=swagger_json.product_list_retrieve)
        ],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        description="""
        Поле additional_data отвечает за дополнительную информацию может помочь отличить один товар от другого.
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


class BrandsViewSet(CustomModelViewSet, CustomBasePermission):
    queryset = Brands.objects.filter(delete_at__isnull=True)
    serializer_class = BrandsSerializer
    filter_backends = [SearchFilter]
    search_fields = ["name"]


class CategoriesViewSet(CustomModelViewSet, CustomBasePermission):
    queryset = Categories.objects.filter(delete_at__isnull=True)
    serializer_class = CategorySerializer
    filter_backends = [SearchFilter]
    search_fields = ["name"]


class SizesViewSet(CustomModelViewSet, CustomBasePermission):
    queryset = Sizes.objects.filter(delete_at__isnull=True)
    serializer_class = SizeSerializer
    filter_backends = [SearchFilter]
    search_fields = ["name"]


class ColorsViewSet(CustomModelViewSet, CustomBasePermission):
    queryset = Colors.objects.filter(delete_at__isnull=True)
    serializer_class = ColorsSerializer
    filter_backends = [SearchFilter]
    search_fields = ["hex_color"]


class ListCreateProductRatingView(generics.ListCreateAPIView):
    serializer_class = ProductRatingSerializers

    def get_queryset(self):
        return ProductRating.objects.filter(product_id=self.kwargs["id"])

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["product_id"] = self.kwargs.get("id")
        return context


class CreateListHumanImageView(
    generics.CreateAPIView,
    generics.ListAPIView,
    CustomBasePermission,
):
    queryset = HumanImage.objects.prefetch_related(
        Prefetch(
            "images", queryset=HumanImageImages.objects.filter(delete_at__isnull=True)
        ),
    )
    serializer_class = HumanImageSerializer
    pagination_class = CustomPagination
    filter_backends = [
        DjangoFilterBackend,
    ]
    filterset_fields = ["shop_id"]

    @extend_schema(
        examples=[OpenApiExample("get example", value=swagger_json.human_images)]
    )
    def get(self, request, *args, **kwargs):
        result = super().get(request, *args, **kwargs)
        return result


class UpdateDeleteHumanImageView(
    CustomDestroyAPIView,
    generics.RetrieveAPIView,
    generics.UpdateAPIView,
    CustomBasePermission,
):
    queryset = HumanImage.objects.prefetch_related(
        Prefetch(
            "products", queryset=ProductHumanImages.objects.select_related("product")
        ),
        "images",
    ).filter(delete_at__isnull=True)

    serializer_class = HumanImageSerializer

    @extend_schema(
        examples=[OpenApiExample("get example", value=swagger_json.human_images)]
    )
    def get(self, request, *args, **kwargs):
        result = super().get(request, *args, **kwargs)
        return result

    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)
        obj = self.get_object()
        return Response(ViewHumanImageSerializer(instance=obj).data)

    def partial_update(self, request, *args, **kwargs):
        super().partial_update(request, *args, **kwargs)
        obj = self.get_object()
        return Response(ViewHumanImageSerializer(instance=obj).data)
