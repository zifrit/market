from shop.models import ProductImages
from rest_framework.viewsets import ModelViewSet
from shop.api.serializers import ProductImagesSerializers

class ProductImagesViewSet(ModelViewSet):
    queryset = ProductImages.objects.all()
    serializer_class = ProductImagesSerializers