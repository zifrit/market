from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiParameter
from rest_framework import generics, status
from rest_framework.response import Response

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


class ProductViewSet(ModelViewSet):
    queryset = (
        Product.objects.select_related("brands", "category", "shop")
        .prefetch_related(
            "sizes",
            "color",
            "images__color",
            "ratings",
            "favorites",
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


class BrandsViewSet(ModelViewSet):
    queryset = Brands.objects.all()
    serializer_class = BrandsSerializer
    filter_backends = [SearchFilter]
    search_fields = ["name"]


class CategoriesViewSet(ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [SearchFilter]
    search_fields = ["name"]


class SizesViewSet(ModelViewSet):
    queryset = Sizes.objects.all()
    serializer_class = SizeSerializer
    filter_backends = [SearchFilter]
    search_fields = ["name"]


class ColorsViewSet(ModelViewSet):
    queryset = Colors.objects.all()
    serializer_class = ColorsSerializer
    filter_backends = [SearchFilter]
    search_fields = ["hex_color"]


class ListCreateProductRaringView(generics.ListCreateAPIView):
    queryset = ProductRating.objects.all()
    serializer_class = ProductRatingSerializers


class CreateListHumanImageView(
    generics.CreateAPIView,
    generics.ListAPIView,
):
    queryset = HumanImage.objects.prefetch_related(
        Prefetch(
            "products", queryset=ProductHumanImages.objects.select_related("product")
        ),
        "images",
    )
    serializer_class = HumanImageSerializer


class UpdateDeleteHumanImageView(
    generics.DestroyAPIView,
    generics.RetrieveAPIView,
    generics.UpdateAPIView,
):
    queryset = HumanImage.objects.prefetch_related(
        Prefetch(
            "products", queryset=ProductHumanImages.objects.select_related("product")
        ),
        "images",
    )

    serializer_class = HumanImageSerializer

    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)
        obj = self.get_object()
        return Response(ViewHumanImageSerializer(instance=obj).data)

    def partial_update(self, request, *args, **kwargs):
        super().partial_update(request, *args, **kwargs)
        obj = self.get_object()
        return Response(ViewHumanImageSerializer(instance=obj).data)
