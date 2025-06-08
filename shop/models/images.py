from django.db import models

from context.models import TimeStampMixin, CreatorMixin
from storages.backends.s3boto3 import S3Boto3Storage


class ProductImages(TimeStampMixin, CreatorMixin):
    name = models.CharField(max_length=200, verbose_name="Название")
    product = models.ForeignKey(
        "shop.Product",
        on_delete=models.CASCADE,
        verbose_name="Продукт",
        related_name="images",
        blank=True,
        null=True,
    )
    color = models.ForeignKey(
        "shop.Colors",
        on_delete=models.CASCADE,
        verbose_name="Цвет",
        related_name="images",
        blank=True,
        null=True,
    )
    image = models.FileField(
        upload_to="products/images/%Y-%m-%d/",  # путь в S3
        storage=S3Boto3Storage(),
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["created_at", "id"]
        db_table = "clo_product_images"
        verbose_name = "ProductImage"
        verbose_name_plural = "ProductImages"

    def __str__(self):
        return self.name


class ShopImages(TimeStampMixin, CreatorMixin):
    name = models.CharField(max_length=200, verbose_name="Название")
    shop = models.ForeignKey(
        "shop.Shop",
        on_delete=models.CASCADE,
        verbose_name="Магазин",
        related_name="images",
        blank=True,
        null=True,
    )
    image = models.FileField(
        upload_to="shop/images/%Y-%m-%d/",  # путь в S3
        storage=S3Boto3Storage(),
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["created_at", "id"]
        db_table = "clo_shop_images"
        verbose_name = "ShopImage"
        verbose_name_plural = "ShopImages"

    def __str__(self):
        return self.name


class HumanImageImages(TimeStampMixin, CreatorMixin):
    name = models.CharField(max_length=200, verbose_name="Название")
    human_image = models.ForeignKey(
        "shop.HumanImage",
        on_delete=models.CASCADE,
        verbose_name="Образ",
        related_name="images",
        blank=True,
        null=True,
    )
    image = models.FileField(
        upload_to="shop/images/%Y-%m-%d/",  # путь в S3
        storage=S3Boto3Storage(),
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["created_at", "id"]
        db_table = "clo_human_image_images"
        verbose_name = "HumanImageImage"
        verbose_name_plural = "HumanImageImages"

    def __str__(self):
        return self.name
