from shop.models import Product, Brands, Categories, Sizes, Colors
from rest_framework.viewsets import ModelViewSet
from shop.api.serializers import (
    ProductSerializers,
    BrandsSerializer,
    CategorySerializer,
    SizeSerializer,
    ColorsSerializer,
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.select_related('brands','category','shop').prefetch_related('sizes','color')
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    serializer_class = ProductSerializers
    search_fields = ['name']
    filterset_fields = ['enabled','shop','brands','category','quantity','price']
    ordering_fields = ['price','enabled']



class BrandsViewSet(ModelViewSet):
    queryset = Brands.objects.all()
    serializer_class = BrandsSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']

class CategoriesViewSet(ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']

class SizesViewSet(ModelViewSet):
    queryset = Sizes.objects.all()
    serializer_class = SizeSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']

class ColorsViewSet(ModelViewSet):
    queryset = Colors.objects.all()
    serializer_class = ColorsSerializer
    filter_backends = [SearchFilter]
    search_fields = ['hex_color']