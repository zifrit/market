from shop.models import Product, Brands, Categories, Sizes
from rest_framework.viewsets import ModelViewSet
from shop.api.serializers import ProductSerializers, BrandsSerializer, CategorySerializer, SizeSerializer

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