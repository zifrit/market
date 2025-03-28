from django.contrib import admin

# Register your models here.
from shop.models import Shop, Sizes, Colors, Brands, Product, ProductImages


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    readonly_fields = ("id",)
    search_fields = ("name",)


@admin.register(Sizes)
class SizesAdmin(admin.ModelAdmin):
    readonly_fields = ("id",)

@admin.register(Colors)
class ColorsAdmin(admin.ModelAdmin):
    readonly_fields = ("id",)

@admin.register(Brands)
class BrandsAdmin(admin.ModelAdmin):
    readonly_fields = ("id",)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ("id",)

@admin.register(ProductImages)
class ProductImagesAdmin(admin.ModelAdmin):
    readonly_fields = ("id",)
