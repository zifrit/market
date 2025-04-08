from shop.models import Shop
from rest_framework.viewsets import ModelViewSet
from shop.api.serializers import ShopSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter

class ShopViewSet(ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    search_fields = ['name']
    filterset_fields = ['is_active','status']
    ordering_fields = ['is_active']