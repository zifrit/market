from django.urls import path, include
from rest_framework import routers

from shop.api.product import (
    ProductViewSet,
    CategoriesViewSet,
    BrandsViewSet,
    SizesViewSet,
    ColorsViewSet,
    ListCreateProductRatingView,
    CreateListHumanImageView,
    UpdateDeleteHumanImageView,
)
from shop.api.shop import (
    ShopViewSet,
    ListCreateShopRatingView,
    UpdateCreateWorkScheduleView,
    ListCreateShopReportView,
    UpdateRetrieveShopReportView,
    VerifyShopReportView,
)
from shop.api.address import AddressViewSet
from shop.api.images import (
    ProductImagesViewSet,
    ShopImagesViewSet,
    AddShopIconImage,
    DeleteProductImagesView,
    DeleteShopImagesView,
    HumanImageImagesView,
    DeleteHumanImageImagesView,
)

router = routers.SimpleRouter()
router.register("products", ProductViewSet)
router.register("categories", CategoriesViewSet)
router.register("brands", BrandsViewSet)
router.register("sizes", SizesViewSet)
router.register("colors", ColorsViewSet)
router.register("shops", ShopViewSet)
router.register("address", AddressViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("human-image", CreateListHumanImageView.as_view()),
    path("human-image/<int:pk>/", UpdateDeleteHumanImageView.as_view()),
    path("human-image/images", HumanImageImagesView.as_view()),
    path(
        "human-image/<int:id>/images/<int:image_id>",
        DeleteHumanImageImagesView.as_view(),
    ),
    path("products/images", ProductImagesViewSet.as_view()),
    path(
        "products/<int:id>/images/<int:image_id>",
        DeleteProductImagesView.as_view(),
    ),
    path("shops/images", ShopImagesViewSet.as_view()),
    path(
        "shops/<int:id>/images/<int:image_id>",
        DeleteShopImagesView.as_view(),
    ),
    path("shops/icon", AddShopIconImage.as_view()),
    path("shops/report", ListCreateShopReportView.as_view()),
    path("shops/report/<int:pk>", UpdateRetrieveShopReportView.as_view()),
    path("shops/report/<int:pk>/verify", VerifyShopReportView.as_view()),
    path("shops/<int:id>/rating", ListCreateShopRatingView.as_view()),
    path("shops/workwork-schedule", UpdateCreateWorkScheduleView.as_view()),
    path("products/<int:id>/rating", ListCreateProductRatingView.as_view()),
]
