from shop.models import Product, Brands, Categories, Sizes, Colors
from rest_framework.viewsets import ModelViewSet
from shop.api.serializers import ProductSerializers, BrandsSerializer, CategorySerializer, SizeSerializer, \
    ColorsSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers


class BrandsViewSet(ModelViewSet):
    queryset = Brands.objects.all()
    serializer_class = BrandsSerializer


class CategoriesViewSet(ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategorySerializer


class SizesViewSet(ModelViewSet):
    queryset = Sizes.objects.all()
    serializer_class = SizeSerializer


class ColorsViewSet(ModelViewSet):
    queryset = Colors.objects.all()
    serializer_class = ColorsSerializer
