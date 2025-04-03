from django.urls import path, include
from rest_framework import routers

from shop.api.product import ProductViewSet, CategoriesViewSet, BrandsViewSet, SizesViewSet
from shop.api.images import ProductImagesViewSet

router = routers.SimpleRouter()
router.register('products', ProductViewSet)
router.register('categories', CategoriesViewSet)
router.register('brands', BrandsViewSet)
router.register('sizes', SizesViewSet)
# router.register('images', ProductImagesViewSet)
urlpatterns = [
    path('', include(router.urls)),
]