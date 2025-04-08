from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiParameter
from rest_framework import generics, status
from rest_framework.response import Response

from shop.models import ProductImages
from rest_framework.viewsets import ModelViewSet
from shop.api.serializers import ProductImagesSerializers

class ProductImagesViewSet(generics.GenericAPIView):
    queryset = ProductImages.objects.all()
    serializer_class = ProductImagesSerializers

    @extend_schema(
        parameters=[
            OpenApiParameter(name='product', description='Product identifier', required=True, type=int),
            OpenApiParameter(name='color', description='Color identifier', required=True, type=int),
        ],
        request={
            'multipart/form-data': {
                'type': 'object',
                'properties': {
                    'file': {
                        'type': 'string',
                        'format': 'binary',
                        'description': 'Файл для загрузки'
                    }
                },
                'required': ['file']
            }
        },
        responses={
            201: {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'},
                    'filename': {'type': 'string'},
                    'size': {'type': 'integer'}
                }
            },
        },
        summary='Загрузка фото продукта',
    )
    def post(self, request, *args, **kwargs):
        for name, file in request.FILES.items():
            data = request.data
            image = ProductImages.objects.create(
                image=file,
                name=file.name,
                product_id=data.get('product'),
                color_id=data.get('color'),
            )
            return Response(data=ProductImagesSerializers(instance=image).data(),status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
