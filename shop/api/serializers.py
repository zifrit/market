from rest_framework import serializers
from shop.models import *


class BaseSerializer(serializers.ModelSerializer):
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())


class ProductSerializers(BaseSerializer):
    class Meta:
        model = Product
        exclude = ['delete_at','enabled','updated_at']

class ViewProductSerializers(ProductSerializers):
    brands = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    shop = serializers.SerializerMethodField()

    @staticmethod
    def get_brands(obj: Product):
        if obj.brands:
            return {"id": obj.id, "name":obj.brands.name}
        return {}

    @staticmethod
    def get_category(obj: Product):
        if obj.category:
            return {"id": obj.id, "name":obj.category.name}
        return {}

    @staticmethod
    def get_shop(obj: Product):
        if obj.shop:
            return {"id": obj.id, "name":obj.shop.name}
        return {}



class ProductImagesSerializers(BaseSerializer):
    class Meta:
        model = ProductImages
        fields = ['product','color','image']


class BrandsSerializer(BaseSerializer):
    class Meta:
        model = Brands
        exclude = ['delete_at']


class SizeSerializer(BaseSerializer):
    class Meta:
        model = Sizes
        exclude = ['delete_at']


class CategorySerializer(BaseSerializer):
    class Meta:
        model = Categories
        exclude = ['delete_at']


class ColorsSerializer(BaseSerializer):
    class Meta:
        model = Colors
        exclude = ['delete_at']


class ShopSerializer(BaseSerializer):
    class Meta:
        model = Shop
        exclude = ['delete_at','is_active','updated_at']