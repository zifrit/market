from drf_spectacular.utils import (
    extend_schema,
    OpenApiExample,
    OpenApiParameter,
    OpenApiResponse,
)
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from shop.models import ProductImages, ShopImages, Shop
from shop.api.serializers import (
    ProductImagesSerializers,
    ShopImagesSerializers,
    ExampleSerializer,
)


class ProductImagesViewSet(generics.GenericAPIView):
    queryset = ProductImages.objects.all()
    serializer_class = ProductImagesSerializers

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="product",
                description="Product identifier",
                required=True,
                type=int,
            ),
            OpenApiParameter(
                name="color", description="Color identifier", required=True, type=int
            ),
        ],
        request={
            "multipart/form-data": {
                "type": "object",
                "properties": {
                    "file": {
                        "type": "string",
                        "format": "binary",
                        "description": "Файл для загрузки",
                    }
                },
                "required": ["file"],
            }
        },
        responses={
            201: OpenApiResponse(
                response=ExampleSerializer,
                examples=[
                    OpenApiExample(
                        "post example",
                        value={
                            "color": {"id": 0, "name": "string", "hex_color": "string"},
                            "image": "string",
                            "name": "string",
                            "product": "string",
                        },
                    )
                ],
            )
        },
        summary="Загрузка фото продукта",
    )
    def post(self, request, *args, **kwargs):
        for name, file in request.FILES.items():
            data = request.query_params
            image = ProductImages.objects.create(
                image=file,
                name=file.name,
                product_id=data.get("product"),
                color_id=data.get("color"),
            )
            return Response(
                data=ProductImagesSerializers(instance=image).data,
                status=status.HTTP_201_CREATED,
            )
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ShopImagesViewSet(generics.GenericAPIView):
    queryset = ShopImages.objects.all()
    serializer_class = ShopImagesSerializers

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="shop",
                description="Shop identifier",
                required=True,
                type=int,
            )
        ],
        request={
            "multipart/form-data": {
                "type": "object",
                "properties": {
                    "file": {
                        "type": "string",
                        "format": "binary",
                        "description": "Файл для загрузки",
                    }
                },
                "required": ["file"],
            }
        },
        responses={
            201: OpenApiResponse(
                response=ExampleSerializer,
                examples=[
                    OpenApiExample(
                        "post example",
                        value={
                            "shop": 0,
                            "image": "string",
                            "name": "string",
                        },
                    )
                ],
            )
        },
        summary="Загрузка фото магазина",
    )
    def post(self, request, *args, **kwargs):
        for name, file in request.FILES.items():
            data = request.query_params
            shop = Shop.objects.filter(id=data.get("shop")).first()
            if not shop:
                return Response(
                    {"ditail": "shop not found"}, status=status.HTTP_404_NOT_FOUND
                )
            image = ShopImages.objects.create(
                image=file,
                name=file.name,
                shop_id=data.get("shop"),
            )
            return Response(
                data=ShopImagesSerializers(instance=image).data,
                status=status.HTTP_201_CREATED,
            )
        return Response(status=status.HTTP_400_BAD_REQUEST)


class AddShopIconImage(APIView):

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="shop",
                description="Shop identifier",
                required=True,
                type=int,
            )
        ],
        request={
            "multipart/form-data": {
                "type": "object",
                "properties": {
                    "file": {
                        "type": "string",
                        "format": "binary",
                        "description": "Файл для загрузки",
                    }
                },
                "required": ["file"],
            }
        },
        responses={
            201: OpenApiResponse(
                response=ExampleSerializer,
                examples=[
                    OpenApiExample(
                        "post example",
                        value={
                            "shop": 0,
                            "image": "string",
                            "name": "string",
                        },
                    )
                ],
            )
        },
        summary="Загрузка иконки магазина",
    )
    def post(self, request, *args, **kwargs):
        for name, file in request.FILES.items():
            data = request.query_params
            shop = Shop.objects.filter(id=data.get("shop")).first()
            if not shop:
                return Response(
                    {"ditail": "shop not found"}, status=status.HTTP_404_NOT_FOUND
                )
            shop.icon = file
            shop.save()
            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_204_NO_CONTENT)
