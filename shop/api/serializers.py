from typing import List

from rest_framework import serializers

from shop.models import ProductImages, Product, Brands, Sizes, Categories, Colors, Shop


class BaseSerializer(serializers.ModelSerializer):
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())


class ProductImagesSerializers(BaseSerializer):
    color = serializers.SerializerMethodField()

    class Meta:
        model = ProductImages
        fields = ["color", "image", "name"]

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

    @staticmethod
    def get_brands(obj: Product):
        if obj.brands:
            return {"id": obj.id, "name": obj.brands.name}
        return {}

    @staticmethod
    def get_category(obj: Product):
        if obj.category:
            return {"id": obj.id, "name": obj.category.name}
        return {}

    @staticmethod
    def get_shop(obj: Product):
        if obj.shop:
            return {"id": obj.id, "name": obj.shop.name}
        return {}

    @staticmethod
    def get_color(obj: Product) -> List[dict]:
        if obj.color.first():
            color = obj.color.first()
            return [{"id": color.id, "name": color.name, "hex_color": color.hex_color}]
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

    @staticmethod
    def get_images(obj: Product) -> List[dict]:
        return [
            {
                "id": image.id,
                "color": {
                    "id": image.color.id,
                    "name": image.color.name,
                    "hex_color": image.color.hex_color,
                },
                "path": f"https://4467e3c1-clo-test.s3.twcstorage.ru/{image.image.__str__()}",
            }
            for image in obj.images.all()  # type : ProductImages
        ]


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


class ShopSerializer(BaseSerializer):
    class Meta:
        model = Shop
        exclude = ["delete_at", "is_active", "updated_at"]
