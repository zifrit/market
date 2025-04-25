from django.urls import path, include
from rest_framework import routers

from shop.api.product import (
    ProductViewSet,
    CategoriesViewSet,
    BrandsViewSet,
    SizesViewSet,
    ColorsViewSet,
    ListCreateProductRaringView,
)
from shop.api.shop import ShopViewSet, ListCreateShopRatingView
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
    path("products/images", ProductImagesViewSet.as_view()),
    path("shops/images", ShopImagesViewSet.as_view()),
    path("shops/icon", AddShopIconImage.as_view()),
    path("shops/rating", ListCreateShopRatingView.as_view()),
    path("products/rating", ListCreateProductRaringView.as_view()),
]
