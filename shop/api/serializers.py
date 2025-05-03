from typing import List

from rest_framework import serializers

from shop.models import (
    ProductImages,
    Product,
    Brands,
    Sizes,
    Categories,
    Colors,
    Shop,
    ShopImages,
    ProductRating,
    ShopRating,
    Address,
    ShopWorkSchedules,
)


class BaseSerializer(serializers.ModelSerializer):
    pass
    # creator = serializers.HiddenField(
    #     default=serializers.CurrentUserDefault(), required=False
    # )


class ProductImagesSerializers(BaseSerializer):
    color = serializers.SerializerMethodField()
    product = serializers.IntegerField(source="product_id", read_only=True)

    class Meta:
        model = ProductImages
        fields = ["color", "image", "name", "product"]

    @staticmethod
    def get_color(obj: ProductImages) -> dict:
        return {
            "id": obj.color.id,
            "name": obj.color.name,
            "hex_color": obj.color.hex_color,
        }


class ProductSerializers(BaseSerializer):
    class Meta:
        model = Product
        exclude = ["delete_at", "enabled", "updated_at"]


class ViewProductSerializers(ProductSerializers):
    brands = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    shop = serializers.SerializerMethodField()
    color = serializers.SerializerMethodField()
    sizes = serializers.SerializerMethodField()
    images = ProductImagesSerializers(many=True, read_only=True)
    rating = serializers.SerializerMethodField()

    @staticmethod
    def get_rating(obj: Product):
        return obj.rating if obj.rating else 0

    @staticmethod
    def get_brands(obj: Product):
        if obj.brands:
            return {"id": obj.brands.id, "name": obj.brands.name}
        return {}

    @staticmethod
    def get_category(obj: Product):
        if obj.category:
            return {"id": obj.category.id, "name": obj.category.name}
        return {}

    @staticmethod
    def get_shop(obj: Product):
        if obj.shop:
            return {"id": obj.shop.id, "name": obj.shop.name}
        return {}

    @staticmethod
    def get_color(obj: Product) -> List[dict]:
        if obj.color.first():
            return [
                {"id": color.id, "name": color.name, "hex_color": color.hex_color}
                for color in obj.color.all()[:3]
            ]
        return [{}]

    @staticmethod
    def get_sizes(obj: Product) -> dict[str, List[dict]]:

        result = {"male": [], "female": []}
        if obj.sizes.filter(gender=Sizes.GenderType.MALE).first():
            size = obj.sizes.filter(gender=Sizes.GenderType.MALE).first()
            result["male"].append({"id": size.id, "name": size.name})

        if obj.sizes.filter(gender=Sizes.GenderType.FEMALE).first():
            size = obj.sizes.filter(gender=Sizes.GenderType.FEMALE).first()
            result["female"].append({"id": size.id, "name": size.name})
        return result


class RetrieveProductSerializers(ViewProductSerializers):
    @staticmethod
    def get_color(obj: Product) -> List[dict]:
        return [
            {"id": color.id, "name": color.name, "hex_color": color.hex_color}
            for color in obj.color.all()
        ]

    @staticmethod
    def get_sizes(obj: Product) -> dict[str, List[dict]]:
        result = {"male": [], "female": []}
        for size in obj.sizes.all():  # type: Sizes
            if size.gender == Sizes.GenderType.MALE:
                result["male"].append({"id": size.id, "name": size.name})
            elif size.gender == Sizes.GenderType.FEMALE:
                result["female"].append({"id": size.id, "name": size.name})

        return result


class BrandsSerializer(BaseSerializer):
    class Meta:
        model = Brands
        exclude = ["delete_at"]


class SizeSerializer(BaseSerializer):
    class Meta:
        model = Sizes
        exclude = ["delete_at"]


class CategorySerializer(BaseSerializer):
    class Meta:
        model = Categories
        exclude = ["delete_at"]


class ColorsSerializer(BaseSerializer):
    class Meta:
        model = Colors
        exclude = ["delete_at"]


class ShopImagesSerializers(BaseSerializer):
    shop = serializers.IntegerField(source="shop_id", read_only=True)

    class Meta:
        model = ShopImages
        fields = ["shop", "image", "name"]


class AddressSerializer(BaseSerializer):

    class Meta:
        model = Address
        exclude = ["delete_at"]


class CreateShopSerializer(BaseSerializer):
    images = ShopImagesSerializers(many=True, read_only=True)
    work_schedules = serializers.JSONField(
        source="work_schedules.work_schedule", read_only=True
    )
    icon = serializers.FileField(read_only=True)

    def validate_status(self, value: str) -> str:
        if value.upper() in Shop.ShopStatus:
            return value.upper()
        raise serializers.ValidationError("Invalid status")

    class Meta:
        model = Shop
        exclude = ["delete_at", "is_active", "updated_at"]


class ShowShopSerializer(CreateShopSerializer):
    address = AddressSerializer()
    rating = serializers.SerializerMethodField()

    @staticmethod
    def get_rating(obj: Shop):
        return obj.rating if getattr(obj, "rating") else 0


class ProductRatingSerializers(BaseSerializer):
    class Meta:
        model = ProductRating
        exclude = ["delete_at"]


class ShopRatingSerializer(BaseSerializer):
    class Meta:
        model = ShopRating
        exclude = ["delete_at"]


class ShopWorkScheduleSerializer(BaseSerializer):

    class Meta:
        model = ShopWorkSchedules
        exclude = ["delete_at"]


class ExampleSerializer(serializers.Serializer):
    example = serializers.CharField()
