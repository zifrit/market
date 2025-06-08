from django.contrib import admin

# Register your models here.
from shop.models import (
    Shop,
    Sizes,
    Colors,
    Brands,
    Product,
    ProductImages,
    Categories,
    Address,
    CustomUserFavoriteProduct,
    ShopImages,
    ProductRating,
    ShopRating,
    ShopReport,
    HumanImageImages,
    HumanImage,
)


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "creator")
    list_display_links = ("id", "name")
    search_fields = ("name",)


@admin.register(ShopReport)
class ShopReportAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "status",
        "future_owner",
        "creator",
    )


@admin.register(Sizes)
class SizesAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "creator",
        "name",
        "gender",
    )


@admin.register(Colors)
class ColorsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "creator",
        "name",
        "hex_color",
    )


@admin.register(Brands)
class BrandsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "creator",
        "name",
        "key",
    )


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "creator",
        "name",
    )


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "creator",
        "address",
    )


@admin.register(CustomUserFavoriteProduct)
class CustomUserFavoriteProductAdmin(admin.ModelAdmin):
    search_fields = (
        "id",
        "product__name",
        "user__phone",
    )
    list_display = (
        "id",
        "product_id",
        "product__name",
        "user_id",
        "user__phone",
    )


@admin.register(HumanImage)
class HumanImageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "price",
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "price",
        "quantity",
    )


@admin.register(ProductImages)
class ProductImagesAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "image",
        "product",
    )


@admin.register(ShopImages)
class ShopImagesAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "shop",
        "image",
    )


@admin.register(HumanImageImages)
class HumanImageImagesAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "image")


@admin.register(ProductRating)
class ProductRatingAdmin(admin.ModelAdmin):
    list_display = ("id", "rating")


@admin.register(ShopRating)
class ShopRatingAdmin(admin.ModelAdmin):
    list_display = ("id", "rating")
