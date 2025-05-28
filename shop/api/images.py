from drf_spectacular.utils import (
    extend_schema,
    OpenApiExample,
    OpenApiParameter,
    OpenApiResponse,
)
from rest_framework import generics, status
from rest_framework.response import Response

from clo.permission import CustomBasePermission
from shop.models import (
    ProductImages,
    ShopImages,
    Shop,
    Product,
    HumanImage,
    HumanImageImages,
)
from shop.api.serializers import (
    ProductImagesSerializers,
    ShopImagesSerializers,
    ExampleSerializer,
    HumanImageImagesSerializers,
)


class ProductImagesViewSet(CustomBasePermission):
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
                    "files": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "format": "binary",
                        },
                        "description": "Файлы для загрузки",
                    }
                },
                "required": ["files"],
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
        images = []
        for file in request.FILES.getlist("files"):
            data = request.query_params
            product = Product.objects.filter(id=data["product"]).first()
            if not product:
                return Response(
                    {"ditail": "product not found"}, status=status.HTTP_404_NOT_FOUND
                )
            image = ProductImages.objects.create(
                image=file,
                name=file.name,
                product_id=data.get("product"),
                color_id=data.get("color"),
            )
            images.append(image)
        if images:
            return Response(
                data=ProductImagesSerializers(instance=images, many=True).data,
                status=status.HTTP_201_CREATED,
            )
        return Response(status=status.HTTP_400_BAD_REQUEST)


class DeleteProductImagesView(generics.DestroyAPIView, CustomBasePermission):
    queryset = ProductImages.objects.all()

    def destroy(self, request, *args, **kwargs):
        product_id = kwargs["id"]
        image_id = kwargs["image_id"]
        if image := ProductImages.objects.filter(
            id=image_id, product_id=product_id
        ).first():
            image.delete()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "not found"})


class ShopImagesViewSet(CustomBasePermission):
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
                    "files": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "format": "binary",
                        },
                        "description": "Файлы для загрузки",
                    }
                },
                "required": ["files"],
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
        images = []
        for file in request.FILES.getlist("files"):
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
            images.append(image)
        if images:
            return Response(
                data=ShopImagesSerializers(instance=images, many=True).data,
                status=status.HTTP_201_CREATED,
            )
        return Response(status=status.HTTP_400_BAD_REQUEST)


class DeleteShopImagesView(generics.DestroyAPIView, CustomBasePermission):
    queryset = ShopImages.objects.all()

    def destroy(self, request, *args, **kwargs):
        shop_id = kwargs["id"]
        image_id = kwargs["image_id"]
        if image := ShopImages.objects.filter(id=image_id, shop_id=shop_id).first():
            image.delete()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "not found"})


class AddShopIconImage(generics.GenericAPIView):

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


class HumanImageImagesView(CustomBasePermission):
    queryset = HumanImage.objects.all()
    serializer_class = ShopImagesSerializers

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="human_image",
                description="Human Image identifier",
                required=True,
                type=int,
            )
        ],
        request={
            "multipart/form-data": {
                "type": "object",
                "properties": {
                    "files": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "format": "binary",
                        },
                        "description": "Файлы для загрузки",
                    }
                },
                "required": ["files"],
            }
        },
        responses={
            201: OpenApiResponse(
                response=ExampleSerializer,
                examples=[
                    OpenApiExample(
                        "post example",
                        value={
                            "human_image": 0,
                            "image": "string",
                            "name": "string",
                        },
                    )
                ],
            )
        },
        summary="Загрузка фото образа",
    )
    def post(self, request, *args, **kwargs):
        images = []
        for file in request.FILES.getlist("files"):
            data = request.query_params
            human_image = HumanImage.objects.filter(id=data.get("human_image")).first()
            if not human_image:
                return Response(
                    {"ditail": "Human image not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            image = HumanImageImages.objects.create(
                image=file,
                name=file.name,
                human_image_id=data.get("human_image"),
            )
            images.append(image)
        if images:
            return Response(
                data=HumanImageImagesSerializers(instance=images, many=True).data,
                status=status.HTTP_201_CREATED,
            )
        return Response(status=status.HTTP_400_BAD_REQUEST)


class DeleteHumanImageImagesView(generics.DestroyAPIView, CustomBasePermission):
    queryset = HumanImage.objects.all()

    def destroy(self, request, *args, **kwargs):
        human_image_id = kwargs["id"]
        image_id = kwargs["image_id"]
        if image := HumanImageImages.objects.filter(
            id=image_id, human_image_id=human_image_id
        ).first():
            image.delete()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "not found"})
