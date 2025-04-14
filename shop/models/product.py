from django.db import models

from context.models import TimeStampMixin, CreatorMixin


class Product(TimeStampMixin, CreatorMixin):
    name = models.CharField(
        verbose_name="Название", blank=True, null=True, max_length=255
    )
    price = models.PositiveIntegerField(verbose_name="Цена", blank=True, null=True)
    description = models.TextField(verbose_name="Описание", blank=True, null=True)
    enabled = models.BooleanField(verbose_name="Включен", default=True)
    quantity = models.PositiveIntegerField(
        verbose_name="Количество", blank=True, null=True
    )
    color = models.ManyToManyField("Colors", verbose_name="Цвет", blank=True)
    brands = models.ForeignKey(
        "Brands",
        verbose_name="Бренды",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    category = models.ForeignKey(
        "Categories",
        verbose_name="Категория",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    sizes = models.ManyToManyField("Sizes", verbose_name="Размеры", blank=True)
    shop = models.ForeignKey(
        "shop.Shop",
        verbose_name="магазин",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ["created_at", "id"]
        db_table = "clo_product"
        verbose_name = "Product"
        verbose_name_plural = "Products"


class Colors(TimeStampMixin, CreatorMixin):
    name = models.CharField(
        verbose_name="Название", blank=True, null=True, max_length=255
    )
    hex_color = models.CharField(
        verbose_name="Цвет", blank=True, null=True, max_length=255
    )

    class Meta:
        ordering = ["created_at", "id"]
        db_table = "clo_colors"
        verbose_name = "Color"
        verbose_name_plural = "Colors"


class Brands(TimeStampMixin, CreatorMixin):
    key = models.CharField(blank=True, null=True, max_length=255)
    name = models.CharField(
        verbose_name="Название", blank=True, null=True, max_length=255
    )

    class Meta:
        ordering = ["created_at", "id"]
        db_table = "clo_brands"
        verbose_name = "Brand"
        verbose_name_plural = "Brands"


class Categories(TimeStampMixin, CreatorMixin):
    name = models.CharField(
        verbose_name="Название", blank=True, null=True, max_length=255
    )

    class Meta:
        ordering = ["created_at", "id"]
        db_table = "clo_categories"
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Sizes(TimeStampMixin, CreatorMixin):
    class GenderType(models.TextChoices):
        MALE = "MALE", "Мужчина"
        FEMALE = "FEMALE", "Женщина"

    gender = models.CharField(
        max_length=10, choices=GenderType.choices, blank=True, null=True
    )
    name = models.CharField(
        verbose_name="Название", blank=True, null=True, max_length=255
    )

    class Meta:
        ordering = ["created_at", "id"]
        db_table = "clo_sizes"
        verbose_name = "Size"
        verbose_name_plural = "Sizes"
