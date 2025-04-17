from django.urls import path, include
from rest_framework import routers

from shop.api.product import (
    ProductViewSet,
    CategoriesViewSet,
    BrandsViewSet,
    SizesViewSet,
    ColorsViewSet,
)
from shop.api.shop import ShopViewSet
from shop.api.images import ProductImagesViewSet, ShopImagesViewSet, AddShopIconImage

router = routers.SimpleRouter()
router.register("products", ProductViewSet)
router.register("categories", CategoriesViewSet)
router.register("brands", BrandsViewSet)
router.register("sizes", SizesViewSet)
router.register("colors", ColorsViewSet)
router.register("shops", ShopViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("images/rpoduct", ProductImagesViewSet.as_view()),
    path("images/shop", ShopImagesViewSet.as_view()),
    path("images/shop/icon", AddShopIconImage.as_view()),
]
