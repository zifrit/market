from rest_framework import serializers
from shop.models import *


class BaseSerializer(serializers.ModelSerializer):
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())


class ProductSerializers(BaseSerializer):
    class Meta:
        model = Product
        exclude = ['delete','enabled']


class ProductImagesSerializers(BaseSerializer):
    class Meta:
        model = ProductImages
        exclude = ['delete']


class BrandsSerializer(BaseSerializer):
    class Meta:
        model = Brands
        exclude = ['delete']


class SizeSerializer(BaseSerializer):
    class Meta:
        model = Sizes
        exclude = ['delete']


class CategorySerializer(BaseSerializer):
    class Meta:
        model = Categories
        exclude = ['delete']


class ColorsSerializer(BaseSerializer):
    class Meta:
        model = Colors
        exclude = ['delete']