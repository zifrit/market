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
    FavoriteProduct,
    ShopImages,
    ProductRating,
    ShopRating,
)


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("id", "name")
    search_fields = ("name",)


@admin.register(Sizes)
class SizesAdmin(admin.ModelAdmin):
    list_display = ("id",)


@admin.register(Colors)
class ColorsAdmin(admin.ModelAdmin):
    list_display = ("id",)


@admin.register(Brands)
class BrandsAdmin(admin.ModelAdmin):
    list_display = ("id",)


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ("id",)


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("id",)


@admin.register(FavoriteProduct)
class FavoriteProductAdmin(admin.ModelAdmin):
    list_display = ("id",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id",)


@admin.register(ProductImages)
class ProductImagesAdmin(admin.ModelAdmin):
    list_display = ("id",)


@admin.register(ShopImages)
class ShopImagesAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "shop")


@admin.register(ProductRating)
class ProductRatingAdmin(admin.ModelAdmin):
    list_display = ("id", "rating")


@admin.register(ShopRating)
class ShopRatingAdmin(admin.ModelAdmin):
    list_display = ("id", "rating")
