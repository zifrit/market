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
    list_display = (
        "id",
        "name",
        "creator",
        "created_at",
        "status",
        "delete_at",
    )
    list_display_links = (
        "id",
        "name",
    )
    search_fields = ("name",)
    list_filter = (
        "status",
        "created_at",
        "delete_at",
    )


@admin.register(ShopReport)
class ShopReportAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "status",
        "future_owner",
        "creator",
        "status",
        "created_at",
        "delete_at",
    )
    list_filter = ("status", "created_at", "delete_at")


@admin.register(Sizes)
class SizesAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "creator",
        "name",
        "gender",
        "created_at",
        "delete_at",
    )


@admin.register(Colors)
class ColorsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "creator",
        "name",
        "hex_color",
        "created_at",
        "delete_at",
    )


@admin.register(Brands)
class BrandsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "creator",
        "name",
        "key",
        "created_at",
        "delete_at",
    )


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "creator",
        "name",
        "created_at",
        "delete_at",
    )


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "creator",
        "address",
        "created_at",
        "delete_at",
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
        "created_at",
    )


@admin.register(HumanImage)
class HumanImageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "price",
        "shop",
        "created_at",
        "delete_at",
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "price",
        "quantity",
        "created_at",
        "delete_at",
    )


@admin.register(ProductImages)
class ProductImagesAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "image",
        "product",
        "created_at",
        "delete_at",
    )


@admin.register(ShopImages)
class ShopImagesAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "shop",
        "image",
        "created_at",
        "delete_at",
    )


@admin.register(HumanImageImages)
class HumanImageImagesAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "image",
        "created_at",
        "delete_at",
    )


@admin.register(ProductRating)
class ProductRatingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "rating",
        "created_at",
        "delete_at",
    )


@admin.register(ShopRating)
class ShopRatingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "rating",
        "created_at",
        "delete_at",
    )
