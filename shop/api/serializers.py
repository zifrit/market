from random import randint
from typing import List

from django.db import transaction
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
    HumanImage,
    ProductHumanImages,
    CustomUserFavoriteProduct,
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
        fields = ["id", "color", "image", "name", "product"]

    @staticmethod
    def get_color(obj: ProductImages) -> dict:
        return {
            "id": obj.color.id,
            "name": obj.color.name,
            "hex_color": obj.color.hex_color,
        }


class ProductSerializers(BaseSerializer):
    external_id = serializers.CharField(read_only=True)

    class Meta:
        model = Product
        exclude = ["delete_at", "enabled", "updated_at"]

    def create(self, validated_data):
        external_id = randint(10_000_000, 99_999_999)
        while (
            Product.objects.filter(external_id=external_id)
            .only("id", "external_id")
            .exists()
        ):
            external_id = randint(10_000_000, 99_999_999)

        product = Product.objects.create(**validated_data, external_id=external_id)
        return product


class ViewProductSerializers(ProductSerializers):
    brands = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    shop = serializers.SerializerMethodField()
    color = serializers.SerializerMethodField()
    sizes = serializers.SerializerMethodField()
    images = ProductImagesSerializers(many=True, read_only=True)
    rating = serializers.SerializerMethodField()
    favorites = serializers.SerializerMethodField()

    @staticmethod
    def get_rating(obj: Product) -> int:
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
    def get_favorites(obj: Product) -> list[int]:
        result = []
        for favorite in obj.favorites.all():  # type: CustomUserFavoriteProduct
            result.append(favorite.user_id)
        return result

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
        for size in obj.sizes.all():  # type: Sizes
            if size.gender == Sizes.GenderType.MALE and not result["male"]:
                result["male"].append({"name": size.name})
            elif size.gender == Sizes.GenderType.FEMALE and not result["female"]:
                result["female"].append({"name": size.name})
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
                result["male"].append({"name": size.name})
            elif size.gender == Sizes.GenderType.FEMALE:
                result["female"].append({"name": size.name})

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
        fields = ["id", "shop", "image", "name"]


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


class ProductHumanImagesSerializer(BaseSerializer):

    class Meta:
        model = ProductHumanImages
        exclude = ["human_image", "id"]


class HumanImageImagesSerializers(BaseSerializer):

    class Meta:
        model = ShopImages
        fields = ["id", "image", "name"]


class HumanImageSerializer(BaseSerializer):
    product_human_images = ProductHumanImagesSerializer(many=True, required=False)
    images = HumanImageImagesSerializers(many=True, read_only=True)

    class Meta:
        model = HumanImage
        exclude = ["delete_at", "creator", "products"]

    def to_representation(self, instance: HumanImage):
        my_representation = super(HumanImageSerializer, self).to_representation(
            instance
        )
        my_representation["product_human_images"] = [
            {
                "product": {
                    "id": item.product_id,
                    "name": item.product.name,
                    "brands_id": item.product.brands_id,
                },
                "product_color": item.product_color_id,
                "product_image": {
                    "path": str(item.product_image.image.url),
                    "id": item.product_image.id,
                    "name": item.product_image.name,
                },
            }
            for item in ProductHumanImages.objects.filter(human_image=instance)
            .select_related("product", "product_image")
            .only(
                "product_id",
                "product__name",
                "product__brands_id",
                "product_image__image",
                "product_image__id",
                "product_image__name",
                "product_color_id",
            )  # type: ProductHumanImages
        ]
        return my_representation

    def validate_product_human_images(self, value):
        if len(value) > 4:
            raise serializers.ValidationError(
                "Product human images can not be longer than 4"
            )
        return value

    def create(self, validated_data):
        print(validated_data)
        product_human_images_data = validated_data.pop("product_human_images", [])
        with transaction.atomic():
            human_image = HumanImage.objects.create(**validated_data)

            for product_human_image_data in product_human_images_data:
                ProductHumanImages.objects.create(
                    human_image=human_image, **product_human_image_data
                )

        return human_image

    def update(self, instance: HumanImage, validated_data):
        product_human_images_data = validated_data.pop("product_human_images", None)
        with transaction.atomic():
            instance.price = validated_data.get("price", instance.price)
            instance.name = validated_data.get("name", instance.name)
            instance.description = validated_data.get(
                "description", instance.description
            )
            instance.save()

            if product_human_images_data is not None:
                instance.products.all().delete()
                for product_human_image_data in product_human_images_data:
                    ProductHumanImages.objects.create(
                        human_image=instance, **product_human_image_data
                    )

        return instance


class ViewHumanImageSerializer(BaseSerializer):
    product_human_images = ProductHumanImagesSerializer(many=True, read_only=True)
    images = HumanImageImagesSerializers(many=True, read_only=True)

    def to_representation(self, instance: HumanImage):
        my_representation = super(ViewHumanImageSerializer, self).to_representation(
            instance
        )
        my_representation["product_human_images"] = [
            {
                "product": {
                    "name": item.product.name,
                    "brands": item.product.brands_id,
                },
                "product_color": item.product_color_id,
                "product_image": str(item.product_image.image.url),
            }
            for item in ProductHumanImages.objects.filter(human_image=instance)
            .select_related("product", "product_image")
            .only(
                "product__name",
                "product__brands_id",
                "product_image__image",
                "product_color_id",
            )  # type: ProductHumanImages
        ]
        return my_representation

    class Meta:
        model = HumanImage
        fields = [
            "product_human_images",
            "name",
            "price",
            "id",
            "description",
            "images",
        ]


class ExampleSerializer(serializers.Serializer):
    example = serializers.CharField()
